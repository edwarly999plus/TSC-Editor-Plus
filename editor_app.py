# -*- coding: utf-8 -*-
"""
Main application class for TSC Editor+.
"""

import os
import sys
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel, Scale, Button, BooleanVar, ttk, simpledialog
from datetime import datetime

# Importaciones modulares
from .encryption import get_cipher_from_tsc, decrypt_tsc, encrypt_tsc
from .command_system import (
    load_base_commands, load_custom_commands, save_custom_commands,
    update_commands_data, build_command_regex, load_command_colors, save_command_colors,
    get_command_color as get_cmd_color
)
from .highlighted_tsc import highlight_current_file_in_list
from .settings_manager import load_settings, save_settings
from .syntax_highlight import check_syntax, highlight_syntax
from .dialogs import ask_encoding_and_cipher, smart_replace_dialog, auto_detect_best
from .ui_components import create_menubar, create_toolbar, create_context_menu, apply_theme_to_widgets
from .file_handling import load_tsc_file, save_tsc_file, load_project_file, save_project_file
from .search_replace import SearchReplaceManager
from .utils import detect_language, update_stats, add_history_entry, get_face_name
from .languages import LANGS
from .music_loader import get_music_name
from .sound_names import get_sound_name


# Librerías opcionales
try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False

try:
    from ttkthemes import ThemedTk
    TTKTHEMES_AVAILABLE = True
except ImportError:
    TTKTHEMES_AVAILABLE = False

try:
    import pywinstyles
    PYWINSTYLES_AVAILABLE = True
except ImportError:
    PYWINSTYLES_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class TSCEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("TSC Editor+")
        self.root.geometry("1300x700")

        # Idioma
        self.current_lang = detect_language()
        self.langs = LANGS
        self.tr = self.langs.get(self.current_lang, self.langs['en'])

        # Comandos
        self.base_commands_data = load_base_commands()
        self.custom_commands_file = os.path.join(os.path.dirname(sys.argv[0]), "custom_commands.json")
        self.custom_commands = load_custom_commands(self.custom_commands_file)
        self.commands_data = update_commands_data(self.base_commands_data, self.custom_commands)
        self.command_pattern = build_command_regex(self.commands_data)

        # Caras
        self.face_names = {
            "0000": "Nothing", "0001": "Sue Smile", "0002": "Sue Serious", "0003": "Sue Angry",
            "0004": "Sue Injured", "0005": "Balrog Serious", "0006": "Toroko", "0007": "King",
            "0008": "Toroko Scared", "0009": "Jack", "0010": "Kazuma", "0011": "Toroko Red",
            "0012": "Igor", "0013": "Jenka", "0014": "Balrog Happy!", "0015": "Misery",
            "0016": "Misery Happy!", "0017": "Booster Injured", "0018": "Booster", "0019": "Curly Smile",
            "0020": "Curly Sad", "0021": "The Doctor", "0022": "Momorin", "0023": "Balrog Injured",
            "0024": "A Random Surface Robot", "0025": "Curly Serious", "0026": "Misery Angry",
            "0027": "Human Sue? (Unused)", "0028": "Itoh", "0029": "Ballos", "0030": "Out Of Bounds!",
        }

        # Colores de comandos
        self.command_colors_file = os.path.join(os.path.dirname(sys.argv[0]), "command_colors.json")
        self.command_colors = load_command_colors(self.command_colors_file)

        # Configuración
        self.settings_file = os.path.join(os.path.dirname(sys.argv[0]), "settings.json")
        default_settings = {
            "auto_save": False,
            "language": self.current_lang,
            "show_history": True,
            "show_quick_docs": False,
            "default_font": "Courier New",
            "dark_theme": False,
            "load_mode": "ask",           # 'auto', 'ask', 'manual'
            "manual_encoding": "shift_jis",
            "manual_cipher": 0
        }
        self.settings = load_settings(self.settings_file, default_settings)
        if self.settings.get("language") != self.current_lang:
            self.current_lang = self.settings["language"]
            self.tr = self.langs.get(self.current_lang, self.langs['en'])

        # Tema
        self.available_themes = ["darkly", "vapor"]
        self.current_theme = tk.StringVar(value="darkly" if self.settings.get("dark_theme", False) else "vapor")

        # Fuentes
        import tkinter.font as tkfont
        system_fonts = set(tkfont.families())
        self.available_fonts = []
        script_dir = os.path.dirname(sys.argv[0])  # <-- Definir aquí para que esté disponible globalmente
        
        for f in ["Courier New", "Consolas", "Lucida Grande", "Cave Story"]:
            if f in system_fonts:
                self.available_fonts.append(f)
        if "Lucida Grande" not in self.available_fonts:
            for fname in ["Lucida Grande Regular.ttf", "LucidaGrande.ttf", "Lucida Grande.ttf"]:
                path = os.path.join(script_dir, fname)
                if os.path.isfile(path):
                    try:
                        tkfont.Font(font=fname, size=10)
                        self.available_fonts.append("Lucida Grande")
                    except:
                        self.available_fonts.append("Lucida Grande")
                    break
        # Buscar fuente Noto Sans JP
        for noto_file in ["NotoSansJP-Regular.ttf", "NotoSansJP.ttf", "NotoSansJP-Bold.ttf"]:
            path = os.path.join(script_dir, noto_file)
            if os.path.isfile(path):
                self.available_fonts.append("Noto Sans JP (Solo usar en TSC japoneses)")
                break
        if not self.available_fonts:
            self.available_fonts = ["Courier New", "Consolas"]
        for basic in ["Courier New", "Consolas"]:
            if basic not in self.available_fonts and basic in system_fonts:
                self.available_fonts.append(basic)
        self.current_font_name = tk.StringVar(value=self.settings.get("default_font", "Courier New"))
        self.base_font_size = 10

        # Construcción de la interfaz
        self._build_ui()

        # Estado del editor
        self.current_file = None
        self.doukutsu_path = None
        self.current_cipher = None
        self.current_encoding = "shift_jis"
        self.raw_bytes_for_hex = None
        self.history = []

        # Búsqueda
        self.search_manager = SearchReplaceManager(self)

        # Autoguardado
        self.auto_save_timer = None
        if self.settings["auto_save"]:
            self.start_auto_save()

        self.add_history_entry("Editor started")
        self.apply_theme()
        self.update_font()
        self.update_ui_language()

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Panel principal
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Barra lateral izquierda (lista de archivos)
        self.sidebar_frame = tk.Frame(self.main_paned, width=250, height=700)
        self.main_paned.add(self.sidebar_frame, minsize=180, width=250)
        files_tab = tk.Frame(self.sidebar_frame)
        files_tab.pack(fill=tk.BOTH, expand=True)

        search_frame = tk.Frame(files_tab)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        self.search_label = tk.Label(search_frame, text=self.tr['search_label'])
        self.search_label.pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *args: self.filter_files())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
        self.clear_btn = tk.Button(search_frame, text=self.tr['clear_btn'], command=self.clear_search)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.file_listbox = tk.Listbox(files_tab, bg="#f0f0f0", selectbackground="#0078D7")
        self.scrollbar_files = tk.Scrollbar(files_tab, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=self.scrollbar_files.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_files.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.bind("<Double-Button-1>", self.on_file_select)
        self.current_folder = None
        self.all_files = []

        # Área de texto
        self.text_area = scrolledtext.ScrolledText(
            self.main_paned, wrap=tk.WORD, undo=True, autoseparators=True, maxundo=50
        )
        self.main_paned.add(self.text_area, minsize=400)
        self.text_area.bind("<Control-MouseWheel>", self.on_ctrl_mousewheel)
        self.text_area.bind("<Control-Button-4>", lambda e: self.change_font_size(1))
        self.text_area.bind("<Control-Button-5>", lambda e: self.change_font_size(-1))
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<<Paste>>", self.on_paste)
        self.text_area.bind("<ButtonRelease-1>", self.on_cursor_move)
        self.text_area.bind("<Control-x>", self.on_cut)
        self.text_area.bind("<Control-c>", self.on_copy)

        # Panel derecho (notebook)
        self.right_notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.right_notebook, minsize=250, width=250)

        # Pestaña de historial
        self.history_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.history_tab, text=self.tr['history'])
        self.history_label = tk.Label(self.history_tab, text=self.tr['history'], font=("Segoe UI", 10, "bold"))
        self.history_label.pack(pady=5)
        self.history_listbox = tk.Listbox(self.history_tab, bg="#f0f0f0", selectbackground="#0078D7")
        self.history_scrollbar = tk.Scrollbar(self.history_tab, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pestaña de documentación rápida
        self.docs_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.docs_tab, text=self.tr['quick_docs'])
        docs_paned = tk.PanedWindow(self.docs_tab, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        docs_paned.pack(fill=tk.BOTH, expand=True)

        search_docs_frame = tk.Frame(self.docs_tab)
        search_docs_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(search_docs_frame, text=self.tr['search_docs']).pack(side=tk.LEFT)
        self.docs_search_var = tk.StringVar()
        self.docs_search_var.trace_add('write', lambda *args: self.filter_quick_docs())
        docs_search_entry = tk.Entry(search_docs_frame, textvariable=self.docs_search_var)
        docs_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))

        top_frame = tk.Frame(docs_paned)
        docs_paned.add(top_frame, minsize=150)
        self.docs_listbox = tk.Listbox(top_frame, bg="#f0f0f0", selectbackground="#0078D7")
        self.scrollbar_docs = tk.Scrollbar(top_frame, orient=tk.VERTICAL, command=self.docs_listbox.yview)
        self.docs_listbox.config(yscrollcommand=self.scrollbar_docs.set)
        self.docs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_docs.pack(side=tk.RIGHT, fill=tk.Y)
        self.docs_listbox.bind("<<ListboxSelect>>", self.on_doc_select)

        bottom_frame = tk.Frame(docs_paned)
        docs_paned.add(bottom_frame, minsize=150)
        self.docs_detail = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, font=("Segoe UI", 9), state=tk.NORMAL)
        self.docs_detail.pack(fill=tk.BOTH, expand=True)
        self.populate_quick_docs()

        # Pestaña de búsqueda
        self.search_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.search_tab, text=self.tr['search_tab'])
        self._create_search_widgets()

        # Menú contextual
        self.context_menu = create_context_menu(self, self.text_area)

        # Barra de estado
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text=self.tr['status_ready'], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stats_label = tk.Label(self.status_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        self.stats_label.pack(side=tk.RIGHT)

        # Barra de herramientas
        self.toolbar_frame, self.theme_btn = create_toolbar(self)

        # Menú principal
        self.menubar = create_menubar(self)

        # Atajos de teclado
        self._bind_shortcuts()

    def _create_search_widgets(self):
        main_frame = tk.Frame(self.search_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(main_frame, text=self.tr['search_term']).pack(anchor=tk.W)
        self.search_entry = tk.Entry(main_frame, width=30)
        self.search_entry.pack(fill=tk.X, pady=(0,5))
        self.search_entry.bind("<KeyRelease>", self.on_search_text_change)

        self.case_var = BooleanVar(value=False)
        self.whole_var = BooleanVar(value=False)
        tk.Checkbutton(main_frame, text=self.tr['case_sensitive'], variable=self.case_var, command=self.refresh_search_highlight).pack(anchor=tk.W)
        tk.Checkbutton(main_frame, text=self.tr['whole_word'], variable=self.whole_var, command=self.refresh_search_highlight).pack(anchor=tk.W)

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text=self.tr['find_next'], command=self.find_next).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text=self.tr['find_prev'], command=self.find_prev).pack(side=tk.LEFT, padx=2)

        tk.Label(main_frame, text=self.tr['replace_term']).pack(anchor=tk.W, pady=(5,0))
        self.replace_entry = tk.Entry(main_frame, width=30)
        self.replace_entry.pack(fill=tk.X, pady=(0,5))

        rep_frame = tk.Frame(main_frame)
        rep_frame.pack(fill=tk.X)
        tk.Button(rep_frame, text=self.tr['replace'], command=self.replace_current).pack(side=tk.LEFT, padx=2)
        tk.Button(rep_frame, text=self.tr['replace_all'], command=self.replace_all).pack(side=tk.LEFT, padx=2)

        self.search_status = tk.Label(main_frame, text="", fg="gray")
        self.search_status.pack(pady=5)

    def _bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.load_file())
        self.root.bind("<Control-s>", lambda e: self.save_project())
        self.root.bind("<Control-Shift-S>", lambda e: self.export_file())
        self.root.bind("<Control-z>", lambda e: self.undo_action())
        self.root.bind("<Control-y>", lambda e: self.redo_action())
        self.root.bind("<Control-f>", lambda e: self.focus_search_tab())
        self.root.bind("<Control-r>", lambda e: self.smart_replace_special_chars())
        self.root.bind("<Control-k>", lambda e: self.open_settings())
        self.root.bind("<F5>", lambda e: self.test_game())
        self.root.bind("<Alt-F4>", lambda e: self.root.quit())
        self.root.bind("<Control-Shift-O>", lambda e: self.load_project())
        self.root.bind("<Control-Shift-Alt-O>", lambda e: self.load_folder())
        self.root.bind("<Control-Delete>", lambda e: self.delete_current_from_list())
        self.root.bind("<Control-Shift-Delete>", lambda e: self.delete_all_from_list())
        self.root.bind("<Control-h>", lambda e: self.focus_history_tab())
        self.root.bind("<Control-Shift-C>", lambda e: self.open_custom_command_syntax_window())

    # ------------------------------------------------------------------
    # Métodos de carga/guardado de archivos
    # ------------------------------------------------------------------
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title=self.tr['open_tsc'],
            filetypes=[("TSC Files", "*.tsc"), ("Plain text", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
        self.load_specific_tsc(file_path)

    def load_specific_tsc(self, file_path):
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
            self.raw_bytes_for_hex = raw_data

            mode = self.settings.get("load_mode", "ask")
            
            if mode == "auto":
                # Auto-detect without dialog
                encoding, cipher = auto_detect_best(raw_data, get_cipher_from_tsc, decrypt_tsc)
                if encoding is None:
                    encoding = "shift_jis"
                    cipher = 0
            elif mode == "manual":
                encoding = self.settings.get("manual_encoding", "shift_jis")
                cipher = self.settings.get("manual_cipher", 0)
            else:  # 'ask'
                encoding, cipher = ask_encoding_and_cipher(
                    self.root, raw_data, self.settings.get("dark_theme", False),
                    get_cipher_from_tsc, decrypt_tsc
                )
                if encoding is None:  # user cancelled
                    return
            
            # Decrypt and decode
            decrypted = decrypt_tsc(raw_data, cipher) if cipher != 0 else raw_data
            text = decrypted.decode(encoding, errors="replace")
            self.load_text_to_editor(text, file_path, cipher, encoding)
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)} | Cipher={cipher}, Enc={encoding}")
            self.add_history_entry(f"Opened TSC: {os.path.basename(file_path)} (cipher={cipher}, enc={encoding})")
        except Exception as e:
            messagebox.showerror(self.tr['load_error'], f"Could not load {os.path.basename(file_path)}:\n{str(e)}")

    def load_text_to_editor(self, text, file_path, cipher, encoding):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text)
        self.text_area.edit_reset()
        self.current_file = file_path
        self.current_cipher = cipher
        self.current_encoding = encoding
        self.delayed_highlight()
        self.update_stats()

    def export_file(self):
        if not self.confirm_save_with_errors():
            return
        text_to_save = self.text_area.get("1.0", tk.END)
        if not text_to_save.strip():
            if not messagebox.askyesno(self.tr['empty_warning'], self.tr['empty_warning']):
                return
        if self.current_file and messagebox.askyesno(self.tr['overwrite_msg'], f"{self.tr['overwrite_question']} '{os.path.basename(self.current_file)}'?"):
            save_path = self.current_file
        else:
            save_path = filedialog.asksaveasfilename(
                title=self.tr['export_tsc_dialog_title'],
                defaultextension=".tsc",
                filetypes=[("TSC Files", "*.tsc"), ("Plain text", "*.txt"), ("All files", "*.*")]
            )
            if not save_path:
                return
        cipher = self.current_cipher if self.current_cipher is not None else 0
        success = save_tsc_file(save_path, text_to_save, cipher, self.current_encoding,
                                encrypt_tsc, lambda l: l // 2)
        if success:
            self.current_file = save_path
            self.status_label.config(text=f"Exported: {os.path.basename(save_path)} | Cipher: {cipher}")
            self.add_history_entry(f"Saved TSC: {os.path.basename(save_path)}")
            messagebox.showinfo(self.tr['export_success'], f"{self.tr['export_success']}\nCipher: {cipher}")
        else:
            messagebox.showerror(self.tr['save_error'], self.tr['save_error'])

    def save_project(self):
        if not self.confirm_save_with_errors():
            return
        text_to_save = self.text_area.get("1.0", tk.END)
        if not text_to_save.strip():
            if not messagebox.askyesno(self.tr['empty_warning'], self.tr['empty_warning']):
                return
        if self.current_file and self.current_file.endswith(".cstsc") and messagebox.askyesno(self.tr['overwrite_msg'], f"{self.tr['overwrite_question']} '{os.path.basename(self.current_file)}'?"):
            save_path = self.current_file
        else:
            save_path = filedialog.asksaveasfilename(
                title=self.tr['save_project_dialog_title'],
                defaultextension=".cstsc",
                filetypes=[("TSC Editor+ Project", "*.cstsc"), ("Text", "*.txt"), ("All", "*.*")]
            )
            if not save_path:
                return
        success = save_project_file(save_path, text_to_save)
        if success:
            self.current_file = save_path
            self.status_label.config(text=f"Project saved: {os.path.basename(save_path)}")
            self.add_history_entry(f"Saved project: {os.path.basename(save_path)}")
            messagebox.showinfo(self.tr['project_saved'], self.tr['project_saved'])
        else:
            messagebox.showerror(self.tr['save_error'], self.tr['save_error'])

    def load_project(self):
        file_path = filedialog.askopenfilename(
            title=self.tr['open_project_dialog_title'],
            filetypes=[("TSC Editor+ Project", "*.cstsc"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if not file_path:
            return
        text, success = load_project_file(file_path)
        if success:
            self.load_text_to_editor(text, file_path, None, "utf-8")
            self.status_label.config(text=f"Project loaded: {os.path.basename(file_path)}")
            self.add_history_entry(f"Opened project: {os.path.basename(file_path)}")
        else:
            messagebox.showerror(self.tr['load_error'], f"{self.tr['load_error']}:\n{file_path}")

    def refresh_current_file(self):
        if self.current_file and os.path.isfile(self.current_file):
            if self.current_file.endswith(".cstsc"):
                self.load_project()
            else:
                self.load_specific_tsc(self.current_file)

    def confirm_save_with_errors(self):
        texto = self.text_area.get("1.0", tk.END)
        errors = check_syntax(texto, self.commands_data, self.command_pattern)
        if errors:
            return messagebox.askyesno(self.tr['syntax_errors'], self.tr['syntax_errors_found'])
        return True

    # ------------------------------------------------------------------
    # Lista lateral de archivos
    # ------------------------------------------------------------------
    def load_folder(self):
        folder = filedialog.askdirectory(title=self.tr['load_folder_title'])
        if not folder:
            return
        self.current_folder = folder
        self.refresh_file_list()
        self.search_var.set("")
        self.filter_files()

    def refresh_file_list(self):
        self.all_files = []
        if not self.current_folder:
            return
        for root_dir, dirs, files in os.walk(self.current_folder):
            for file in files:
                if file.lower().endswith(".tsc"):
                    rel_path = os.path.relpath(os.path.join(root_dir, file), self.current_folder)
                    full_path = os.path.join(root_dir, file)
                    self.all_files.append((rel_path, full_path))
        self.all_files.sort(key=lambda x: x[0].lower())
        self.filter_files()

    def filter_files(self):
        search_text = self.search_var.get().strip().lower()
        self.file_listbox.delete(0, tk.END)
        self.file_listbox._paths = {}
        for rel_path, full_path in self.all_files:
            filename = os.path.basename(rel_path)
            name_no_ext = os.path.splitext(filename)[0].lower()
            if search_text == "" or search_text in name_no_ext:
                self.file_listbox.insert(tk.END, rel_path)
                self.file_listbox._paths[rel_path] = full_path

    def clear_search(self):
        self.search_var.set("")
        self.filter_files()

    def on_file_select(self, event):
        selection = self.file_listbox.curselection()
        if not selection:
            return
        rel_path = self.file_listbox.get(selection[0])
        full_path = getattr(self.file_listbox, '_paths', {}).get(rel_path)
        if full_path and os.path.isfile(full_path):
            self.load_specific_tsc(full_path)

    def delete_current_from_list(self):
        if not self.current_file:
            messagebox.showinfo("Info", "There is no file loaded.")
            return
        self.all_files = [(r, f) for r, f in self.all_files if f != self.current_file]
        self.filter_files()
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.current_cipher = None
        self.status_label.config(text="File removed from list.")
        self.add_history_entry("Removed current file from list")

    def delete_all_from_list(self):
        if not self.all_files:
            messagebox.showinfo("Info", "There are no files in the list.")
            return
        if messagebox.askyesno("Confirm", "Delete ALL files from the sidebar list?\n(They will NOT be deleted from the disk)"):
            self.all_files = []
            self.filter_files()
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            self.current_cipher = None
            self.status_label.config(text="List Cleared.")
            self.add_history_entry("Cleared all files from list")

    # ------------------------------------------------------------------
    # Documentación rápida
    # ------------------------------------------------------------------
    def populate_quick_docs(self):
        self.all_docs_commands = sorted(self.commands_data.keys())
        self.filter_quick_docs()

    def filter_quick_docs(self):
        search_text = self.docs_search_var.get().strip().lower()
        self.docs_listbox.delete(0, tk.END)
        for cmd in self.all_docs_commands:
            if search_text == "" or search_text in cmd.lower():
                self.docs_listbox.insert(tk.END, cmd)

    def on_doc_select(self, event):
        selection = self.docs_listbox.curselection()
        if not selection:
            return
        cmd = self.docs_listbox.get(selection[0])
        if cmd in self.commands_data:
            num_args, types, desc = self.commands_data[cmd]
            if num_args == "0":
                syntax = f"<{cmd}>"
            else:
                arg_list = []
                for i in range(int(num_args)):
                    arg_char = types[i] if i < len(types) else "?"
                    arg_list.append(f"<{arg_char}>")
                syntax = f"<{cmd} " + " ".join(arg_list) + ">"
            extra = ""
            if cmd == "FAC":
                extra = f"\n{self.tr['face_name']}: {self.face_names.get('0000', '?')}"
            elif cmd == "CMU":
                extra = f"\n{self.tr['music_name']}: Check music ID list"
            info = f"{self.tr['command']}: {cmd}\n\n{self.tr['syntax']}: {syntax}\n\n{self.tr['description']}: {desc}\n"
            if extra:
                info += f"\n{self.tr['details']}:{extra}"
            self.docs_detail.config(state=tk.NORMAL)
            self.docs_detail.delete(1.0, tk.END)
            self.docs_detail.insert(tk.END, info)
            self.docs_detail.config(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Comandos personalizados
    # ------------------------------------------------------------------
    def edit_custom_commands(self):
        win = Toplevel(self.root)
        win.title(self.tr['edit_custom_cmds_title'])
        win.geometry("700x500")
        win.transient(self.root)
        win.grab_set()
        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        win.configure(bg=bg)

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame.configure(bg=bg)

        columns = ("name", "args", "desc")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("name", text="Command")
        tree.heading("args", text="Args")
        tree.heading("desc", text="Description")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        for cmd, data in self.custom_commands.items():
            tree.insert("", tk.END, values=(cmd, data[0], data[2]))

        btn_frame = tk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        btn_frame.configure(bg=bg)

        btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark else {"bg": "#f0f0f0", "fg": "black"}

        def add_cmd():
            name = simpledialog.askstring("Add Command", self.tr['custom_cmd_name'], parent=win)
            if not name or len(name) < 2 or len(name) > 3:
                messagebox.showerror("Error", "Command name must be 2-3 letters.", parent=win)
                return
            name = name.upper()
            if name in self.commands_data:
                messagebox.showerror("Error", "Command already exists.", parent=win)
                return
            args = simpledialog.askinteger("Arguments", self.tr['custom_cmd_args'], minvalue=0, maxvalue=4, parent=win)
            if args is None:
                return
            desc = simpledialog.askstring("Description", self.tr['custom_cmd_desc'], parent=win)
            if desc is None:
                desc = ""
            self.custom_commands[name] = [str(args), "----", desc]
            save_custom_commands(self.custom_commands_file, self.custom_commands)
            self.commands_data = update_commands_data(self.base_commands_data, self.custom_commands)
            self.command_pattern = build_command_regex(self.commands_data)
            self.populate_quick_docs()
            tree.insert("", tk.END, values=(name, args, desc))
            self.refresh_current_file()

        def edit_cmd():
            selected = tree.selection()
            if not selected:
                return
            name = tree.item(selected[0])['values'][0]
            if name not in self.custom_commands:
                return
            current_args, _, current_desc = self.custom_commands[name]
            new_args = simpledialog.askinteger("Arguments", self.tr['custom_cmd_args'], initialvalue=int(current_args), minvalue=0, maxvalue=4, parent=win)
            if new_args is None:
                return
            new_desc = simpledialog.askstring("Description", self.tr['custom_cmd_desc'], initialvalue=current_desc, parent=win)
            if new_desc is None:
                return
            self.custom_commands[name] = [str(new_args), "----", new_desc]
            save_custom_commands(self.custom_commands_file, self.custom_commands)
            self.commands_data = update_commands_data(self.base_commands_data, self.custom_commands)
            self.command_pattern = build_command_regex(self.commands_data)
            self.populate_quick_docs()
            tree.item(selected[0], values=(name, new_args, new_desc))
            self.refresh_current_file()

        def remove_cmd():
            selected = tree.selection()
            if not selected:
                return
            name = tree.item(selected[0])['values'][0]
            if name in self.custom_commands:
                del self.custom_commands[name]
                save_custom_commands(self.custom_commands_file, self.custom_commands)
                self.commands_data = update_commands_data(self.base_commands_data, self.custom_commands)
                self.command_pattern = build_command_regex(self.commands_data)
                self.populate_quick_docs()
                tree.delete(selected[0])
                self.refresh_current_file()

        tk.Button(btn_frame, text="Add", command=add_cmd, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit", command=edit_cmd, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove", command=remove_cmd, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['close_btn'], command=win.destroy, **btn_style).pack(side=tk.RIGHT, padx=5)

    # ------------------------------------------------------------------
    # Ventana de análisis de sintaxis de comandos
    # ------------------------------------------------------------------
    def open_custom_command_syntax_window(self):
        win = tk.Toplevel(self.root)
        win.title(self.tr['cmd_syntax_window_title'])
        win.geometry("700x500")
        win.transient(self.root)
        win.grab_set()

        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        win.configure(bg=bg)

        force_error = tk.BooleanVar(value=False)

        main_frame = tk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_frame.configure(bg=bg)

        tk.Label(main_frame, text=self.tr['cmd_input_label'], anchor=tk.W, bg=bg, fg=fg).pack(fill=tk.X)
        input_entry = tk.Entry(main_frame, font=("Courier New", 10), bg=bg, fg=fg, insertbackground=fg)
        input_entry.pack(fill=tk.X, pady=(5, 10))
        input_entry.insert(0, "<CMU0000")

        error_cb = tk.Checkbutton(main_frame, text=self.tr['syntax_error_purpose'], variable=force_error, bg=bg, fg=fg, selectcolor=bg)
        error_cb.pack(anchor=tk.W, pady=5)

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        btn_frame.configure(bg=bg)

        btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark else {"bg": "#f0f0f0", "fg": "black"}

        result_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, font=("Courier New", 10), bg=bg, fg=fg, insertbackground=fg)
        result_text.pack(fill=tk.BOTH, expand=True, pady=5)

        def analyze():
            line = input_entry.get().strip()
            result_text.delete(1.0, tk.END)
            if not line:
                result_text.insert(tk.END, "⚠️ " + self.tr['cmd_not_found'])
                return
            if force_error.get():
                result_text.insert(tk.END, "🔴 " + self.tr['error_type'] + ": ", "error")
                result_text.insert(tk.END, self.tr['syntax_error_purpose'] + "\n", "error")
                result_text.insert(tk.END, line, "error")
                return
            match = self.command_pattern.match(line)
            if not match:
                if re.fullmatch(r'\d{4}', line):
                    result_text.insert(tk.END, "🔵 " + self.tr['id_type'] + ": ", "command")
                    result_text.insert(tk.END, line + "\n", "id")
                    result_text.insert(tk.END, self.tr['id_header'] + ": " + line)
                else:
                    result_text.insert(tk.END, "🔴 " + self.tr['error_type'] + ": ", "error")
                    result_text.insert(tk.END, self.tr['unknown_command'] + "\n", "error")
                    result_text.insert(tk.END, line, "error")
                return
            cmd_name = match.group(1)
            if cmd_name not in self.commands_data:
                result_text.insert(tk.END, "🔴 " + self.tr['error_type'] + ": ", "error")
                result_text.insert(tk.END, self.tr['unknown_command'] + f" '{cmd_name}'\n", "error")
                result_text.insert(tk.END, line, "error")
                return
            num_args, types, desc = self.commands_data[cmd_name]
            num_args = int(num_args)
            after_cmd = line[match.end():]
            arg_matches = re.findall(r':?(\d{4})', after_cmd)
            args = arg_matches[:num_args]
            custom_color = get_cmd_color(self.command_colors, cmd_name)
            result_text.insert(tk.END, "🔵 " + self.tr['command_type'] + ": ", "command")
            if custom_color == "pink":
                result_text.insert(tk.END, f"<{cmd_name} ", "id")
            elif custom_color == "red":
                result_text.insert(tk.END, f"<{cmd_name} ", "error")
            else:
                result_text.insert(tk.END, f"<{cmd_name} ", "command")
            result_text.insert(tk.END, "\n" + "🩷 " + self.tr['id_type'] + "s: ", "id")
            if num_args == 0:
                result_text.insert(tk.END, "ninguno\n", "id")
            else:
                for idx, arg in enumerate(args):
                    if arg and len(arg) == 4 and arg.isdigit():
                        result_text.insert(tk.END, f"{arg} ", "id")
                    else:
                        result_text.insert(tk.END, f"[{arg if arg else '???'}] ", "error")
                result_text.insert(tk.END, "\n")
                if len(args) < num_args:
                    result_text.insert(tk.END, "🔴 " + self.tr['error_type'] + ": ", "error")
                    result_text.insert(tk.END, self.tr['missing_param'] + f" (se esperaban {num_args})\n", "error")
                elif len(args) > num_args:
                    result_text.insert(tk.END, "🔴 " + self.tr['error_type'] + ": ", "error")
                    result_text.insert(tk.END, self.tr['extra_text'] + f" (se esperaban {num_args})\n", "error")
            result_text.insert(tk.END, "\n📖 " + self.tr['description'] + ": ", "bold")
            result_text.insert(tk.END, desc + "\n")
            result_text.insert(tk.END, "\n" + "─" * 50 + "\n")
            result_text.insert(tk.END, "📝 " + self.tr['cmd_input_label'] + " ", "bold")
            result_text.insert(tk.END, line + "\n")
            errors = check_syntax(line + "\n", self.commands_data, self.command_pattern)
            if errors:
                result_text.insert(tk.END, "\n🔴 " + self.tr['syntax_errors'] + ":\n", "error")
                for err in errors:
                    result_text.insert(tk.END, f"  • {err['message']}\n", "error")
            else:
                result_text.insert(tk.END, "\n✅ " + self.tr['syntax_no_errors'] + "\n")

        def clear():
            result_text.delete(1.0, tk.END)

        tk.Button(btn_frame, text=self.tr['parse_button'], command=analyze, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['clear_button'], command=clear, **btn_style).pack(side=tk.LEFT, padx=5)

        # Configurar colores de etiquetas
        if dark:
            result_text.tag_configure("command", foreground="#88AAFF")
            result_text.tag_configure("id", foreground="#FF88BB")
            result_text.tag_configure("error", foreground="#FF6666")
            result_text.tag_configure("bold", font=("Courier New", 10, "bold"))
        else:
            result_text.tag_configure("command", foreground="#0000FF")
            result_text.tag_configure("id", foreground="#C7158C")
            result_text.tag_configure("error", foreground="#FF0000")
            result_text.tag_configure("bold", font=("Courier New", 10, "bold"))

        analyze()

    # ------------------------------------------------------------------
    # Configuración y tema
    # ------------------------------------------------------------------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title(self.tr['settings_window_title'])
        win.geometry("500x550")
        win.transient(self.root)
        win.grab_set()

        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        win.configure(bg=bg)

        # Auto-save
        auto_var = BooleanVar(value=self.settings["auto_save"])
        def toggle_auto():
            self.settings["auto_save"] = auto_var.get()
            if self.settings["auto_save"]:
                self.start_auto_save()
            else:
                self.stop_auto_save()
            save_settings(self.settings_file, self.settings)
        tk.Checkbutton(win, text=self.tr['auto_save_label'], variable=auto_var, command=toggle_auto, bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=5)

        # Dark theme
        dark_var = BooleanVar(value=self.settings["dark_theme"])
        def toggle_dark():
            self.settings["dark_theme"] = dark_var.get()
            self.current_theme.set("darkly" if dark_var.get() else "vapor")
            self.apply_theme()
            save_settings(self.settings_file, self.settings)
            win.destroy()
            self.open_settings()
        tk.Checkbutton(win, text=self.tr['dark_theme_label'], variable=dark_var, command=toggle_dark, bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=5)

        # Language
        tk.Label(win, text=self.tr['language_label'], bg=bg, fg=fg).pack(anchor=tk.W, padx=20, pady=(10,0))
        lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.Combobox(win, textvariable=lang_var, values=['en', 'es', 'jp'], state="readonly")
        lang_menu.pack(anchor=tk.W, padx=20, pady=5)

        # Default font
        tk.Label(win, text=self.tr['default_font_label'], bg=bg, fg=fg).pack(anchor=tk.W, padx=20, pady=(10,0))
        font_var = tk.StringVar(value=self.current_font_name.get())
        font_menu = ttk.Combobox(win, textvariable=font_var, values=self.available_fonts, state="readonly")
        font_menu.pack(anchor=tk.W, padx=20, pady=5)

        # ---- Load mode settings ----
        tk.Label(win, text="TSC file loading mode:", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10,0))
        load_mode_var = tk.StringVar(value=self.settings.get("load_mode", "ask"))

        def on_load_mode_change(*args):
            mode = load_mode_var.get()
            if mode == "manual":
                manual_frame.pack(anchor=tk.W, padx=40, pady=5)
            else:
                manual_frame.pack_forget()

        tk.Radiobutton(win, text="Always auto-detect", variable=load_mode_var, value="auto", bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(win, text="Always ask per file", variable=load_mode_var, value="ask", bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(win, text="Always use this encoding and cipher", variable=load_mode_var, value="manual", bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)

        manual_frame = tk.Frame(win, bg=bg)
        tk.Label(manual_frame, text="Encoding:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)
        manual_encoding_var = tk.StringVar(value=self.settings.get("manual_encoding", "shift_jis"))
        encodings = ["shift_jis", "cp932", "latin-1", "utf-8", "cp850"]
        manual_encoding_menu = ttk.Combobox(manual_frame, textvariable=manual_encoding_var, values=encodings, state="readonly", width=10)
        manual_encoding_menu.pack(side=tk.LEFT, padx=5)
        tk.Label(manual_frame, text="Cipher:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)
        manual_cipher_var = tk.StringVar(value=str(self.settings.get("manual_cipher", 0)))
        manual_cipher_entry = tk.Entry(manual_frame, textvariable=manual_cipher_var, width=6)
        manual_cipher_entry.pack(side=tk.LEFT, padx=5)

        if load_mode_var.get() != "manual":
            manual_frame.pack_forget()
        else:
            manual_frame.pack(anchor=tk.W, padx=40, pady=5)

        load_mode_var.trace_add('write', on_load_mode_change)

        # Buttons
        btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark else {"bg": "#e0e0e0", "fg": "black"}

        def apply_settings():
            if lang_var.get() != self.current_lang:
                self.current_lang = lang_var.get()
                self.settings["language"] = self.current_lang
                self.update_ui_language()
            self.settings["default_font"] = font_var.get()
            self.current_font_name.set(font_var.get())
            self.update_font()
            self.settings["load_mode"] = load_mode_var.get()
            self.settings["manual_encoding"] = manual_encoding_var.get()
            try:
                self.settings["manual_cipher"] = int(manual_cipher_var.get())
            except:
                self.settings["manual_cipher"] = 0
            save_settings(self.settings_file, self.settings)
            win.destroy()

        tk.Button(win, text=self.tr['apply_btn'], command=apply_settings, **btn_style).pack(pady=20)
        tk.Button(win, text=self.tr['close_btn'], command=win.destroy, **btn_style).pack(pady=5)

    def apply_theme(self):
        if TTKBOOTSTRAP_AVAILABLE:
            try:
                self.root.style.theme_use(self.current_theme.get())
            except:
                pass
        elif TTKTHEMES_AVAILABLE:
            if self.settings.get("dark_theme", False):
                try:
                    self.root.set_theme("equilux")
                except:
                    pass
            else:
                try:
                    self.root.set_theme("clam")
                except:
                    pass
        apply_theme_to_widgets(self, self.settings.get("dark_theme", False))
        self.update_theme_button_text()
        if PYWINSTYLES_AVAILABLE and sys.platform == "win32":
            try:
                if self.settings.get("dark_theme", False):
                    pywinstyles.change_header_color(self.root, "#1e1e1e")
                else:
                    pywinstyles.change_header_color(self.root, "#ffffff")
            except:
                pass

    def toggle_theme(self):
        current = self.current_theme.get()
        new_theme = "vapor" if current == "darkly" else "darkly"
        self.current_theme.set(new_theme)
        self.settings["dark_theme"] = (new_theme == "darkly")
        save_settings(self.settings_file, self.settings)
        self.apply_theme()
        self.add_history_entry(f"Changed theme to {new_theme}")

    def update_theme_button_text(self):
        if hasattr(self, 'theme_btn'):
            if self.current_theme.get() == "darkly":
                self.theme_btn.config(text="🌙 Darkly")
            else:
                self.theme_btn.config(text="☀️ Vapor")

    def start_auto_save(self):
        if self.auto_save_timer:
            self.root.after_cancel(self.auto_save_timer)
        self.schedule_auto_save()

    def schedule_auto_save(self):
        if self.settings["auto_save"] and self.current_file and self.current_file.endswith(".cstsc"):
            self.save_project()
            self.status_label.config(text=self.tr['auto_save_notification'])
            self.root.after(3000, lambda: self.status_label.config(text=self.tr['status_ready']))
        self.auto_save_timer = self.root.after(360000, self.schedule_auto_save)

    def stop_auto_save(self):
        if self.auto_save_timer:
            self.root.after_cancel(self.auto_save_timer)
            self.auto_save_timer = None

    # ------------------------------------------------------------------
    # Sintaxis y resaltado
    # ------------------------------------------------------------------
    def check_syntax_cmd(self):
        texto = self.text_area.get("1.0", tk.END)
        errors = check_syntax(texto, self.commands_data, self.command_pattern)
        if errors:
            msg = f"{self.tr['syntax_errors']}:\n\n"
            for err in errors:
                msg += f"- {err['message']}\n"
            messagebox.showwarning(self.tr['syntax_error_window_title'], msg)
        else:
            messagebox.showinfo(self.tr['syntax_error_window_title'], self.tr['syntax_no_errors'])

    def highlight_syntax(self):
        highlight_syntax(self.text_area, self.commands_data, self.command_pattern, self.command_colors)

    def delayed_highlight(self):
        self.root.after(50, self.highlight_syntax)

    # ------------------------------------------------------------------
    # Búsqueda y reemplazo (delegado)
    # ------------------------------------------------------------------
    def on_search_text_change(self, event=None):
        self.search_manager.search_text = self.search_entry.get()
        self.search_manager.search_case = self.case_var.get()
        self.search_manager.search_whole = self.whole_var.get()
        self.search_manager.refresh_highlight()

    def refresh_search_highlight(self):
        self.search_manager.refresh_highlight()

    def find_next(self):
        self.search_manager.find_next()

    def find_prev(self):
        self.search_manager.find_prev()

    def replace_current(self):
        self.search_manager.replace_current(self.replace_entry.get())

    def replace_all(self):
        self.search_manager.replace_all(self.replace_entry.get())

    def focus_search_tab(self, event=None):
        self.right_notebook.select(self.search_tab)
        self.search_entry.focus_set()

    def focus_history_tab(self):
        self.right_notebook.select(self.history_tab)

    # ------------------------------------------------------------------
    # Edición básica
    # ------------------------------------------------------------------
    def undo_action(self):
        try:
            self.text_area.edit_undo()
            self.add_history_entry("Undo")
        except:
            pass

    def redo_action(self):
        try:
            self.text_area.edit_redo()
            self.add_history_entry("Redo")
        except:
            pass

    def copy_text(self):
        try:
            self.text_area.event_generate("<<Copy>>")
            self.add_history_entry("Copied")
        except:
            pass

    def paste_text(self):
        try:
            self.text_area.event_generate("<<Paste>>")
            self.add_history_entry("Pasted")
        except:
            pass

    def cut_text(self):
        try:
            self.text_area.event_generate("<<Cut>>")
            self.add_history_entry("Cut")
        except:
            pass

    def on_paste(self, event=None):
        self.root.after(10, lambda: self.add_history_entry("Pasted"))
        self.update_stats()

    def on_cut(self, event=None):
        self.root.after(10, lambda: self.add_history_entry("Cut"))
        self.update_stats()

    def on_copy(self, event=None):
        self.add_history_entry("Copied")

    def on_backspace(self, event=None):
        self.add_history_entry("Backspace")
        self.update_stats()

    def on_enter(self, event=None):
        self.add_history_entry("Enter")
        self.update_stats()

    def on_space(self, event=None):
        self.add_history_entry("Space")
        self.update_stats()

    def on_text_change(self, event=None):
        self.delayed_highlight()
        self.update_stats()
        if self.settings["auto_save"] and self.current_file and self.current_file.endswith(".cstsc"):
            self.save_project()
        if event and event.char and event.char.isprintable():
            self.add_history_entry("Handwrite")

    def on_cursor_move(self, event=None):
        self.update_stats()

    def update_stats(self):
        update_stats(self)

    def add_history_entry(self, action):
        add_history_entry(self, action)

    # ------------------------------------------------------------------
    # Conteo de caracteres
    # ------------------------------------------------------------------
    def count_characters_normal(self):
        self._count_characters(with_face=False)

    def count_characters_face(self):
        self._count_characters(with_face=True)

    def _count_characters(self, with_face):
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showinfo(self.tr['count_normal_title'], "No text selected.")
            return
        if not selected.strip():
            messagebox.showinfo(self.tr['count_normal_title'], "Selected text is empty.")
            return
        clean_text = re.sub(r'<[^>]+>', '', selected)
        clean_text = re.sub(r'#[0-9]{4}\b', '', clean_text)
        char_count = len(clean_text)
        limit = 27 if with_face else 34
        if char_count <= limit:
            msg = f"{self.tr['fits']} ({self.tr['limit']}: {limit})"
        else:
            msg = f"{self.tr['not_fits']} ({self.tr['limit']}: {limit})"
        title = self.tr['count_face_title'] if with_face else self.tr['count_normal_title']
        messagebox.showinfo(title, f"{msg}\n\nCharacters: {char_count}\nLimit: {limit}")

    # ------------------------------------------------------------------
    # Fuentes
    # ------------------------------------------------------------------
    def update_font(self):
        font_name = self.current_font_name.get()
        self.text_area.config(font=(font_name, self.base_font_size))
        self.text_area.tag_configure("evento", font=(font_name, self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_letras", font=(font_name, self.base_font_size, "bold"))
        self.delayed_highlight()

    def change_font_size(self, delta):
        new_size = self.base_font_size + delta
        if 8 <= new_size <= 24:
            self.base_font_size = new_size
            self.update_font()
            self.update_stats()

    def on_ctrl_mousewheel(self, event):
        delta = event.delta
        if delta > 0:
            self.change_font_size(1)
        else:
            self.change_font_size(-1)

    def open_view_options(self):
        win = Toplevel(self.root)
        win.title(self.tr['font_size'])
        win.geometry("300x150")
        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        win.configure(bg=bg)
        tk.Label(win, text="Font size:", bg=bg, fg=fg).pack(pady=5)
        scale = Scale(win, from_=8, to=24, orient=tk.HORIZONTAL, command=lambda v: self.change_font(int(float(v))), bg=bg, fg=fg)
        scale.set(self.base_font_size)
        scale.pack(pady=5, padx=20, fill=tk.X)
        btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark else {"bg": "#e0e0e0", "fg": "black"}
        Button(win, text=self.tr['close_btn'], command=win.destroy, **btn_style).pack(pady=10)

    def change_font(self, new_size):
        self.base_font_size = new_size
        self.update_font()

    # ------------------------------------------------------------------
    # Información del comando bajo el cursor (con caras)
    # ------------------------------------------------------------------
    def _get_face_image_path(self, face_id: str) -> str:
        try:
            num = int(face_id)
            num_str = f"{num:02d}"
        except:
            num_str = "00"
        filename = f"fac_sprite_free{num_str}.png"
        base_dir = os.path.dirname(sys.argv[0])
        face_dir = os.path.join(base_dir, "faces", "free")
        return os.path.join(face_dir, filename)

    def _show_face_image(self, face_id: str, face_name: str):
        if not PIL_AVAILABLE:
            messagebox.showinfo("Image Viewer", "PIL (Pillow) is not installed. Cannot display image.")
            return
        img_path = self._get_face_image_path(face_id)
        if not os.path.isfile(img_path):
            messagebox.showinfo("Image Not Found", f"Face image not found:\n{img_path}")
            return
        try:
            img = Image.open(img_path)
            if img.width > 300 or img.height > 300:
                img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            win = tk.Toplevel(self.root)
            win.title(f"Face: {face_name} (ID {face_id})")
            win.transient(self.root)
            label = tk.Label(win, image=photo)
            label.image = photo
            label.pack(padx=10, pady=10)
            tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image:\n{str(e)}")

    def show_command_info(self):
        cursor_pos = self.text_area.index(tk.INSERT)
        line_start = f"{cursor_pos} linestart"
        line_end = f"{cursor_pos} lineend"
        line_text = self.text_area.get(line_start, line_end)
        cursor_col = int(cursor_pos.split('.')[1])

        start_col = cursor_col
        while start_col > 0 and line_text[start_col-1] != '<':
            start_col -= 1
        if start_col == 0 or line_text[start_col-1] != '<':
            messagebox.showinfo(self.tr['cmd_info_title'], self.tr['cmd_not_found'])
            return
        start_col -= 1
        substring = line_text[start_col:]
        match = self.command_pattern.match(substring)
        if not match:
            messagebox.showinfo(self.tr['cmd_info_title'], self.tr['cmd_unrecognized'])
            return
        cmd_name = match.group(1)
        if cmd_name in self.commands_data:
            desc = self.commands_data[cmd_name][2]
            extra = ""
            face_id = None
            music_id = None
            sound_id = None

            if cmd_name == "FAC":
                after = substring[match.end():]
                id_match = re.search(r'(\d{4})', after)
                if id_match:
                    face_id = id_match.group(1)
                    extra = f"\n{self.tr['face_name']}: {self.face_names.get(face_id, 'Unknown')}"
                else:
                    face_id = "0000"
                    extra = f"\n{self.tr['face_name']}: {self.face_names.get('0000', 'Nothing')}"

            elif cmd_name == "CMU":
                after = substring[match.end():]
                id_match = re.search(r'(\d{4})', after)
                if id_match:
                    music_id = id_match.group(1)
                    extra = f"\nMusic: {get_music_name(music_id)}"
                else:
                    extra = ""

            elif cmd_name == "SOU":
                after = substring[match.end():]
                id_match = re.search(r'(\d{4})', after)
                if id_match:
                    sound_id = id_match.group(1)
                    extra = f"\nSound effect: {get_sound_name(sound_id)}"
                else:
                    extra = ""

            # Mostrar información
            msg = f"{desc}{extra}"
            messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", msg)

            # Si es FAC y tenemos el ID, mostrar la imagen
            if cmd_name == "FAC" and face_id is not None:
                face_name = self.face_names.get(face_id, "Unknown")
                self._show_face_image(face_id, face_name)
        else:
            messagebox.showinfo(self.tr['cmd_info_title'], f"{self.tr['cmd_unknown']} '<{cmd_name}>'")

    # ------------------------------------------------------------------
    # Reemplazo inteligente
    # ------------------------------------------------------------------
    def smart_replace_special_chars(self):
        smart_replace_dialog(self.root, self.text_area, self.tr, self.settings.get("dark_theme", False))

    # ------------------------------------------------------------------
    # Personalización de colores de comandos
    # ------------------------------------------------------------------
    def customize_command_colors(self):
        win = tk.Toplevel(self.root)
        win.title(self.tr['cmd_colors_title'])
        win.geometry("600x500")
        win.transient(self.root)
        win.grab_set()

        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        win.configure(bg=bg)

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        frame.configure(bg=bg)

        tk.Label(frame, text=self.tr['cmd_color_instruction'], bg=bg, fg=('white' if dark else 'black')).pack(anchor=tk.W)

        columns = ("command", "color")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("command", text=self.tr['cmd_list'])
        tree.heading("color", text=self.tr['current_color'])
        tree.pack(fill=tk.BOTH, expand=True)

        all_cmds = sorted(self.commands_data.keys())
        for cmd in all_cmds:
            color = self.command_colors.get(cmd, "blue")
            color_display = {
                "blue": self.tr['color_blue'],
                "pink": self.tr['color_pink'],
                "red": self.tr['color_red']
            }.get(color, self.tr['color_blue'])
            tree.insert("", tk.END, values=(cmd, color_display), tags=(cmd,))

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        btn_frame.configure(bg=bg)

        def set_color(color):
            selected = tree.selection()
            if not selected:
                return
            item = selected[0]
            cmd = tree.item(item, "values")[0]
            if color == "reset":
                if cmd in self.command_colors:
                    del self.command_colors[cmd]
            else:
                self.command_colors[cmd] = color
            save_command_colors(self.command_colors_file, self.command_colors)
            new_display = {
                "blue": self.tr['color_blue'],
                "pink": self.tr['color_pink'],
                "red": self.tr['color_red']
            }.get(color, self.tr['color_blue']) if color != "reset" else self.tr['color_blue']
            tree.item(item, values=(cmd, new_display))
            self.delayed_highlight()

        btn_style = {"bg": "#3c3c3c", "fg": "white"} if dark else {"bg": "#f0f0f0", "fg": "black"}
        tk.Button(btn_frame, text=self.tr['color_blue'], command=lambda: set_color("blue"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['color_pink'], command=lambda: set_color("pink"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['color_red'], command=lambda: set_color("red"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['color_reset'], command=lambda: set_color("reset"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['close_btn'], command=win.destroy, **btn_style).pack(side=tk.RIGHT, padx=5)

    # ------------------------------------------------------------------
    # Prueba del juego
    # ------------------------------------------------------------------
    def lookup_doukutsu(self):
        if self.current_file:
            base_dir = os.path.dirname(self.current_file)
            candidate = os.path.join(base_dir, "doukutsu.exe")
            if os.path.isfile(candidate):
                self.doukutsu_path = candidate
                self.status_label.config(text=f"Executable: {candidate}")
                messagebox.showinfo(self.tr['find_doukutsu'], f"Using {candidate}")
                return
        path = filedialog.askopenfilename(
            title=self.tr['find_doukutsu'],
            filetypes=[("Executable", "doukutsu.exe"), ("All files", "*.*")]
        )
        if path:
            self.doukutsu_path = path
            self.status_label.config(text=f"Executable: {os.path.basename(path)}")

    def test_game(self):
        if not self.current_file:
            messagebox.showwarning(self.tr['no_file_warning'], self.tr['no_file_warning'])
            return
        if messagebox.askyesno(self.tr['save_before_test'], self.tr['save_before_test']):
            self.export_file()
        if not self.doukutsu_path:
            self.lookup_doukutsu()
            if not self.doukutsu_path:
                messagebox.showerror(self.tr['exe_not_found'], self.tr['exe_not_found'])
                return
        try:
            import subprocess
            subprocess.Popen([self.doukutsu_path], cwd=os.path.dirname(self.doukutsu_path))
            self.status_label.config(text=self.tr['game_launched'])
            self.add_history_entry("Game launched")
        except Exception as e:
            messagebox.showerror(self.tr['exe_not_found'], str(e))

    # ------------------------------------------------------------------
    # Varios
    # ------------------------------------------------------------------
    def show_about(self):
        messagebox.showinfo(self.tr['about'],
        "TSC Editor+ v1.0\n"
        "Professional editor for Cave Story .tsc files\n"
        "Encryption compatible with Booster's Lab (Carrot Lord)\n"
        "Features:\n"
        "- Syntax highlighting (commands, events, numbers, special characters)\n"
        "- Customizable command colors (blue/pink/red)\n"
        "- Action history, line and character counter\n"
        "- Search and replace with real-time highlighting\n"
        "- Quick command documentation with integrated search\n"
        "- Customizable commands (add/edit/delete)\n"
        "- Auto-save every 6 minutes\n"
        "- Quick font size change with Ctrl+Wheel\n"
        "- Dark mode with dark title bar and full interface\n"
        "- Multilingual support (Spanish, English, Japanese)\n"
        "- Command Syntax Analysis window (Ctrl+Shift+C)\n"
        "- Face image preview for <FAC> command (requires PIL and images in faces/free/)\n"
        "Shortcuts: Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Z, Ctrl+Y, Ctrl+F, Ctrl+H, Ctrl+R, Ctrl+K, F5, Ctrl+Del, Ctrl+Shift+Del, Ctrl+Shift+C, Alt+F4\n"
        "Created for the Cave Story modding community.")

    def show_hex_dump(self):
        if self.raw_bytes_for_hex is None:
            messagebox.showwarning(self.tr['hex_info'], self.tr['hex_info'])
            return
        import binascii
        hex_str = binascii.hexlify(self.raw_bytes_for_hex[:512], ' ').decode('ascii')
        win = Toplevel(self.root)
        win.title(self.tr['hex_window_title'])
        win.geometry("800x400")
        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        win.configure(bg=bg)
        text_w = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Courier New", 9), bg=bg, fg=fg)
        text_w.pack(fill=tk.BOTH, expand=True)
        text_w.insert(tk.END, hex_str)
        text_w.config(state=tk.DISABLED)

    def show_quick_docs(self):
        self.right_notebook.select(self.docs_tab)

    def update_ui_language(self):
        self.tr = self.langs.get(self.current_lang, self.langs['en'])
        self.root.title(self.tr['window_title'])
        self.search_label.config(text=self.tr['search_label'])
        self.clear_btn.config(text=self.tr['clear_btn'])
        self.status_label.config(text=self.tr['status_ready'])
        self.right_notebook.tab(0, text=self.tr['history'])
        self.right_notebook.tab(1, text=self.tr['quick_docs'])
        self.right_notebook.tab(2, text=self.tr['search_tab'])
        self.context_menu.entryconfig(0, label=self.tr['copy'])
        self.context_menu.entryconfig(1, label=self.tr['paste'])
        self.context_menu.entryconfig(2, label=self.tr['cut'])
        self.context_menu.entryconfig(4, label=self.tr['count_chars'])
        self.context_menu.entryconfig(5, label=self.tr['count_chars_face'])
        self.context_menu.entryconfig(7, label=self.tr['tsc_commands'])
        self.context_menu.entryconfig(9, label=self.tr['smart_replace'])
        self.menubar = create_menubar(self)
        self.update_stats()

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
