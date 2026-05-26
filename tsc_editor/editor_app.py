# -*- coding: utf-8 -*-
"""
Main application class for TSC Editor+.
Version 1.2
Now with modern tabs, persistent recent folder, face preview (Freeware/Steam),
export to .txt as plain text, and improved search highlighting.
"""

import os
import sys
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel, Scale, Button, BooleanVar, ttk, simpledialog
from datetime import datetime

# Some Imports
from .encryption import get_cipher_from_tsc, decrypt_tsc, encrypt_tsc
from .command_system import (
    load_base_commands, load_custom_commands, save_custom_commands,
    update_commands_data, build_command_regex, load_command_colors, save_command_colors,
    get_command_color as get_cmd_color
)
from . import animate_switch_faces
from .animate_switch_faces import show_switch_anim_dialog
from .settings_manager import load_settings, save_settings
from .syntax_highlight import check_syntax, highlight_syntax
from .dialogs import ask_encoding_and_cipher, smart_replace_dialog, auto_detect_best
from .ui_components import create_menubar, create_toolbar, create_context_menu, apply_theme_to_widgets, apply_syntax_tags_to_widget
from .file_handling import load_tsc_file, save_tsc_file, load_project_file, save_project_file
from .search_replace import SearchReplaceManager
from .utils import detect_language, update_stats, add_history_entry, get_face_name
from .languages import LANGS
from .music_loader import get_music_name
from .sound_names import get_sound_name
from .highlighted_tsc import highlight_current_file_in_list
from .tab_manager import TabManager
from .load_recents import save_recent_folder, get_recent_folder, should_restore_recent
from .show_hints import HintsManager

# Libs
try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False

try:
    import importlib
    _ttkthemes = importlib.import_module('ttkthemes')
    ThemedTk = getattr(_ttkthemes, 'ThemedTk', None)
    TTKTHEMES_AVAILABLE = ThemedTk is not None
except Exception:
    ThemedTk = None
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

        # Langs
        self.current_lang = detect_language()
        self.langs = LANGS
        self.tr = self.langs.get(self.current_lang, self.langs['en'])

        # Commands
        self.base_commands_data = load_base_commands()
        self.custom_commands_file = os.path.join(os.path.dirname(sys.argv[0]), "custom_commands.json")
        self.custom_commands = load_custom_commands(self.custom_commands_file)
        self.commands_data = update_commands_data(self.base_commands_data, self.custom_commands)
        self.command_pattern = build_command_regex(self.commands_data)

        # Faces (Freeware/Steam)
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
        self.face_names_steam = self.face_names.copy()
        self.face_names_steam["0027"] = "Quote"   # Changed On Steam
        self.face_names_switch = self.face_names_steam.copy()        
        # Command Colors
        self.command_colors_file = os.path.join(os.path.dirname(sys.argv[0]), "command_colors.json")
        self.command_colors = load_command_colors(self.command_colors_file)

        # Config
        self.settings_file = os.path.join(os.path.dirname(sys.argv[0]), "settings.json")
        default_settings = {
            "auto_save": False,
            "language": self.current_lang,
            "show_history": True,
            "show_quick_docs": False,
            "default_font": "Courier New",
            "dark_theme": False,
            "current_theme": "darkly",
            "load_mode": "ask",
            "manual_encoding": "shift_jis",
            "manual_cipher": 0,
            "keep_recent_tsc": False,
            "last_folder": "",
            "enable_ai": True,
            "gemini_api_key": "AIzaSyBQoyxo4pXzyoeoTACxS5UcU8XoF8gAf9s",

        }
        self.settings = load_settings(self.settings_file, default_settings)

        # Migrate old theme
        if "current_theme" not in self.settings:
            if self.settings.get("dark_theme", False):
                self.settings["current_theme"] = "darkly"
            else:
                self.settings["current_theme"] = "cosmo"
            save_settings(self.settings_file, self.settings)

        # Load language
        if self.settings.get("language") != self.current_lang:
            self.current_lang = self.settings["language"]
            self.tr = self.langs.get(self.current_lang, self.langs['en'])

        # Actual theme
        self.available_themes = ["darkly", "vapor", "cosmo"]
        self.current_theme = tk.StringVar(value=self.settings.get("current_theme", "darkly"))

        # Fonts
        import tkinter.font as tkfont
        system_fonts = set(tkfont.families())
        self.available_fonts = []
        script_dir = os.path.dirname(sys.argv[0])
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
        # Noto Sans JP
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

        # Editor status
        self.current_file = None
        self.doukutsu_path = None
        self.current_cipher = None
        self.current_encoding = "shift_jis"
        self.raw_bytes_for_hex = None
        self.history = []
        self.saved_content = ""

        # Build ui
        self._build_ui()

        # Search
        self.search_manager = SearchReplaceManager(self)

        # Autosave
        self.auto_save_timer = None
        if self.settings["auto_save"]:
            self.start_auto_save()

        # Restore recent folder if enabled
        if should_restore_recent(self.settings):
            recent = get_recent_folder(self.settings)
            if recent:
                self.set_current_folder(recent)

        self.add_history_entry("Editor started")
        self.apply_theme()
        self.update_font()
        self.update_ui_language()

        # Secure closure
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Left sidebar (file list)
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

        # Tabs
        self.tab_manager = TabManager(self.main_paned, self)
        self.main_paned.add(self.tab_manager.notebook, minsize=400)

        # Tab title
        self.text_area = None

        # Tab size  
        self.right_notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.right_notebook, minsize=250, width=250)

        # AI Assistant tab (solo si está habilitado y Python >= 3.9)
        if self.settings.get("enable_ai", True) and sys.version_info >= (3, 9):
            try:
                from .gemini_tsc_ai import GeminiTSCAI
                ai_tab_text = self.tr.get('ai_assistant', 'AI Assistant')
                self.ai_tab = tk.Frame(self.right_notebook)
                self.right_notebook.add(self.ai_tab, text=ai_tab_text)  # <--- ¡Usa ai_tab_text!
                self.ai_assistant = GeminiTSCAI(self.ai_tab, self, self.settings)
                print("AI Assistant tab created successfully.")
            except ImportError as e:
                print(f"Failed to import GeminiTSCAI: {e}")
            except Exception as e:
                print(f"Unexpected error creating AI tab: {e}")

        # History
        self.history_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.history_tab, text=self.tr['history'])
        self.history_label = tk.Label(self.history_tab, text=self.tr['history'], font=("Segoe UI", 10, "bold"))
        self.history_label.pack(pady=5)
        self.history_listbox = tk.Listbox(self.history_tab, bg="#f0f0f0", selectbackground="#0078D7")
        self.history_scrollbar = tk.Scrollbar(self.history_tab, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Quick Docs
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
        self.hints_manager = HintsManager(self.docs_tab, self)

        # Search
        self.search_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.search_tab, text=self.tr['search_tab'])
        self._create_search_widgets()

        # Context menu
        self.context_menu = create_context_menu(self)

        # Status Bar
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text=self.tr['status_ready'], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stats_label = tk.Label(self.status_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        self.stats_label.pack(side=tk.RIGHT)

        # Toolbar
        self.toolbar_frame, self.theme_btn = create_toolbar(self)

        # Main menu
        self.menubar = create_menubar(self)

        # Shortcuts
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
        self.root.bind("<Alt-F4>", lambda e: self.on_close())
        self.root.bind("<Control-Shift-O>", lambda e: self.load_project())
        self.root.bind("<Control-Shift-Alt-O>", lambda e: self.load_folder())
        self.root.bind("<Control-Delete>", lambda e: self.delete_current_from_list())
        self.root.bind("<Control-Shift-Delete>", lambda e: self.delete_all_from_list())
        self.root.bind("<Control-h>", lambda e: self.focus_history_tab())
        self.root.bind("<Control-Shift-C>", lambda e: self.open_custom_command_syntax_window())
        self.root.bind("<Control-n>", lambda e: self.tab_manager.add_empty_tab())
        self.root.bind("<Control-t>", lambda e: self.tab_manager.add_empty_tab())
        self.root.bind("<Control-w>", lambda e: self.tab_manager.close_current_tab())
        self.root.bind("<Control-Shift-W>", lambda e: self.tab_manager.close_all_tabs())
        self.root.bind("<Control-Alt-w>", lambda e: self.tab_manager.close_other_tabs())

    # ------------------------------------------------------------------
    # File and tab management methods
    # ------------------------------------------------------------------
    def load_file(self):
        if not self.check_unsaved_changes("otro archivo .tsc"):
            return
        file_path = filedialog.askopenfilename(
            title=self.tr['open_tsc'],
            filetypes=[("TSC Files", "*.tsc"), ("Plain text", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
        self.load_specific_tsc(file_path)

    def _decode_with_fallback(self, raw_bytes: bytes, primary_encoding: str) -> tuple:
        """
        Decodifica raw_bytes usando primary_encoding y fallbacks si aparece '�'.
        Retorna (texto_decodificado, encoding_usado).
        """
        encodings = [primary_encoding, 'cp850', 'cp932', 'latin-1']
        # Eliminar duplicados
        seen = set()
        unique = []
        for enc in encodings:
            if enc not in seen:
                seen.add(enc)
                unique.append(enc)
        best_text = None
        best_enc = primary_encoding
        for enc in unique:
            try:
                text = raw_bytes.decode(enc, errors='replace')
                if '�' not in text:
                    return text, enc
                if best_text is None:
                    best_text = text
                    best_enc = enc
            except Exception:
                continue
        if best_text is not None:
            return best_text, best_enc
        return raw_bytes.decode(primary_encoding, errors='replace'), primary_encoding        

    def load_specific_tsc(self, file_path):
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
            self.raw_bytes_for_hex = raw_data

            mode = self.settings.get("load_mode", "ask")
            if mode == "auto":
                encoding, cipher = auto_detect_best(raw_data, get_cipher_from_tsc, decrypt_tsc)
                if encoding is None:
                    encoding = "shift_jis"
                    cipher = 0
                if cipher == 0:
                    encoding = "utf-8"
            elif mode == "manual":
                encoding = self.settings.get("manual_encoding", "shift_jis")
                cipher = self.settings.get("manual_cipher", 0)
            else:  # 'ask'
                encoding, cipher = ask_encoding_and_cipher(
                    self.root, raw_data, self.settings.get("dark_theme", False),
                    get_cipher_from_tsc, decrypt_tsc
                )
                if encoding is None:
                    return

            decrypted = decrypt_tsc(raw_data, cipher) if cipher != 0 else raw_data

            # Fallback para shift_jis
            if encoding.lower() == 'shift_jis':
                text, used_encoding = self._decode_with_fallback(decrypted, encoding)
                encoding = used_encoding
            else:
                text = decrypted.decode(encoding, errors='replace')

            # Si la codificación resultante es cp850, convertir a español legible
            if encoding == 'cp850':
                text = self._convert_cp850_to_spanish(text)

            self.tab_manager.add_tab(file_path, text, encoding, cipher)
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)} | Cipher={cipher}, Enc={encoding}")
            self.add_history_entry(f"Opened TSC: {os.path.basename(file_path)} (cipher={cipher}, enc={encoding})")
        except Exception as e:
            messagebox.showerror(self.tr['load_error'], f"Could not load {os.path.basename(file_path)}:\n{str(e)}")

    def _convert_cp850_to_spanish(self, text: str) -> str:
        """
        Convierte caracteres específicos de cp850 a sus equivalentes legibles en español.
        """
        mapping = {
            '┐': '¿',
            'í': '¡',
            '±': 'ñ',
            'Ð': 'Ñ',
            'ß': 'á',
            'Ú': 'é',
            'Ý': 'í',
            '¾': 'ó',
            '·': 'ú',
            '─': 'Ä',
            '╦': 'Ë',
            '¤': 'Ï',
            'Í': 'Ö',
            '▄': 'Ü',
            '┴': 'Á',
            '╔': 'É',
            '═': 'Í',
            'Ë': 'Ó',
            '┌': 'Ú',
        }
        trans_table = str.maketrans(mapping)
        return text.translate(trans_table)

    def create_new_text_widget(self, parent):
        text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, undo=True, autoseparators=True, maxundo=50)
        text_widget.bind("<Control-MouseWheel>", self.on_ctrl_mousewheel)
        text_widget.bind("<Control-Button-4>", lambda e: self.change_font_size(1))
        text_widget.bind("<Control-Button-5>", lambda e: self.change_font_size(-1))
        text_widget.bind("<KeyRelease>", self.on_text_change)
        text_widget.bind("<<Paste>>", self.on_paste)
        text_widget.bind("<ButtonRelease-1>", self.on_cursor_move)
        text_widget.bind("<Control-x>", self.on_cut)
        text_widget.bind("<Control-c>", self.on_copy)
        text_widget.bind("<Button-3>", self.show_context_menu)
        apply_syntax_tags_to_widget(text_widget, self.current_theme.get())
        return text_widget

    def export_file(self):
        if not self.text_area:
            return
        if not self.confirm_save_with_errors():
            return
        text_to_save = self.text_area.get("1.0", "end-1c")
        if not text_to_save.strip():
            if not messagebox.askyesno(self.tr['empty_warning'], self.tr['empty_warning']):
                return
        current_path = self.current_file
        if current_path and messagebox.askyesno(self.tr['overwrite_msg'], f"{self.tr['overwrite_question']} '{os.path.basename(current_path)}'?"):
            save_path = current_path
        else:
            save_path = filedialog.asksaveasfilename(
                title=self.tr['export_tsc_dialog_title'],
                defaultextension=".tsc",
                filetypes=[("TSC Files", "*.tsc"), ("Plain text", "*.txt"), ("All files", "*.*")]
            )
            if not save_path:
                return

        is_txt = save_path.lower().endswith('.txt')

        if is_txt:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(text_to_save)
                success = True
            except Exception as e:
                success = False
                messagebox.showerror(self.tr['save_error'], str(e))
        else:
            cipher = self.current_cipher if self.current_cipher is not None else 0
            success = save_tsc_file(save_path, text_to_save, cipher, self.current_encoding,
                                    encrypt_tsc, lambda l: l // 2)

        if success:
            if not is_txt:
                old_key = self.current_file
                if not old_key:
                    try:
                        current_idx = self.tab_manager.notebook.index("current")
                        if current_idx >= 0:
                            old_key = self.tab_manager.buffers[current_idx]['key']
                    except:
                        old_key = None
                if old_key and str(old_key).startswith('__temp'):
                    self.tab_manager.close_tab(old_key)
                    self.tab_manager.add_tab(save_path, text_to_save, self.current_encoding, cipher)
                elif old_key:
                    self.tab_manager.update_tab_file_path(old_key, save_path, text_to_save, self.current_encoding, cipher)
                self.status_label.config(text=f"Exported: {os.path.basename(save_path)} | Cipher: {cipher}")
                self.add_history_entry(f"Saved TSC: {os.path.basename(save_path)}")
                messagebox.showinfo(self.tr['export_success'], f"{self.tr['export_success']}\nCipher: {cipher}")
            else:
                self.status_label.config(text=f"Exported as plain text: {os.path.basename(save_path)}")
                self.add_history_entry(f"Exported as plain text: {os.path.basename(save_path)}")
                messagebox.showinfo(self.tr['export_success'], "File saved as plain text (UTF-8).")
        else:
            if not is_txt:
                messagebox.showerror(self.tr['save_error'], self.tr['save_error'])

    def save_project(self):
        if not self.text_area:
            return
        if not self.confirm_save_with_errors():
            return
        text_to_save = self.text_area.get("1.0", "end-1c")
        if not text_to_save.strip():
            if not messagebox.askyesno(self.tr['empty_warning'], self.tr['empty_warning']):
                return
        current_path = self.current_file
        if current_path and current_path.endswith(".cstsc") and messagebox.askyesno(self.tr['overwrite_msg'], f"{self.tr['overwrite_question']} '{os.path.basename(current_path)}'?"):
            save_path = current_path
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
            old_key = self.current_file if self.current_file else None
            if not old_key:
                try:
                    current_idx = self.tab_manager.notebook.index("current")
                    if current_idx >= 0:
                        old_key = self.tab_manager.buffers[current_idx]['key']
                except:
                    old_key = None
            if old_key and str(old_key).startswith('__temp'):
                self.tab_manager.close_tab(old_key)
                self.tab_manager.add_tab(save_path, text_to_save, "utf-8", None)
            elif old_key:
                self.tab_manager.update_tab_file_path(old_key, save_path, text_to_save, "utf-8", None)
            self.status_label.config(text=f"Project saved: {os.path.basename(save_path)}")
            self.add_history_entry(f"Saved project: {os.path.basename(save_path)}")
            messagebox.showinfo(self.tr['project_saved'], self.tr['project_saved'])
        else:
            messagebox.showerror(self.tr['save_error'], self.tr['save_error'])

    def load_project(self):
        if not self.check_unsaved_changes("otro proyecto .cstsc"):
            return
        file_path = filedialog.askopenfilename(
            title=self.tr['open_project_dialog_title'],
            filetypes=[("TSC Editor+ Project", "*.cstsc"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if not file_path:
            return
        text, success = load_project_file(file_path)
        if success:
            self.tab_manager.add_tab(file_path, text, "utf-8", None)
            self.status_label.config(text=f"Project loaded: {os.path.basename(file_path)}")
            self.add_history_entry(f"Opened project: {os.path.basename(file_path)}")
        else:
            messagebox.showerror(self.tr['load_error'], f"{self.tr['load_error']}:\n{file_path}")

    def save_specific_file(self, file_path, text_widget):
        text_to_save = text_widget.get("1.0", "end-1c")
        if file_path.endswith(".cstsc"):
            save_project_file(file_path, text_to_save)
        else:
            cipher = getattr(text_widget, 'cipher', 0)
            encoding = getattr(text_widget, 'encoding', 'shift_jis')
            save_tsc_file(file_path, text_to_save, cipher, encoding, encrypt_tsc, lambda l: l // 2)
        for buf in self.tab_manager.buffers:
            if buf['key'] == file_path:
                buf['saved_content'] = text_to_save
                break

    def save_file_as(self, text_widget):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tsc",
            filetypes=[("TSC Files", "*.tsc"), ("Project files", "*.cstsc"), ("All files", "*.*")]
        )
        if file_path:
            self.save_specific_file(file_path, text_widget)
            current_idx = self.tab_manager.notebook.index("current")
            if current_idx >= 0:
                old_key = self.tab_manager.buffers[current_idx]['key']
                if str(old_key).startswith('__temp'):
                    text = text_widget.get("1.0", "end-1c")
                    encoding = getattr(text_widget, 'encoding', 'shift_jis')
                    cipher = getattr(text_widget, 'cipher', 0)
                    self.tab_manager.close_tab(old_key)
                    self.tab_manager.add_tab(file_path, text, encoding, cipher)
            return True
        return False

    def confirm_save_with_errors(self):
        if not self.text_area:
            return True
        texto = self.text_area.get("1.0", "end-1c")
        errors = check_syntax(texto, self.commands_data, self.command_pattern)
        if errors:
            return messagebox.askyesno(self.tr['syntax_errors'], self.tr['syntax_errors_found'])
        return True

    def check_unsaved_changes(self, new_file_desc="archivo") -> bool:
        if not self.text_area:
            return True
        current_text = self.text_area.get("1.0", "end-1c")
        if current_text == self.saved_content:
            return True
        answer = messagebox.askyesnocancel(
            self.tr['unsaved_title'],
            self.tr['unsaved_message'].format(new_file_desc)
        )
        if answer is None:
            return False
        elif answer:
            if self.current_file and self.current_file.endswith(".cstsc"):
                self.save_project()
            else:
                self.export_file()
            return True
        else:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", self.saved_content)
            self.text_area.edit_reset()
            return True

    # ------------------------------------------------------------------
    # File Side List
    # ------------------------------------------------------------------
    def load_folder(self):
        if not self.check_unsaved_changes("una carpeta de proyectos"):
            return
        folder = filedialog.askdirectory(title=self.tr['load_folder_title'])
        if not folder:
            return
        self.set_current_folder(folder)

    def set_current_folder(self, folder_path):
        if not folder_path or not os.path.isdir(folder_path):
            return False
        self.current_folder = folder_path
        self.refresh_file_list()
        self.search_var.set("")
        self.filter_files()
        if self.settings.get("keep_recent_tsc", False):
            save_recent_folder(self.settings, folder_path)
            save_settings(self.settings_file, self.settings)
        return True

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
        self.root.after(50, lambda: highlight_current_file_in_list(self))

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
            for buf in self.tab_manager.buffers:
                if buf['key'] == full_path:
                    self.tab_manager.notebook.select(buf['tab_id'])
                    return
            if self.check_unsaved_changes(f"'{os.path.basename(full_path)}'"):
                self.load_specific_tsc(full_path)
            else:
                self.root.after(50, lambda: highlight_current_file_in_list(self))

    def delete_current_from_list(self):
        if not self.current_file:
            messagebox.showinfo("Info", "There is no file loaded.")
            return
        if not self.check_unsaved_changes("eliminar este archivo de la lista"):
            return
        self.all_files = [(r, f) for r, f in self.all_files if f != self.current_file]
        self.filter_files()
        self.status_label.config(text="File removed from list.")
        self.add_history_entry("Removed current file from list")
        highlight_current_file_in_list(self)

    def delete_all_from_list(self):
        if not self.all_files:
            messagebox.showinfo("Info", "There are no files in the list.")
            return
        if not self.check_unsaved_changes("eliminar todos los archivos de la lista"):
            return
        if messagebox.askyesno("Confirm", "Delete ALL files from the sidebar list?\n(They will NOT be deleted from the disk)"):
            self.all_files = []
            self.filter_files()
            self.status_label.config(text="List Cleared.")
            self.add_history_entry("Cleared all files from list")
            highlight_current_file_in_list(self)

    # ------------------------------------------------------------------
    # Quick Docs
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
    # Custom Commands
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
    # Config and theme
    # ------------------------------------------------------------------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title(self.tr['settings_window_title'])
        win.geometry("500x600")
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        # Determine colors based on current theme
        current_theme = self.current_theme.get()
        if current_theme in ("darkly", "vapor"):
            bg, fg, select_bg = "#1e1e1e", "#ffffff", "#3c3c3c"
            btn_bg, btn_fg = "#3c3c3c", "#ffffff"
        else:  # cosmo
            bg, fg, select_bg = "#ffffff", "#000000", "#0078D7"
            btn_bg, btn_fg = "#e0e0e0", "#000000"

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
        tk.Checkbutton(win, text=self.tr['auto_save_label'], variable=auto_var, command=toggle_auto,
                       bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=5)

        # Keep recent TSC
        keep_recent_var = BooleanVar(value=self.settings.get("keep_recent_tsc", False))
        def toggle_keep_recent():
            self.settings["keep_recent_tsc"] = keep_recent_var.get()
            save_settings(self.settings_file, self.settings)
        tk.Checkbutton(win, text="Keep recent TSC folder on startup", variable=keep_recent_var, command=toggle_keep_recent,
                       bg=bg, fg=fg, selectcolor=bg).pack(anchor=tk.W, padx=20, pady=5)

        # Theme selection
        tk.Label(win, text="Theme:", bg=bg, fg=fg).pack(anchor=tk.W, padx=20, pady=(10,0))
        theme_var = tk.StringVar(value=self.current_theme.get())
        theme_menu = ttk.Combobox(win, textvariable=theme_var, values=self.available_themes, state="readonly")
        theme_menu.pack(anchor=tk.W, padx=20, pady=5)

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

        # Load mode settings
        tk.Label(win, text="TSC file loading mode:", bg=bg, fg=fg, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10,0))
        load_mode_var = tk.StringVar(value=self.settings.get("load_mode", "ask"))

        def on_load_mode_change(*args):
            mode = load_mode_var.get()
            if mode == "manual":
                manual_frame.pack(anchor=tk.W, padx=40, pady=5)
            else:
                manual_frame.pack_forget()

        tk.Radiobutton(win, text="Always auto-detect", variable=load_mode_var, value="auto",
                       bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(win, text="Always ask per file", variable=load_mode_var, value="ask",
                       bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(win, text="Always use this encoding and cipher", variable=load_mode_var, value="manual",
                       bg=bg, fg=fg, selectcolor=bg, command=on_load_mode_change).pack(anchor=tk.W, padx=40)

        manual_frame = tk.Frame(win, bg=bg)
        tk.Label(manual_frame, text="Encoding:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)
        manual_encoding_var = tk.StringVar(value=self.settings.get("manual_encoding", "shift_jis"))
        encodings = ["shift_jis", "cp932", "latin-1", "utf-8", "cp850"]
        manual_encoding_menu = ttk.Combobox(manual_frame, textvariable=manual_encoding_var, values=encodings, state="readonly", width=10)
        manual_encoding_menu.pack(side=tk.LEFT, padx=5)
        tk.Label(manual_frame, text="Cipher:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)
        manual_cipher_var = tk.StringVar(value=str(self.settings.get("manual_cipher", 0)))
        manual_cipher_entry = tk.Entry(manual_frame, textvariable=manual_cipher_var, width=6, bg=bg, fg=fg, insertbackground=fg)
        manual_cipher_entry.pack(side=tk.LEFT, padx=5)

        if load_mode_var.get() != "manual":
            manual_frame.pack_forget()
        else:
            manual_frame.pack(anchor=tk.W, padx=40, pady=5)

        load_mode_var.trace_add('write', on_load_mode_change)

        # Buttons
        btn_style = {"bg": btn_bg, "fg": btn_fg, "activebackground": select_bg}

        def apply_settings():
            new_theme = theme_var.get()
            if new_theme != self.current_theme.get():
                self.current_theme.set(new_theme)
                self.settings["current_theme"] = new_theme
                self.apply_theme()
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
            if self.current_theme.get() == "darkly":
                try:
                    self.root.set_theme("equilux")
                except:
                    pass
            elif self.current_theme.get() == "vapor":
                try:
                    self.root.set_theme("equilux")
                except:
                    pass
            else:
                try:
                    self.root.set_theme("clam")
                except:
                    pass
        apply_theme_to_widgets(self, None)
        self.root.after(50, lambda: highlight_current_file_in_list(self))
        self.update_theme_button_text()
        if hasattr(self, 'hints_manager'):
            self.hints_manager.update_theme()
        if PYWINSTYLES_AVAILABLE and sys.platform == "win32":
            try:
                if self.current_theme.get() in ("darkly", "vapor"):
                    pywinstyles.change_header_color(self.root, "#1e1e1e")
                else:
                    pywinstyles.change_header_color(self.root, "#ffffff")
            except:
                pass

    def toggle_theme(self):
        current = self.current_theme.get()
        if current == "darkly":
            new_theme = "cosmo"
        elif current == "cosmo":
            new_theme = "darkly"
        else:
            new_theme = "darkly"
        self.current_theme.set(new_theme)
        self.settings["current_theme"] = new_theme
        save_settings(self.settings_file, self.settings)
        self.apply_theme()
        self.add_history_entry(f"Changed theme to {new_theme}")

    def update_theme_button_text(self):
        if hasattr(self, 'theme_btn'):
            if self.current_theme.get() == "darkly":
                self.theme_btn.config(text="🌙 Darkly")
            elif self.current_theme.get() == "vapor":
                self.theme_btn.config(text="🌙 Vapor")
            else:
                self.theme_btn.config(text="☀️ Cosmo")

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
    # Syntax and colors
    # ------------------------------------------------------------------
    def check_syntax_cmd(self):
        if not self.text_area:
            return
        texto = self.text_area.get("1.0", "end-1c")
        errors = check_syntax(texto, self.commands_data, self.command_pattern)
        if errors:
            msg = f"{self.tr['syntax_errors']}:\n\n"
            for err in errors:
                msg += f"- {err['message']}\n"
            messagebox.showwarning(self.tr['syntax_error_window_title'], msg)
        else:
            messagebox.showinfo(self.tr['syntax_error_window_title'], self.tr['syntax_no_errors'])

    def highlight_syntax(self):
        if not self.text_area:
            return
        highlight_syntax(self.text_area, self.commands_data, self.command_pattern, self.command_colors)

    def delayed_highlight(self):
        self.root.after(50, self.highlight_syntax)

    # ------------------------------------------------------------------
    # Search and replace (fixed)
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
    # Basic editor tools
    # ------------------------------------------------------------------
    def undo_action(self):
        if self.text_area:
            try:
                self.text_area.edit_undo()
                self.add_history_entry("Undo")
            except:
                pass

    def redo_action(self):
        if self.text_area:
            try:
                self.text_area.edit_redo()
                self.add_history_entry("Redo")
            except:
                pass

    def copy_text(self):
        if self.text_area:
            try:
                self.text_area.event_generate("<<Copy>>")
                self.add_history_entry("Copied")
            except:
                pass

    def paste_text(self):
        if self.text_area:
            try:
                self.text_area.event_generate("<<Paste>>")
                self.add_history_entry("Pasted")
            except:
                pass

    def cut_text(self):
        if self.text_area:
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
        if self.text_area:
            self.delayed_highlight()
            self.update_stats()
            if self.settings["auto_save"] and self.current_file and self.current_file.endswith(".cstsc"):
                self.save_project()
            if event and event.char and event.char.isprintable():
                self.add_history_entry("Handwrite")

    def on_cursor_move(self, event=None):
        self.update_stats()

    def update_stats(self):
        if self.text_area:
            text = self.text_area.get("1.0", "end-1c")
            lines = len(text.splitlines())
            chars = len(text)
            self.stats_label.config(text=f"{self.tr['lines']}: {lines}  |  {self.tr['chars']}: {chars}")
        else:
            self.stats_label.config(text="")

    def add_history_entry(self, action):
        add_history_entry(self, action)

    # ------------------------------------------------------------------
    # Characters Count
    # ------------------------------------------------------------------
    def count_characters_normal(self):
        self._count_characters(with_face=False)

    def count_characters_face(self):
        self._count_characters(with_face=True)

    def _count_characters(self, with_face):
        if not self.text_area:
            return
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
    # Fonts
    # ------------------------------------------------------------------
    def update_font(self):
        font_name = self.current_font_name.get()
        if hasattr(self, 'tab_manager'):
            for buf in self.tab_manager.buffers:
                widget = buf['widget']
                widget.config(font=(font_name, self.base_font_size))
                widget.tag_configure("evento", font=(font_name, self.base_font_size, "bold"))
                widget.tag_configure("comando_letras", font=(font_name, self.base_font_size, "bold"))
        if self.text_area:
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
    # Face preview (FAC) with version selection
    # ------------------------------------------------------------------
    def _ask_face_version_and_show(self, face_id: str):
        """Muestra diálogo para elegir versión (Freeware/Steam/Switch) normalizando el ID."""
        # Normalizar el ID a sus dos últimos dígitos (ej. 1019 -> 19 -> "0019")
        try:
            person_id = int(face_id[-2:])
            base_id = f"{person_id:04d}"
        except Exception:
            base_id = "0000"
        
        # Para Freeware y Steam usaremos el base_id (4 dígitos)
        # Para Switch usaremos el face_id original (para detectar 10XX/11XX)
        
        dialog = tk.Toplevel(self.root)
        dialog.title(self.tr['face_version_title'])
        dialog.geometry("350x160")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        current_theme = self.current_theme.get()
        if current_theme in ("darkly", "vapor"):
            bg, fg = "#1e1e1e", "#ffffff"
            btn_bg, btn_fg = "#3c3c3c", "#ffffff"
        else:
            bg, fg = "#ffffff", "#000000"
            btn_bg, btn_fg = "#e0e0e0", "#000000"
        dialog.configure(bg=bg)
        
        tk.Label(dialog, text=self.tr['face_version_question'].format(face_id), bg=bg, fg=fg).pack(pady=10)
        
        def show_freeware():
            # Usar base_id para mostrar la imagen estática Freeware
            self._show_face_image(base_id, "free")
            dialog.destroy()
        
        def show_steam():
            self._show_face_image(base_id, "steam")
            dialog.destroy()
        
        def show_switch():
            from .animate_switch_faces import auto_switch_animation
            auto_switch_animation(self.root, face_id, self.settings)
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=bg)
        btn_frame.pack(pady=10)
        btn_style = {"bg": btn_bg, "fg": btn_fg, "activebackground": "#4a2a6a" if current_theme == "vapor" else "#3c3c3c"}
        tk.Button(btn_frame, text="Freeware", command=show_freeware, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Steam", command=show_steam, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Switch (Animado)", command=show_switch, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, **btn_style).pack(side=tk.LEFT, padx=5)

    def _show_face_image(self, face_id: str, version: str = "free"):
        """Muestra la imagen de la cara según la versión (free/steam)."""
        if not PIL_AVAILABLE:
            messagebox.showinfo("Image Viewer", "PIL (Pillow) is not installed. Cannot display image.")
            return
        try:
            num = int(face_id)
            num_str = f"{num:02d}"
        except:
            num_str = "00"
        if version == "steam":
            filename = f"fac_sprite_steam{num_str}.png"
            face_dir = os.path.join(os.path.dirname(sys.argv[0]), "faces", "steam")
        else:
            filename = f"fac_sprite_free{num_str}.png"
            face_dir = os.path.join(os.path.dirname(sys.argv[0]), "faces", "free")
        img_path = os.path.join(face_dir, filename)
        
        if not os.path.isfile(img_path):
            messagebox.showinfo("Image Not Found", f"Face image not found:\n{img_path}")
            return
        try:
            img = Image.open(img_path)
            if img.width > 300 or img.height > 300:
                img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            win = tk.Toplevel(self.root)
            win.title(f"Face: {face_id} ({version.capitalize()})")
            win.transient(self.root)
            label = tk.Label(win, image=photo)
            label.image = photo
            label.pack(padx=10, pady=10)
            tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image:\n{str(e)}")

    def _show_switch_static(self, face_id: str):
        """Muestra la imagen estática de Switch (sin animación) para códigos 01XX o 00XX."""
        try:
            person_id = int(face_id[-2:])
            base_id = f"{person_id:04d}"
        except:
            base_id = "0000"
        from .animate_switch_faces import load_frames_from_folder
        frames = load_frames_from_folder("anim1", face_id, 96)
        if not frames:
            messagebox.showinfo("Switch", f"No se encontró imagen estática para la cara {face_id}")
            return
        img = frames[0]
        win = tk.Toplevel(self.root)
        win.title(f"Switch - {face_id} (Estático)")
        win.transient(self.root)
        win.resizable(False, False)
        dark = self.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        win.configure(bg=bg)
        label = tk.Label(win, image=img, bg=bg)
        label.image = img
        label.pack(padx=10, pady=10)
        btn_style = {"bg": "#3c3c3c" if dark else "#e0e0e0", "fg": "white" if dark else "black"}
        tk.Button(win, text="Cerrar", command=win.destroy, **btn_style).pack(pady=5)            

    def show_command_info(self):
        if not self.text_area:
            return
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

        # Comandos especiales de dirección (FAI, FAO)
        if cmd_name in ("FAI", "FAO"):
            after = substring[match.end():]
            id_match = re.search(r'(\d{4})', after)
            dir_map = {
                "0000": "Left",
                "0001": "Up",
                "0002": "Right",
                "0003": "Down",
                "0004": "Center",
                "0005": "INVALID (ignored/unchanged)"
            }
            if id_match:
                dir_id = id_match.group(1)
                dir_text = dir_map.get(dir_id, "Unknown direction")
                desc = f"Sets the {cmd_name.lower()} direction.\nDirection: {dir_text}"
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", desc)
            else:
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", "Missing direction parameter (4 digits).")
            return

                    # Comando TRA (teletransporte a mapa)
        if cmd_name == "TRA":
            after = substring[match.end():]
            id_match = re.search(r'(\d{4})', after)
            map_names = {
                "0000": "Null",
                "0001": "Arthur's House - normal",
                "0002": "Egg Corridor",
                "0003": "Egg No. 00 - normal",
                "0004": "Egg No. 06",
                "0005": "Egg Observation Room",
                "0006": "Grasstown",
                "0007": "Santa's House",
                "0008": "Chaco's House",
                "0009": "Labyrinth I (vertical starting room)",
                "0010": "Sand Zone - normal",
                "0011": "Mimiga Village",
                "0012": "First Cave",
                "0013": "Start Point",
                "0014": "Shack (Mimiga Village)",
                "0015": "Reservoir",
                "0016": "Graveyard",
                "0017": "Yamashita Farm",
                "0018": "Shelter (Grasstown)",
                "0019": "Assembly Hall (Mimiga Village)",
                "0020": "Save Point (Mimiga Village)",
                "0021": "Side Room (Egg Corridor)",
                "0022": "Cthulhu's Abode (Egg Corridor)",
                "0023": "Egg No. 01",
                "0024": "Arthur's House - Sue on computer",
                "0025": "Power Room (Grasstown)",
                "0026": "Save Point (Grasstown)",
                "0027": "Execution Chamber (Grasstown)",
                "0028": "Gum (Grasstown)",
                "0029": "Sand Zone Residence",
                "0030": "Grasstown Hut",
                "0031": "Main Artery (Waterway)",
                "0032": "Small Room (Sand Zone)",
                "0033": "Jenka's House - normal",
                "0034": "Deserted House (Sand Zone)",
                "0035": "Sand Zone Storehouse",
                "0036": "Jenka's House - after Balrog attacks",
                "0037": "Sand Zone - after boss fight",
                "0038": "Labyrinth H (sliding block room)",
                "0039": "Labyrinth W (main area w/shop, camp)",
                "0040": "Camp (Labyrinth)",
                "0041": "Clinic Ruins (Labyrinth)",
                "0042": "Labyrinth Shop",
                "0043": "Labyrinth B (booster)",
                "0044": "Boulder Chamber (Labyrinth)",
                "0045": "Labyrinth M (gaudi eggs)",
                "0046": "Dark Place (Labyrinth)",
                "0047": "Core (Labyrinth)",
                "0048": "Waterway",
                "0049": "Egg Corridor?",
                "0050": "Cthulhu's Abode? (Egg Corridor?)",
                "0051": "Egg Observation Room?",
                "0052": "Egg No. 00 - hatched",
                "0053": "Outer Wall",
                "0054": "Side Room (Egg Corridor?)",
                "0055": "Storehouse (Outer Wall)",
                "0056": "Plantation",
                "0057": "Jail No. 1 (Plantation)",
                "0058": "Hideout (Plantation)",
                "0059": "Rest Area (Plantation)",
                "0060": "Teleporter (Plantation)",
                "0061": "Jail No. 2 (Plantation)",
                "0062": "Balcony - normal",
                "0063": "Last Cave",
                "0064": "Throne Room (Balcony)",
                "0065": "The King's Table (Balcony)",
                "0066": "Prefab House (Balcony) - normal",
                "0067": "Last Cave Hidden",
                "0068": "Black Space (Balcony)",
                "0069": "Little House (Outer Wall)",
                "0070": "Balcony - after boss fights",
                "0071": "Ending",
                "0072": "Intro",
                "0073": "Waterway Cabin",
                "0074": "Credits - Labyrinth",
                "0075": "Credits - Jenka's House",
                "0076": "Credits - Power Room",
                "0077": "Credits - Graveyard",
                "0078": "Credits - Sky",
                "0079": "Prefab House (Balcony) - entrance to hell",
                "0080": "Sacred Ground B1",
                "0081": "Sacred Ground B2",
                "0082": "Sacred Ground B3",
                "0083": "Storage (Graveyard)",
                "0084": "Passage? - normal",
                "0085": "Passage? - from Sacred Ground B3",
                "0086": "Statue Chamber (Plantation/Sacred Grounds)",
                "0087": "Seal Chamber (Sacred Grounds) - normal",
                "0088": "Corridor (Sacred Grounds)",
                "0089": "Credits - Laboratory",
                "0090": "Hermit Gunsmith",
                "0091": "Island",
                "0092": "Seal Chamber (Sacred Grounds) - after boss fight",
                "0093": "Credits - Balcony",
                "0094": "Clock Room (Outer Wall)"
            }
            if id_match:
                map_id = id_match.group(1)
                map_name = map_names.get(map_id, "Unknown map ID")
                desc = f"Teleport to map.\nMap ID: {map_id}\nName: {map_name}"
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", desc)
            else:
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", "Missing map ID parameter (4 digits).")
            return

        # Comandos relacionados con armas: AM+, AM-, AMJ, GIT, TAM
        if cmd_name in ("AM+", "AM-", "AMJ", "GIT", "TAM"):
            after = substring[match.end():]
            id_match = re.search(r'(\d{4})', after)
            weapon_names = {
                "0000": "Nothing",
                "0001": "Snake",
                "0002": "Polar Star",
                "0003": "Fireball",
                "0004": "Machine Gun",
                "0005": "Missile Launcher",
                "0006": "Missiles (GIT only)",
                "0007": "Bubbler",
                "0008": "Nothing?",
                "0009": "Blade",
                "0010": "Super Missile Launcher",
                "0011": "Super Missiles (GIT only)",
                "0012": "Nemesis",
                "0013": "Spur"
            }
            if id_match:
                weapon_id = id_match.group(1)
                weapon_name = weapon_names.get(weapon_id, "Unknown weapon ID")
                desc = f"Weapon operation.\nCommand: {cmd_name}\nWeapon ID: {weapon_id}\nName: {weapon_name}"
                # Descripción adicional según comando
                if cmd_name == "AM+":
                    desc += "\nAdd ammo/weapon."
                elif cmd_name == "AM-":
                    desc += "\nRemove ammo/weapon."
                elif cmd_name == "AMJ":
                    desc += "\nSet ammo to maximum (Japanese version?)."
                elif cmd_name == "GIT":
                    desc += "\nGet item/weapon."
                elif cmd_name == "TAM":
                    desc += "\nTest ammo/weapon (condition)."
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", desc)
            else:
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", "Missing weapon ID parameter (4 digits).")
            return

        # Comandos relacionados con items: GIT, IT+, IT-, ITJ
        if cmd_name in ("GIT", "IT+", "IT-", "ITJ"):
            after = substring[match.end():]
            id_match = re.search(r'(\d{4})', after)
            item_names = {
                "0000": "Blank - Clears box in GIT",
                "0001": "Arthur's Key",
                "0002": "Map System",
                "0003": "Santa's Key",
                "0004": "Silver Locket",
                "0005": "Beast Fang",
                "0006": "Life Capsule (GIT only)",
                "0007": "ID Card",
                "0008": "Jellyfish Juice",
                "0009": "Rusty Key",
                "0010": "Gum Key",
                "0011": "Gum Base",
                "0012": "Charcoal",
                "0013": "Explosive",
                "0014": "Puppy",
                "0015": "Life Pot",
                "0016": "Cure-All",
                "0017": "Clinic Key",
                "0018": "Booster 0.8",
                "0019": "Arms Barrier",
                "0020": "Turbocharge",
                "0021": "Curly's Air Tank",
                "0022": "Nikumaru Counter",
                "0023": "Booster v2.0",
                "0024": "Mimiga Mask",
                "0025": "Teleporter Room Key",
                "0026": "Sue's Letter",
                "0027": "Controller",
                "0028": "Broken Sprinkler",
                "0029": "Sprinkler",
                "0030": "Tow Rope",
                "0031": "Clay Figure Medal",
                "0032": "Little Man",
                "0033": "Mushroom Badge",
                "0034": "Ma Pignon",
                "0035": "Curly's Underwear",
                "0036": "Alien Medal",
                "0037": "Chaco's Lipstick",
                "0038": "Whimsical Star",
                "0039": "Iron Bond"
            }
            if id_match:
                item_id = id_match.group(1)
                item_name = item_names.get(item_id, "Unknown item ID")
                desc = f"Item operation.\nCommand: {cmd_name}\nItem ID: {item_id}\nName: {item_name}"
                if cmd_name == "GIT":
                    desc += "\nGet item (add to inventory)."
                elif cmd_name == "IT+":
                    desc += "\nAdd item."
                elif cmd_name == "IT-":
                    desc += "\nRemove item."
                elif cmd_name == "ITJ":
                    desc += "\nCheck if item exists (condition)."
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", desc)
            else:
                messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", "Missing item ID parameter (4 digits).")
            return

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
                    full_id = id_match.group(1)
                    face_id = full_id
                    prefix = full_id[:2]
                    try:
                        person_id = int(full_id[-2:])
                        base_id = f"{person_id:04d}"
                    except:
                        base_id = "0000"
                    name_base = self.face_names.get(base_id, "Unknown")
                    if base_id == "0027":
                        name_steam = "Quote"
                        name_switch = "Quote"
                    else:
                        name_steam = name_base
                        name_switch = name_base
                    
                    if prefix == "00":
                        extra = f"\nFreeware: {name_base}\nSteam: {name_base}"
                    elif prefix in ("01", "10", "11"):
                        extra = f"\nSwitch: {name_switch}"
                    else:
                        extra = f"\nFreeware: {name_base}\nSteam: {name_steam}\nSwitch: {name_switch}"
                else:
                    face_id = "0000"
                    extra = "\nFreeware: Nothing\nSteam: Nothing\nSwitch: Nothing"

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

            msg = f"{desc}{extra}"
            messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_name}", msg)

            if cmd_name == "FAC" and face_id is not None:
                if messagebox.askyesno(self.tr['face_view_title'], self.tr['face_view_question'].format(face_id)):
                    self._ask_face_version_and_show(face_id)
        else:
            messagebox.showinfo(self.tr['cmd_info_title'], f"{self.tr['cmd_unknown']} '<{cmd_name}>'")

    # ------------------------------------------------------------------
    # Smart replace
    # ------------------------------------------------------------------
    def smart_replace_special_chars(self):
        smart_replace_dialog(self.root, self.text_area, self.tr, self.settings.get("dark_theme", False))

    # ------------------------------------------------------------------
    # Command Color Customization
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
    # Gametest
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
    # Misc
    # ------------------------------------------------------------------
    def show_about(self):
        messagebox.showinfo(self.tr['about'],
        "TSC Editor+ v1.2\n"
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
        "- Modern tabs (Ctrl+T new tab, Ctrl+W close tab)\n"
        "- Keep recent TSC folder on startup\n"
        "- Face image preview for <FAC> command (Freeware/Steam)\n"
        "- Export to .txt as plain text (UTF-8)\n"
        "Shortcuts: Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Z, Ctrl+Y, Ctrl+F, Ctrl+H, Ctrl+R, Ctrl+K, F5, Ctrl+Del, Ctrl+Shift+Del, Ctrl+Shift+C, Ctrl+T, Ctrl+W, Ctrl+Shift+W, Ctrl+Alt+W, Ctrl+N, Alt+F4\n"
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
        if hasattr(self, 'context_menu') and self.context_menu:
            self.context_menu.entryconfig(0, label=self.tr['copy'])
            self.context_menu.entryconfig(1, label=self.tr['paste'])
            self.context_menu.entryconfig(2, label=self.tr['cut'])
            self.context_menu.entryconfig(4, label=self.tr['count_chars'])
            self.context_menu.entryconfig(5, label=self.tr['count_chars_face'])
            self.context_menu.entryconfig(7, label=self.tr['tsc_commands'])
            self.context_menu.entryconfig(9, label=self.tr['smart_replace'])
        self.menubar = create_menubar(self)
        self.update_stats()
        if hasattr(self, 'hints_manager'):
            self.hints_manager.update_language()

    def show_context_menu(self, event):
        if self.context_menu:
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def on_close(self):
        if hasattr(self, 'tab_manager'):
            for buf in list(self.tab_manager.buffers):
                if not self.tab_manager.close_tab(buf['key']):
                    return
        if hasattr(self, 'hints_manager'):
            self.hints_manager.destroy()
        self.root.destroy()
