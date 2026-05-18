# -*- coding: utf-8 -*-
"""
Custom dialogs: encoding/cipher selector, smart replace, etc.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, BooleanVar
import re

def ask_encoding_and_cipher(parent, raw_data: bytes, dark_theme: bool,
                            get_cipher_func, decrypt_func, preview_length=816):
    win = tk.Toplevel(parent)
    win.title("Select encoding and cipher")
    win.geometry("600x500")
    win.transient(parent)
    win.grab_set()

    bg = "#1e1e1e" if dark_theme else "#ffffff"
    fg = "white" if dark_theme else "black"
    win.configure(bg=bg)

    tk.Label(win, text="Encoding:", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10,0))
    encoding_var = tk.StringVar(value="shift_jis")
    encodings = ["shift_jis", "cp932", "latin-1", "utf-8", "cp850"]
    enc_menu = ttk.Combobox(win, textvariable=encoding_var, values=encodings, state="readonly")
    enc_menu.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

    tk.Label(win, text="Cipher:", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10,0))
    cipher_var = tk.StringVar(value="auto")
    cipher_auto = tk.Radiobutton(win, text="Auto-detect", variable=cipher_var, value="auto", bg=bg, fg=fg, selectcolor=bg)
    cipher_none = tk.Radiobutton(win, text="None (0)", variable=cipher_var, value="0", bg=bg, fg=fg, selectcolor=bg)
    cipher_manual = tk.Radiobutton(win, text="Manual:", variable=cipher_var, value="manual", bg=bg, fg=fg, selectcolor=bg)
    cipher_auto.pack(anchor=tk.W, padx=20)
    cipher_none.pack(anchor=tk.W, padx=20)
    cipher_manual.pack(anchor=tk.W, padx=20)

    cipher_entry = tk.Entry(win, width=6, state=tk.DISABLED)
    cipher_entry.pack(anchor=tk.W, padx=40, pady=5)

    def on_cipher_choice(*args):
        if cipher_var.get() == "manual":
            cipher_entry.config(state=tk.NORMAL)
        else:
            cipher_entry.config(state=tk.DISABLED)
    cipher_var.trace_add('write', on_cipher_choice)

    tk.Label(win, text=f"Preview (first {preview_length} bytes decoded):", bg=bg, fg=fg,
             font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10,0))
    preview = scrolledtext.ScrolledText(win, height=10, wrap=tk.WORD, bg=bg, fg=fg, font=("Courier New", 9))
    preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def update_preview():
        enc = encoding_var.get()
        mode = cipher_var.get()
        if not raw_data:
            preview.delete(1.0, tk.END)
            preview.insert(tk.END, "No data to preview")
            return
        if mode == "auto":
            cipher = get_cipher_func(raw_data)
        elif mode == "0":
            cipher = 0
        else:
            try:
                cipher = int(cipher_entry.get().strip())
            except:
                cipher = 0
        decrypted = decrypt_func(raw_data, cipher) if cipher != 0 else raw_data
        try:
            text = decrypted.decode(enc, errors="replace")
        except LookupError:
            text = f"Unknown encoding: {enc}"
        except Exception as e:
            text = f"Decoding error: {e}"
        preview.delete(1.0, tk.END)
        preview.insert(tk.END, text[:preview_length])

    encoding_var.trace_add('write', lambda *_: update_preview())
    cipher_var.trace_add('write', lambda *_: update_preview())
    cipher_entry.bind("<KeyRelease>", lambda e: update_preview())

    btn_frame = tk.Frame(win, bg=bg)
    btn_frame.pack(pady=10)
    btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark_theme else {"bg": "#e0e0e0", "fg": "black"}

    result = [None, None]

    def accept():
        enc = encoding_var.get()
        mode = cipher_var.get()
        if mode == "auto":
            cipher = get_cipher_func(raw_data)
        elif mode == "0":
            cipher = 0
        else:
            try:
                cipher = int(cipher_entry.get().strip())
            except:
                cipher = 0
        result[0] = enc
        result[1] = cipher
        win.destroy()

    def suggest():
        best_enc, best_cipher = auto_detect_best(raw_data, get_cipher_func, decrypt_func)
        if best_enc:
            encoding_var.set(best_enc)
        if best_cipher is not None:
            cipher_var.set("manual")
            cipher_entry.delete(0, tk.END)
            cipher_entry.insert(0, str(best_cipher))
        update_preview()

    tk.Button(btn_frame, text="Accept", command=accept, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Cancel", command=win.destroy, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Suggest (Auto-detect)", command=suggest, **btn_style).pack(side=tk.LEFT, padx=10)

    update_preview()
    win.wait_window()
    if result[0] is None:
        return None, None
    return result[0], result[1]

def auto_detect_best(raw_data, get_cipher_func, decrypt_func):
    best_score = -1
    best_enc = None
    best_cipher = 0
    encodings = ["shift_jis", "cp932", "latin-1", "utf-8", "cp850"]
    for enc in encodings:
        cipher = get_cipher_func(raw_data)
        for c in (cipher, 0):
            try:
                decrypted = decrypt_func(raw_data, c) if c != 0 else raw_data
                text = decrypted.decode(enc, errors="replace")
                printable = sum(1 for ch in text if ch.isprintable() or ch in "\n\r\t")
                total = len(text)
                if total == 0:
                    score = 0
                else:
                    ratio = printable / total
                    bonus = 20 if re.search(r'<[A-Z0-9+\-]+', text) else 0
                    bonus += 10 if re.search(r'#[0-9A-F]{4}', text) else 0
                    score = ratio * 100 + bonus
                if score > best_score:
                    best_score = score
                    best_enc = enc
                    best_cipher = c
            except:
                continue
    return best_enc, best_cipher

def smart_replace_dialog(parent, text_widget, tr, dark_theme):
    try:
        selected = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        has_selection = True
    except tk.TclError:
        selected = text_widget.get("1.0", tk.END)
        has_selection = False
    if not selected.strip():
        messagebox.showinfo(tr['smart_replace_title'], "No text to process.", parent=parent)
        return

    win = tk.Toplevel(parent)
    win.title(tr['smart_replace_title'])
    win.geometry("450x320")
    win.transient(parent)
    win.grab_set()
    win.resizable(False, False)

    bg = "#1e1e1e" if dark_theme else "#ffffff"
    fg = "white" if dark_theme else "black"
    win.configure(bg=bg)

    var_nn = tk.BooleanVar(value=True)
    var_accents = tk.BooleanVar(value=True)
    var_symbols = tk.BooleanVar(value=True)
    var_all = tk.BooleanVar(value=False)

    def update_all():
        if var_all.get():
            var_nn.set(True)
            var_accents.set(True)
            var_symbols.set(True)

    tk.Label(win, text="Select which characters to replace/remove:", font=("Segoe UI", 10, "bold"),
             bg=bg, fg=fg).pack(pady=10)
    tk.Checkbutton(win, text=tr['option_nn'], variable=var_nn, command=lambda: var_all.set(False),
                   bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=2)
    tk.Checkbutton(win, text=tr['option_accents'], variable=var_accents, command=lambda: var_all.set(False),
                   bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=2)
    tk.Checkbutton(win, text=tr['option_symbols'], variable=var_symbols, command=lambda: var_all.set(False),
                   bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=2)
    tk.Checkbutton(win, text=tr['option_all'], variable=var_all, command=update_all,
                   bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=10)

    btn_frame = tk.Frame(win, bg=bg)
    btn_frame.pack(pady=20)
    btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark_theme else {"bg": "#e0e0e0", "fg": "black"}

    def apply_changes():
        new_text = selected
        if var_nn.get():
            new_text = new_text.replace('ñ', 'n').replace('Ñ', 'N')
        if var_accents.get():
            accent_map = {
                'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
                'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U'
            }
            for acc, repl in accent_map.items():
                new_text = new_text.replace(acc, repl)
        if var_symbols.get():
            new_text = new_text.replace('¡', '').replace('¿', '')
        if new_text != selected:
            msg = tr['backup_warning']
            if not messagebox.askyesno(tr['confirm'], msg, parent=win):
                return
            if has_selection:
                text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                text_widget.insert(tk.INSERT, new_text)
            else:
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", new_text)
            messagebox.showinfo(tr['done'], "Special characters replaced/removed.", parent=win)
        else:
            messagebox.showinfo(tr['no_changes'], "No characters to replace.", parent=win)
        win.destroy()

    tk.Button(btn_frame, text=tr['apply_btn'], command=apply_changes, width=10, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text=tr['close_btn'], command=win.destroy, width=10, **btn_style).pack(side=tk.LEFT, padx=10)
