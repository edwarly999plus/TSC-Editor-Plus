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
    encodings = ["shift_jis", "cp932", "latin-1", "utf-8", "cp850", "cp1252"]
    encoding_descriptions = {
        "shift_jis": "original Japanese, recommended for Japanese/English mods",
        "cp932": "Windows Japanese variant",
        "latin-1": "ISO-8859-1, fallback for Western European",
        "utf-8": "Unicode, best for modern files (Switch, plain text)",
        "cp850": "MS-DOS Latin-1, legacy",
        "cp1252": "Windows-1252, for Spanish and other European languages, recommended for translators"
    }

    # Encriptions Desc Engine
    desc_label = tk.Label(win, text="", bg=bg, fg=fg, wraplength=550, justify=tk.LEFT)
    desc_label.pack(anchor=tk.W, padx=10, pady=2, fill=tk.X)
    def update_description(*args):
        enc = encoding_var.get()
        desc = encoding_descriptions.get(enc, "")
        desc_label.config(text=desc)
    encoding_var.trace_add('write', update_description)
    update_description()

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
    encodings = ["cp1252", "shift_jis", "cp932", "latin-1", "utf-8", "cp850"]
    auto_cipher = get_cipher_func(raw_data)
    
    # Caracteres que son sospechosos en latin-1 (generalmente indican shift_jis mal decodificado)
    suspicious_latin1 = set('»½«°©¾±÷×')
    # Caracteres típicos de shift_jis (rango katakana/hiragana aproximado)
    hiragana_katakana_range = range(0x3040, 0x30FF)  # Unicode ranges
    # Caracteres españoles
    spanish_chars = set('áéíóúüñÁÉÍÓÚÜÑ')
    spanish_punct = set('¡¿')
    
    for enc in encodings:
        for c in (auto_cipher, 0):
            try:
                decrypted = decrypt_func(raw_data, c) if c != 0 else raw_data
                text = decrypted.decode(enc, errors="replace")
                total = len(text)
                if total == 0:
                    score = 0
                else:
                    printable = sum(1 for ch in text if ch.isprintable() or ch in "\n\r\t")
                    replacement_count = text.count('�')
                    ratio = (printable - replacement_count) / total
                    
                    # Bonus por comandos TSC y eventos
                    cmd_bonus = 30 if re.search(r'<[A-Z0-9+\-]+', text) else 0
                    event_bonus = 15 if re.search(r'#[0-9A-F]{4}', text) else 0
                    
                    # Bonus por caracteres españoles
                    spanish_bonus = 0
                    for ch in spanish_chars:
                        if ch in text:
                            spanish_bonus += 5
                            break
                    punct_bonus = 0
                    for ch in spanish_punct:
                        if ch in text:
                            punct_bonus += 15
                            break
                    if re.search(r'No\.\d{2}', text):
                        punct_bonus += 20
                    
                    # Bonus por caracteres japoneses (si hay hiragana/katakana)
                    jp_bonus = 0
                    for ch in text:
                        if ord(ch) in hiragana_katakana_range:
                            jp_bonus = 30
                            break
                    
                    # Penalizaciones
                    penalty = replacement_count * 3
                    
                    # Penalización específica para latin-1
                    if enc == "latin-1":
                        suspicious_count = sum(1 for ch in text if ch in suspicious_latin1)
                        suspicious_ratio = suspicious_count / total if total > 0 else 0
                        # Si hay muchos caracteres sospechosos, penalizar fuerte
                        if suspicious_ratio > 0.05:
                            penalty += 200
                        # Si no hay bonus de español ni japonés, penalizar más
                        if spanish_bonus == 0 and jp_bonus == 0 and cmd_bonus < 20:
                            penalty += 100
                    
                    # Penalización para cp850 (similar a antes)
                    if enc == "cp850":
                        non_ascii_count = sum(1 for ch in text if ord(ch) > 127)
                        non_ascii_ratio = non_ascii_count / total if total > 0 else 0
                        if non_ascii_ratio > 0.3 and cmd_bonus < 20:
                            penalty += 150
                        if 'é' in text or 'À' in text:
                            penalty += 50
                    
                    score = ratio * 100 + cmd_bonus + event_bonus + spanish_bonus + punct_bonus + jp_bonus - penalty
                if score > best_score:
                    best_score = score
                    best_enc = enc
                    best_cipher = c
            except:
                continue
    
    # Si el mejor fue latin-1 pero el score es bajo, forzar shift_jis o cp1252 según contexto
    if best_enc == "latin-1" and best_score < 70:
        # Probar shift_jis y cp1252 con el mismo cipher
        try:
            decrypted = decrypt_func(raw_data, best_cipher) if best_cipher != 0 else raw_data
            text_sjis = decrypted.decode('shift_jis', errors='replace')
            text_cp1252 = decrypted.decode('cp1252', errors='replace')
            # Elegir el que tenga menos caracteres de reemplazo y más comandos TSC
            score_sjis = text_sjis.count('�') * -10 + (30 if re.search(r'<[A-Z0-9+\-]+', text_sjis) else 0)
            score_cp1252 = text_cp1252.count('�') * -10 + (30 if re.search(r'<[A0-9+\-]+', text_cp1252) else 0)
            if score_sjis > score_cp1252 and score_sjis > -50:
                return "shift_jis", best_cipher
            elif score_cp1252 > -50:
                return "cp1252", best_cipher
        except:
            pass
    return best_enc, best_cipher

def ask_export_settings(parent, dark_theme, current_text=None, suggest_cipher=None):
    win = tk.Toplevel(parent)
    win.title("Exportar TSC - Configuración")
    win.geometry("550x350")
    win.transient(parent)
    win.grab_set()
    win.resizable(False, False)

    bg = "#1e1e1e" if dark_theme else "#ffffff"
    fg = "white" if dark_theme else "black"
    win.configure(bg=bg)

    tk.Label(win, text="Codificación:", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10,0))
    encoding_var = tk.StringVar(value="shift_jis")
    encodings = ["shift_jis", "cp1252", "cp932", "latin-1", "cp850"]
    enc_menu = ttk.Combobox(win, textvariable=encoding_var, values=encodings, state="readonly", width=30)
    enc_menu.pack(anchor=tk.W, padx=20, pady=5)

    tk.Label(win, text="Cifrado (0 = sin cifrado):", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10,0))
    cipher_var = tk.StringVar(value=str(suggest_cipher if suggest_cipher is not None else 0))
    cipher_entry = tk.Entry(win, textvariable=cipher_var, width=10, bg=bg, fg=fg, insertbackground=fg)
    cipher_entry.pack(anchor=tk.W, padx=20, pady=5)

    btn_frame = tk.Frame(win, bg=bg)
    btn_frame.pack(fill=tk.X, padx=20, pady=10)

    warn_label = tk.Label(btn_frame, text="", bg=bg, fg="orange")
    warn_label.pack(side=tk.LEFT, expand=True)

    def update_warning(*args):
        enc = encoding_var.get().lower()
        if enc in ("utf-8", "utf8"):
            warn_label.config(text="⚠️ UTF-8 no es recomendado para .tsc", fg="red")
        else:
            warn_label.config(text="✅ Codificación compatible", fg="lightgreen")
    encoding_var.trace_add('write', update_warning)
    update_warning()

    if current_text:
        def suggest():
            best_enc = None
            best_score = -1
            for enc in encodings:
                try:
                    encoded = current_text.encode(enc, errors='strict')
                    score = len(encoded)
                    if score > best_score:
                        best_score = score
                        best_enc = enc
                except UnicodeEncodeError:
                    encoded = current_text.encode(enc, errors='replace')
                    replacement_count = encoded.count(b'?') + encoded.count(b'\xef\xbf\xbd')
                    score = len(encoded) - replacement_count
                    if score > best_score:
                        best_score = score
                        best_enc = enc
            if best_enc:
                encoding_var.set(best_enc)
            else:
                messagebox.showinfo("Suggest", "No se pudo determinar una codificación adecuada.", parent=win)
            if suggest_cipher is not None:
                cipher_var.set(str(suggest_cipher))
                messagebox.showinfo("Suggest", f"Cifrado sugerido: {suggest_cipher}", parent=win)
        suggest_btn = tk.Button(btn_frame, text="Suggest", command=suggest,
                                bg="#3c3c3c" if dark_theme else "#e0e0e0",
                                fg="white" if dark_theme else "black")
        suggest_btn.pack(side=tk.RIGHT, padx=5)

    result = [None, None]

    def accept():
        enc = encoding_var.get()
        if enc.lower() in ("utf-8", "utf8"):
            if not messagebox.askyesno("Advertencia", "UTF-8 no es la codificación estándar para archivos .tsc. ¿Continuar de todos modos?", parent=win):
                return
        try:
            cipher = int(cipher_var.get().strip())
        except ValueError:
            cipher = 0
        result[0] = enc
        result[1] = cipher
        win.destroy()

    action_frame = tk.Frame(win, bg=bg)
    action_frame.pack(pady=20)
    btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark_theme else {"bg": "#e0e0e0", "fg": "black"}
    tk.Button(action_frame, text="Aceptar", command=accept, width=10, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(action_frame, text="Cancelar", command=win.destroy, width=10, **btn_style).pack(side=tk.LEFT, padx=10)

    win.wait_window()
    if result[0] is None:
        return None, None
    return result[0], result[1]
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
