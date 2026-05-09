#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, Toplevel, Scale, Button, BooleanVar, ttk, simpledialog
import os
import subprocess
import re
import sys
import json
import binascii
import locale
from datetime import datetime

# ---------------------------- CLASE TSCEditor ----------------------------
class TSCEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("TSC Editor+ - Professional Edition")
        self.root.geometry("1300x700")

        # ---------- IDIOMAS ----------
        self.langs = {
            'en': {
                'window_title': 'TSC Editor+ - Professional Edition',
                'file_menu': 'File',
                'open_tsc': 'Open .tsc...',
                'open_project': 'Open .cstsc project...',
                'open_folder': 'Open project folder...',
                'delete_from_list': 'Delete loaded TSC from this list',
                'export_tsc': 'Export .tsc...',
                'save_project': 'Save project .cstsc...',
                'settings': 'Settings...',
                'exit': 'Exit',
                'edit_menu': 'Edit',
                'undo': 'Undo',
                'redo': 'Redo',
                'search_tab': 'Search',
                'check_syntax': 'Check Syntax',
                'smart_replace': 'Smart Replace Special Characters',
                'view_menu': 'View',
                'font_size': 'Font size...',
                'hex_dump': 'Hex dump of current file...',
                'show_history': 'Show History',
                'see_quick_docs': 'See Quick Docs',
                'edit_custom_cmds': 'Edit Custom Commands...',
                'font_submenu': 'Font',
                'run_menu': 'Run',
                'find_doukutsu': 'Find doukutsu.exe...',
                'test_game': 'Test (F5)',
                'help_menu': 'Help',
                'about': 'About...',
                'search_label': 'Search file:',
                'clear_btn': 'X',
                'status_ready': 'Ready',
                'open_project_dialog_title': 'Open .cstsc project',
                'save_project_dialog_title': 'Save project',
                'export_tsc_dialog_title': 'Save .tsc file',
                'load_folder_title': 'Select folder with .tsc files',
                'hex_info': 'No data',
                'hex_window_title': 'Hex dump (first 512 bytes)',
                'settings_window_title': 'Settings',
                'auto_save_label': 'Auto-save project (.cstsc) every 6 minutes',
                'language_label': 'Language:',
                'apply_btn': 'Apply',
                'close_btn': 'Close',
                'cmd_info_title': 'Info',
                'cmd_not_found': 'No TSC command at cursor.',
                'cmd_unrecognized': 'Command format not recognized.',
                'cmd_unknown': 'No documentation for',
                'music_id': 'Music ID',
                'direction': 'Direction',
                'empty_warning': 'The text is empty. Save anyway?',
                'overwrite_msg': 'Overwrite',
                'overwrite_question': 'Overwrite',
                'export_success': 'File saved successfully.',
                'project_saved': 'Project saved in UTF-8.',
                'load_error': 'Could not load file',
                'save_error': 'Could not save file',
                'search_not_found': 'No more matches found.',
                'search_back_not_found': 'No more matches backwards.',
                'replace_all_count': ' replacements performed.',
                'no_file_warning': 'No file loaded. Load or save a .tsc first.',
                'save_before_test': 'Save changes before running?',
                'exe_not_found': 'Could not find doukutsu.exe',
                'game_launched': 'Game launched',
                'lines': 'Lines',
                'chars': 'Chars',
                'history': 'History',
                'copy': 'Copy',
                'paste': 'Paste',
                'cut': 'Cut',
                'count_chars': 'Count Characters',
                'count_chars_face': 'Count Characters (Face)',
                'count_normal_title': 'Character count (Normal)',
                'count_face_title': 'Character count (Face)',
                'fits': 'This text fits correctly in the message box',
                'not_fits': 'This text may NOT fit correctly in the message box',
                'limit': 'Limit',
                'quick_docs': 'Quick Docs',
                'command': 'Command',
                'syntax': 'Syntax',
                'description': 'Description',
                'details': 'Script Details',
                'face_name': 'Face',
                'music_name': 'Music',
                'confirm': 'Confirm',
                'backup_warning': 'It is recommended to make a backup of this TSC file before proceeding.\nThis action cannot be undone (except via Undo).',
                'done': 'Done',
                'no_changes': 'No changes',
                'smart_replace_title': 'Smart Replace Special Characters',
                'option_nn': "Replace 'ñÑ' with 'nN'",
                'option_accents': 'Remove accents (áéíóúüÁÉÍÓÚÜ) → aeiouuAEIOUU',
                'option_symbols': 'Remove rare symbols (¡¿)',
                'option_all': 'All of the above',
                'syntax_errors': 'Syntax Errors',
                'syntax_errors_found': 'Syntax errors found. Save anyway?',
                'syntax_no_errors': 'No syntax errors found.',
                'syntax_error_window_title': 'Syntax Check',
                'auto_save_notification': 'Project auto-saved',
                'find': 'Find',
                'replace': 'Replace',
                'replace_all': 'Replace All',
                'find_next': 'Find Next',
                'find_prev': 'Find Previous',
                'case_sensitive': 'Case sensitive',
                'whole_word': 'Whole word',
                'search_term': 'Search term:',
                'replace_term': 'Replace with:',
                'edit_custom_cmds_title': 'Edit Custom Commands',
                'custom_cmd_name': 'Command name (without <):',
                'custom_cmd_desc': 'Description:',
                'custom_cmd_args': 'Number of arguments (0-4):',
                'search_docs': 'Search command...',
            },
            'es': {
                'window_title': 'TSC Editor+ - Edición Profesional',
                'file_menu': 'Archivo',
                'open_tsc': 'Abrir .tsc...',
                'open_project': 'Abrir proyecto .cstsc...',
                'open_folder': 'Abrir carpeta de proyectos...',
                'delete_from_list': 'Eliminar TSC cargado de esta lista',
                'export_tsc': 'Exportar .tsc...',
                'save_project': 'Guardar proyecto .cstsc...',
                'settings': 'Configuración...',
                'exit': 'Salir',
                'edit_menu': 'Editar',
                'undo': 'Deshacer',
                'redo': 'Rehacer',
                'search_tab': 'Buscar',
                'check_syntax': 'Verificar sintaxis',
                'smart_replace': 'Reemplazo inteligente de caracteres especiales',
                'view_menu': 'Ver',
                'font_size': 'Tamaño de fuente...',
                'hex_dump': 'Ver hexadecimal del archivo actual...',
                'show_history': 'Mostrar historial',
                'see_quick_docs': 'Ver documentación rápida',
                'edit_custom_cmds': 'Editar comandos personalizados...',
                'font_submenu': 'Fuente',
                'run_menu': 'Ejecutar',
                'find_doukutsu': 'Buscar doukutsu.exe...',
                'test_game': 'Probar (F5)',
                'help_menu': 'Ayuda',
                'about': 'Acerca de...',
                'search_label': 'Buscar archivo:',
                'clear_btn': 'X',
                'status_ready': 'Listo',
                'open_project_dialog_title': 'Abrir proyecto .cstsc',
                'save_project_dialog_title': 'Guardar proyecto',
                'export_tsc_dialog_title': 'Guardar archivo .tsc',
                'load_folder_title': 'Seleccionar carpeta con archivos .tsc',
                'hex_info': 'Sin datos',
                'hex_window_title': 'Vista hexadecimal (primeros 512 bytes)',
                'settings_window_title': 'Configuración',
                'auto_save_label': 'Auto-guardar proyecto (.cstsc) cada 6 minutos',
                'language_label': 'Idioma:',
                'apply_btn': 'Aplicar',
                'close_btn': 'Cerrar',
                'cmd_info_title': 'Información',
                'cmd_not_found': 'No hay un comando TSC en esta posición.',
                'cmd_unrecognized': 'Formato de comando no reconocido.',
                'cmd_unknown': 'No hay documentación para',
                'music_id': 'ID de música',
                'direction': 'Dirección',
                'empty_warning': 'El texto está vacío. ¿Guardar de todos modos?',
                'overwrite_msg': 'Sobrescribir',
                'overwrite_question': '¿Sobrescribir',
                'export_success': 'Archivo guardado correctamente.',
                'project_saved': 'Proyecto guardado en UTF-8.',
                'load_error': 'No se pudo cargar el archivo',
                'save_error': 'No se pudo guardar',
                'search_not_found': 'No se encontró más texto.',
                'search_back_not_found': 'No se encontró texto hacia atrás.',
                'replace_all_count': ' reemplazos realizados.',
                'no_file_warning': 'No hay archivo cargado. Cargue o guarde un .tsc primero.',
                'save_before_test': '¿Guardar cambios antes de ejecutar?',
                'exe_not_found': 'No se encontró doukutsu.exe',
                'game_launched': 'Juego lanzado',
                'lines': 'Líneas',
                'chars': 'Caracteres',
                'history': 'Historial',
                'copy': 'Copiar',
                'paste': 'Pegar',
                'cut': 'Cortar',
                'count_chars': 'Contar caracteres',
                'count_chars_face': 'Contar caracteres (cara)',
                'count_normal_title': 'Conteo de caracteres (Normal)',
                'count_face_title': 'Conteo de caracteres (Cara)',
                'fits': 'Este mensaje puede caber correctamente en la caja de diálogo',
                'not_fits': 'Este mensaje quizá NO pueda caber correctamente en la caja de diálogo',
                'limit': 'Límite',
                'quick_docs': 'Documentación rápida',
                'command': 'Comando',
                'syntax': 'Sintaxis',
                'description': 'Descripción',
                'details': 'Detalles del script',
                'face_name': 'Cara',
                'music_name': 'Música',
                'confirm': 'Confirmar',
                'backup_warning': 'Se recomienda hacer una copia de seguridad de este archivo TSC antes de continuar.\nEsta acción no se puede deshacer (excepto mediante Deshacer).',
                'done': 'Hecho',
                'no_changes': 'Sin cambios',
                'smart_replace_title': 'Reemplazo inteligente de caracteres especiales',
                'option_nn': "Reemplazar 'ñÑ' por 'nN'",
                'option_accents': 'Eliminar acentos (áéíóúüÁÉÍÓÚÜ) → aeiouuAEIOUU',
                'option_symbols': 'Eliminar símbolos raros (¡¿)',
                'option_all': 'Todo lo anterior',
                'syntax_errors': 'Errores de sintaxis',
                'syntax_errors_found': 'Se encontraron errores de sintaxis. ¿Guardar de todos modos?',
                'syntax_no_errors': 'No se encontraron errores de sintaxis.',
                'syntax_error_window_title': 'Verificación de sintaxis',
                'auto_save_notification': 'Proyecto auto-guardado',
                'find': 'Buscar',
                'replace': 'Reemplazar',
                'replace_all': 'Reemplazar todo',
                'find_next': 'Buscar siguiente',
                'find_prev': 'Buscar anterior',
                'case_sensitive': 'Mayúsculas/minúsculas',
                'whole_word': 'Palabra completa',
                'search_term': 'Término a buscar:',
                'replace_term': 'Reemplazar con:',
                'edit_custom_cmds_title': 'Editar comandos personalizados',
                'custom_cmd_name': 'Nombre del comando (sin <):',
                'custom_cmd_desc': 'Descripción:',
                'custom_cmd_args': 'Número de argumentos (0-4):',
                'search_docs': 'Buscar comando...',
            },
            'jp': {
                'window_title': 'TSC Editor+ - プロフェッショナル版',
                'file_menu': 'ファイル',
                'open_tsc': '.tscを開く...',
                'open_project': '.cstscプロジェクトを開く...',
                'open_folder': 'プロジェクトフォルダを開く...',
                'delete_from_list': 'ロードしたTSCをこのリストから削除',
                'export_tsc': '.tscにエクスポート...',
                'save_project': 'プロジェクトを保存.cstsc...',
                'settings': '設定...',
                'exit': '終了',
                'edit_menu': '編集',
                'undo': '元に戻す',
                'redo': 'やり直し',
                'search_tab': '検索',
                'check_syntax': '構文チェック',
                'smart_replace': '特殊文字のスマート置換',
                'view_menu': '表示',
                'font_size': 'フォントサイズ...',
                'hex_dump': '現在のファイルの16進ダンプ...',
                'show_history': '履歴を表示',
                'see_quick_docs': 'クイックドキュメントを表示',
                'edit_custom_cmds': 'カスタムコマンドを編集...',
                'font_submenu': 'フォント',
                'run_menu': '実行',
                'find_doukutsu': 'doukutsu.exeを検索...',
                'test_game': 'テスト（F5）',
                'help_menu': 'ヘルプ',
                'about': 'このソフトについて...',
                'search_label': 'ファイル検索:',
                'clear_btn': 'X',
                'status_ready': '準備完了',
                'open_project_dialog_title': '.cstscプロジェクトを開く',
                'save_project_dialog_title': 'プロジェクトを保存',
                'export_tsc_dialog_title': '.tscファイルを保存',
                'load_folder_title': '.tscファイルのあるフォルダを選択',
                'hex_info': 'データなし',
                'hex_window_title': '16進ダンプ（最初の512バイト）',
                'settings_window_title': '設定',
                'auto_save_label': 'プロジェクトを自動保存（.cstsc）6分ごと',
                'language_label': '言語:',
                'apply_btn': '適用',
                'close_btn': '閉じる',
                'cmd_info_title': '情報',
                'cmd_not_found': 'カーソル位置にTSCコマンドがありません。',
                'cmd_unrecognized': 'コマンド形式が認識できません。',
                'cmd_unknown': '次のコマンドのドキュメントはありません',
                'music_id': '音楽ID',
                'direction': '方向',
                'empty_warning': 'テキストが空です。それでも保存しますか？',
                'overwrite_msg': '上書き',
                'overwrite_question': '上書きしますか？',
                'export_success': 'ファイルは正常に保存されました。',
                'project_saved': 'プロジェクトはUTF-8で保存されました。',
                'load_error': 'ファイルを読み込めませんでした',
                'save_error': '保存できませんでした',
                'search_not_found': 'これ以上見つかりません。',
                'search_back_not_found': '後方に見つかりません。',
                'replace_all_count': ' 件置換しました。',
                'no_file_warning': 'ファイルが読み込まれていません。まず.tscを読み込むか保存してください。',
                'save_before_test': '実行前に変更を保存しますか？',
                'exe_not_found': 'doukutsu.exeが見つかりません',
                'game_launched': 'ゲームを起動しました',
                'lines': '行',
                'chars': '文字',
                'history': '履歴',
                'copy': 'コピー',
                'paste': 'ペースト',
                'cut': 'カット',
                'count_chars': '文字数をカウント',
                'count_chars_face': '文字数をカウント（顔あり）',
                'count_normal_title': '文字数カウント（通常）',
                'count_face_title': '文字数カウント（顔）',
                'fits': 'このメッセージはダイアログボックスに正しく収まります',
                'not_fits': 'このメッセージはダイアログボックスに収まらない可能性があります',
                'limit': '制限',
                'quick_docs': 'クイックドキュメント',
                'command': 'コマンド',
                'syntax': '構文',
                'description': '説明',
                'details': 'スクリプト詳細',
                'face_name': '顔',
                'music_name': '音楽',
                'confirm': '確認',
                'backup_warning': '続行する前にこのTSCファイルのバックアップを作成することをお勧めします。\nこの操作は元に戻せません（元に戻す機能を除く）。',
                'done': '完了',
                'no_changes': '変更なし',
                'smart_replace_title': '特殊文字のスマート置換',
                'option_nn': "'ñÑ' を 'nN' に置換",
                'option_accents': 'アクセント記号を削除 (áéíóúüÁÉÍÓÚÜ) → aeiouuAEIOUU',
                'option_symbols': 'まれな記号を削除 (¡¿)',
                'option_all': 'すべて選択',
                'syntax_errors': '構文エラー',
                'syntax_errors_found': '構文エラーが見つかりました。それでも保存しますか？',
                'syntax_no_errors': '構文エラーは見つかりませんでした。',
                'syntax_error_window_title': '構文チェック',
                'auto_save_notification': 'プロジェクトを自動保存しました',
                'find': '検索',
                'replace': '置換',
                'replace_all': 'すべて置換',
                'find_next': '次を検索',
                'find_prev': '前を検索',
                'case_sensitive': '大文字小文字を区別',
                'whole_word': '単語単位',
                'search_term': '検索語:',
                'replace_term': '置換後:',
                'edit_custom_cmds_title': 'カスタムコマンドを編集',
                'custom_cmd_name': 'コマンド名（<なし）:',
                'custom_cmd_desc': '説明:',
                'custom_cmd_args': '引数の数（0-4）:',
                'search_docs': 'コマンドを検索...',
            }
        }

        self.current_lang = self.detect_language()
        self.tr = self.langs[self.current_lang]

        # ---------- COMANDOS BASE + PERSONALIZADOS ----------
        self.base_commands_data = self.load_base_commands()
        self.custom_commands_file = os.path.join(os.path.dirname(sys.argv[0]), "custom_commands.json")
        self.load_custom_commands()
        self.update_commands_data()

        self.face_names = {
            "0000": "Nothing",
            "0001": "Sue Smile", "0002": "Sue Serious", "0003": "Sue Angry", "0004": "Sue Injured",
            "0005": "Balrog Serious", "0006": "Toroko", "0007": "King", "0008": "Toroko Scared",
            "0009": "Jack", "0010": "Kazuma", "0011": "Toroko Red", "0012": "Igor", "0013": "Jenka",
            "0014": "Balrog Happy!", "0015": "Misery", "0016": "Misery Happy!", "0017": "Booster Injured",
            "0018": "Booster", "0019": "Curly Smile", "0020": "Curly Sad", "0021": "The Doctor",
            "0022": "Momorin", "0023": "Balrog Injured", "0024": "A Random Surface Robot",
            "0025": "Curly Serious", "0026": "Misery Angry", "0027": "Human Sue? (Unused)",
            "0028": "Itoh", "0029": "Ballos", "0030": "Out Of Bounds!",
        }

        # ---------- CONFIGURACIÓN ----------
        self.settings_file = os.path.join(os.path.dirname(sys.argv[0]), "settings.json")
        self.settings = {
            "auto_save": False,
            "language": self.current_lang,
            "show_history": True,
            "show_quick_docs": False
        }
        self.load_settings()
        if self.settings.get("language") != self.current_lang:
            self.current_lang = self.settings["language"]
            self.tr = self.langs[self.current_lang]

        # Fuentes disponibles
        self.available_fonts = ["Courier New", "Consolas"]
        script_dir = os.path.dirname(sys.argv[0])
        cave_font_path = os.path.join(script_dir, "Cave-Story.ttf")
        if os.path.isfile(cave_font_path):
            self.available_fonts.append("Cave Story")
        lucida_font_path = os.path.join(script_dir, "Lucida Grande Regular.ttf")
        if os.path.isfile(lucida_font_path):
            self.available_fonts.append("Lucida Grande")
        self.current_font_name = tk.StringVar(value="Courier New")
        self.base_font_size = 10

        # ---------- INTERFAZ PRINCIPAL ----------
        self.main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Barra lateral izquierda
        self.sidebar_frame = tk.Frame(self.main_paned, width=250, height=700)
        self.main_paned.add(self.sidebar_frame, minsize=180, width=250)
        self.files_tab = tk.Frame(self.sidebar_frame)
        self.files_tab.pack(fill=tk.BOTH, expand=True)

        search_frame = tk.Frame(self.files_tab)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        self.search_label = tk.Label(search_frame, text=self.tr['search_label'])
        self.search_label.pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *args: self.filter_files())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
        self.clear_btn = tk.Button(search_frame, text=self.tr['clear_btn'], command=self.clear_search)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.file_listbox = tk.Listbox(self.files_tab, bg="#f0f0f0", selectbackground="#0078D7")
        scrollbar_files = tk.Scrollbar(self.files_tab, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar_files.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_files.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.bind("<Double-Button-1>", self.on_file_select)

        self.current_folder = None
        self.all_files = []

        # Panel central: editor
        self.text_area = scrolledtext.ScrolledText(
            self.main_paned, wrap=tk.WORD, undo=True, autoseparators=True, maxundo=50
        )
        self.main_paned.add(self.text_area, minsize=400)
        self.text_area.bind("<Control-MouseWheel>", self.on_ctrl_mousewheel)
        self.text_area.bind("<Control-Button-4>", lambda e: self.change_font_size(1))
        self.text_area.bind("<Control-Button-5>", lambda e: self.change_font_size(-1))

        # Panel derecho: Notebook (History, Quick Docs, Search)
        self.right_notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.right_notebook, minsize=250, width=250)

        # History tab
        self.history_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.history_tab, text=self.tr['history'])
        self.history_label = tk.Label(self.history_tab, text=self.tr['history'], font=("Segoe UI", 10, "bold"))
        self.history_label.pack(pady=5)
        self.history_listbox = tk.Listbox(self.history_tab, bg="#f0f0f0", selectbackground="#0078D7")
        self.history_scrollbar = tk.Scrollbar(self.history_tab, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Quick Docs tab (con buscador)
        self.docs_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.docs_tab, text=self.tr['quick_docs'])
        docs_paned = tk.PanedWindow(self.docs_tab, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        docs_paned.pack(fill=tk.BOTH, expand=True)

        # Buscador de comandos
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
        scrollbar_docs = tk.Scrollbar(top_frame, orient=tk.VERTICAL, command=self.docs_listbox.yview)
        self.docs_listbox.config(yscrollcommand=scrollbar_docs.set)
        self.docs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_docs.pack(side=tk.RIGHT, fill=tk.Y)
        self.docs_listbox.bind("<<ListboxSelect>>", self.on_doc_select)
        bottom_frame = tk.Frame(docs_paned)
        docs_paned.add(bottom_frame, minsize=150)
        self.docs_detail = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, font=("Segoe UI", 9), state=tk.NORMAL)
        self.docs_detail.pack(fill=tk.BOTH, expand=True)
        self.populate_quick_docs()

        # Search tab
        self.search_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.search_tab, text=self.tr['search_tab'])
        self.create_search_widgets()

        # Menú contextual
        self.context_menu = tk.Menu(self.text_area, tearoff=0)
        self.context_menu.add_command(label=self.tr['copy'], command=self.copy_text)
        self.context_menu.add_command(label=self.tr['paste'], command=self.paste_text)
        self.context_menu.add_command(label=self.tr['cut'], command=self.cut_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.tr['count_chars'], command=self.count_characters_normal)
        self.context_menu.add_command(label=self.tr['count_chars_face'], command=self.count_characters_face)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.tr['smart_replace'], command=self.smart_replace_special_chars)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.update_font()

        # Tags de resaltado
        self.text_area.tag_configure("evento", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_letras", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_digitos", foreground="#C7158C")
        self.text_area.tag_configure("comando_id", foreground="#C7158C")
        self.text_area.tag_configure("error", foreground="#FF0000")
        self.text_area.tag_configure("search_highlight", background="yellow")
        self.text_area.tag_configure("special_warning", foreground="#FF0000")

        self.search_text = ""
        self.search_case = False
        self.search_whole = False

        # Eventos
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<<Paste>>", self.on_paste)
        self.text_area.bind("<ButtonRelease-1>", self.on_cursor_move)
        self.text_area.bind("<KeyPress-BackSpace>", self.on_backspace)
        self.text_area.bind("<KeyPress-Return>", self.on_enter)
        self.text_area.bind("<KeyPress-space>", self.on_space)
        self.text_area.bind("<Control-x>", self.on_cut)
        self.text_area.bind("<Control-c>", self.on_copy)

        self.current_file = None
        self.doukutsu_path = None
        self.current_cipher = None
        self.current_encoding = "shift_jis"
        self.raw_bytes_for_hex = None

        # Barra de estado
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text=self.tr['status_ready'], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stats_label = tk.Label(self.status_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        self.stats_label.pack(side=tk.RIGHT)
        self.update_stats()

        self.create_menus()
        self.apply_theme()

        self.root.bind("<Control-o>", lambda e: self.load_file())
        self.root.bind("<Control-s>", lambda e: self.save_project())
        self.root.bind("<Control-Shift-S>", lambda e: self.export_file())
        self.root.bind("<Control-z>", lambda e: self.undo_action())
        self.root.bind("<Control-y>", lambda e: self.redo_action())
        self.root.bind("<Control-f>", lambda e: self.focus_search_tab)
        self.root.bind("<Control-r>", lambda e: self.smart_replace_special_chars())
        self.root.bind("<Control-k>", lambda e: self.open_settings())
        self.root.bind("<F5>", lambda e: self.test_game())

        self.auto_save_timer = None
        if self.settings["auto_save"]:
            self.start_auto_save()

        self.history = []
        self.add_history_entry("Editor started")

    # ---------------------- CAMBIO DE FUENTE CON CTRL+RUEDA ------------------
    def on_ctrl_mousewheel(self, event):
        delta = event.delta
        if delta > 0:
            self.change_font_size(1)
        else:
            self.change_font_size(-1)

    def change_font_size(self, delta):
        new_size = self.base_font_size + delta
        if 8 <= new_size <= 24:
            self.base_font_size = new_size
            self.update_font()
            self.update_stats()

    # ---------------------- COMANDOS PERSONALIZABLES ------------------
    def load_base_commands(self):
        return {
            "AE+": ["0", "----", "Refill all weapon ammo."],
            "AM+": ["2", "aA--", "Give weapon W with X ammo. Use 0000 for infinite ammo."],
            "AM-": ["1", "a---", "Remove weapon W."],
            "AMJ": ["2", "ae--", "Jump to event X if the PC has weapon W."],
            "ANP": ["3", "N#d-", "Animate entity W to scriptstate X and direction Y."],
            "BOA": ["1", "#---", "Give map-boss scriptstate W"],
            "BSL": ["1", "N---", "Start boss fight with entity W. Use 0000 to end the boss fight."],
            "CAT": ["0", "----", "Instantly display text until <END."],
            "CIL": ["0", "----", "Clear illustration (during credits)."],
            "CLO": ["0", "----", "Close message box."],
            "CLR": ["0", "----", "Clear message box."],
            "CMP": ["3", "xyt-", "Change tile at coordinates W:X to type Y (with smoke)."],
            "CMU": ["1", "u---", "Change music to song W."],
            "CNP": ["3", "Nnd-", "Change all entities W to type X, direction Y."],
            "CPS": ["0", "----", "Stop propeller sound."],
            "CRE": ["0", "----", "Roll credits."],
            "CSS": ["0", "----", "Stop stream sound."],
            "DNA": ["1", "n---", "Remove all entities of type W."],
            "DNP": ["1", "N---", "Remove all entities W."],
            "ECJ": ["2", "#e--", "Jump to event X if any entities W exist."],
            "END": ["0", "----", "End current scripted event."],
            "EQ+": ["1", "E---", "Equip item W (Booster, Map System, etc)."],
            "EQ-": ["1", "E---", "Dequip item W."],
            "ESC": ["0", "----", "Quit to title screen."],
            "EVE": ["1", "e---", "Go to event W."],
            "FAC": ["1", "f---", "Show face W in message box."],
            "FAI": ["1", "d---", "Fade in with direction W."],
            "FAO": ["1", "d---", "Fade out with direction W."],
            "FL+": ["1", "F---", "Set flag W."],
            "FL-": ["1", "F---", "Clear flag W."],
            "FLA": ["0", "----", "Flash screen white."],
            "FLJ": ["2", "Fe--", "Jump to event X if flag W is set."],
            "FMU": ["0", "----", "Fade music out."],
            "FOB": ["2", "N.--", "Focus on boss W in X ticks."],
            "FOM": ["1", ".---", "Focus on PC in W ticks."],
            "FON": ["2", "N.--", "Focus on entity W in X ticks."],
            "FRE": ["0", "----", "Free game action and PC."],
            "GIT": ["1", "g---", "Display item/weapon icon (add 1000 for items)."],
            "HMC": ["0", "----", "Hide PC."],
            "INI": ["0", "----", "Reset memory and restart game."],
            "INP": ["3", "Nnd-", "Change entity W to type X, direction Y, set flag 0x8000."],
            "IT+": ["1", "i---", "Give item W."],
            "IT-": ["1", "i---", "Remove item W."],
            "ITJ": ["2", "ie--", "Jump to event X if PC has item W."],
            "KEY": ["0", "----", "Lock player controls and hide status bars until <END."],
            "LDP": ["0", "----", "Load saved game."],
            "LI+": ["1", "#---", "Recover W health."],
            "ML+": ["1", "#---", "Increase max health by W."],
            "MLP": ["0", "----", "Display map of current area."],
            "MM0": ["0", "----", "Halt PC's forward motion."],
            "MNA": ["0", "----", "Display map name."],
            "MNP": ["4", "Nxyd", "Move entity W to coordinates X:Y, direction Z."],
            "MOV": ["2", "xy--", "Move PC to coordinates W:X."],
            "MP+": ["1", "#---", "Set map flag W (0-127)."],
            "MPJ": ["1", "e---", "Jump to event W if current map flag set."],
            "MS2": ["0", "----", "Open invisible message box at top."],
            "MS3": ["0", "----", "Open message box at top."],
            "MSG": ["0", "----", "Open message box at bottom."],
            "MYB": ["1", "d---", "Bump PC in opposite direction."],
            "MYD": ["1", "d---", "Set PC direction."],
            "NCJ": ["2", "ne--", "Jump to event X if any entity type W exists."],
            "NOD": ["0", "----", "Wait for player input."],
            "NUM": ["1", "#---", "Print numeric value."],
            "PRI": ["0", "----", "Lock controls and freeze game action."],
            "PS+": ["2", "#m--", "Set teleporter slot W to event X."],
            "QUA": ["1", ".---", "Shake screen for W ticks."],
            "RMU": ["0", "----", "Resume previous music."],
            "SAT": ["0", "----", "Instantly display text until <END."],
            "SIL": ["1", "l---", "Show illustration W (credits)."],
            "SK+": ["1", "F---", "Set skipflag W."],
            "SK-": ["1", "F---", "Clear skipflag W."],
            "SKJ": ["2", "Fe--", "Jump to event X if skipflag W set."],
            "SLP": ["0", "----", "Show teleporter menu."],
            "SMC": ["0", "----", "Unhide PC."],
            "SMP": ["2", "xy--", "Subtract 1 from tile type at W:X (no smoke)."],
            "SNP": ["4", "nxyd", "Create entity type W at X:Y, direction Z."],
            "SOU": ["1", "s---", "Play sound effect W."],
            "SPS": ["0", "----", "Start propeller sound."],
            "SSS": ["1", "#---", "Start stream sound with volume W."],
            "STC": ["0", "----", "Save current time to 290.rec."],
            "SVP": ["0", "----", "Save current game."],
            "TAM": ["3", "aaA-", "Trade weapon W for X, set max ammo Y."],
            "TRA": ["4", "mexy", "Travel to map W, run event X, move to Y:Z."],
            "TUR": ["0", "----", "Instantly display text until next <MSG/END."],
            "UNI": ["1", "#---", "Set movement type (0000 normal, 0001 zero-G)."],
            "UNJ": ["2", "#e--", "Jump if movement type W."],
            "WAI": ["1", ".---", "Pause script for W ticks."],
            "WAS": ["0", "----", "Wait until PC on ground."],
            "XX1": ["1", "l---", "Island falling: 0000 crash, 0001 halt."],
            "YNJ": ["1", "e---", "Yes/No prompt; jump to event W if No."],
            "ZAM": ["0", "----", "Reset all weapon energy to zero."],
            "LRX": ["3", "eee-", "Jump to W,X,Y if Left/Right/Shoot."],
            "FNJ": ["2", "Fe--", "Jump if flag X not set."],
            "VAR": ["2", "##--", "Store XXXX into variable WWWW."],
            "VAZ": ["2", "##--", "Zero XXXX variables starting at WWWW."],
            "VAO": ["2", "##--", "Perform operation on variable."],
            "VAJ": ["4", "###e", "Compare variables and jump."],
            "RND": ["3", "###-", "Random number into variable."],
            "IMG": ["1", "#---", "Set TimgFILE.bmp over screen."],
            "PHY": ["2", "##--", "Change physics variables."],
        }

    def load_custom_commands(self):
        if os.path.exists(self.custom_commands_file):
            try:
                with open(self.custom_commands_file, "r", encoding="utf-8") as f:
                    self.custom_commands = json.load(f)
            except:
                self.custom_commands = {}
        else:
            self.custom_commands = {}
        self.save_custom_commands()

    def save_custom_commands(self):
        with open(self.custom_commands_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_commands, f, indent=2)

    def update_commands_data(self):
        self.commands_data = self.base_commands_data.copy()
        self.commands_data.update(self.custom_commands)

    def edit_custom_commands(self):
        win = Toplevel(self.root)
        win.title(self.tr['edit_custom_cmds_title'])
        win.geometry("700x500")
        win.transient(self.root)
        win.grab_set()

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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

        def add_cmd():
            name = simpledialog.askstring("Add Command", self.tr['custom_cmd_name'], parent=win)
            if not name or len(name) < 1 or len(name) > 4:
                messagebox.showerror("Error", "Command name must be 1-4 letters.", parent=win)
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
            self.save_custom_commands()
            self.update_commands_data()
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
            self.save_custom_commands()
            self.update_commands_data()
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
                self.save_custom_commands()
                self.update_commands_data()
                self.populate_quick_docs()
                tree.delete(selected[0])
                self.refresh_current_file()

        tk.Button(btn_frame, text="Add", command=add_cmd).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit", command=edit_cmd).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove", command=remove_cmd).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.tr['close_btn'], command=win.destroy).pack(side=tk.RIGHT, padx=5)

    # ---------------------- QUICK DOCS CON BUSCADOR ------------------
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

    # ---------------------- AUTO-DETECCIÓN ------------------
    def auto_detect_and_load(self, raw_data: bytes, file_path: str):
        candidates = [
            (True, "shift_jis", "Cifrado + Shift-JIS"),
            (True, "cp932", "Cifrado + CP932"),
            (False, "latin-1", "Sin cifrado + Latin-1"),
            (False, "cp850", "Sin cifrado + CP850"),
            (False, "utf-8", "Sin cifrado + UTF-8")
        ]
        best_text = None
        best_score = -1
        best_cipher = None
        best_encoding = None
        best_desc = ""

        for use_cipher, enc, desc in candidates:
            try:
                if use_cipher:
                    cipher = self.get_cipher_from_tsc(raw_data)
                    decrypted = self.decrypt_tsc(raw_data, cipher)
                else:
                    decrypted = raw_data
                    cipher = 0
                text = decrypted.decode(enc, errors="replace")
                printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                total = len(text)
                if total == 0:
                    score = 0
                else:
                    ratio = printable / total
                    bonus = 0
                    if re.search(r'<[A-Z]{1,3}[+-]?', text):
                        bonus += 20
                    if re.search(r'#[0-9A-F]{4}', text):
                        bonus += 10
                    score = ratio * 100 + bonus
                if score > best_score:
                    best_score = score
                    best_text = text
                    best_cipher = cipher if use_cipher else None
                    best_encoding = enc
                    best_desc = desc
            except:
                continue

        if best_text is not None:
            self.load_text_to_editor(best_text, file_path, best_cipher, best_encoding, apply_load_conversion=False)
            self.status_label.config(text=f"Cargado: {os.path.basename(file_path)} | {best_desc}")
            self.add_history_entry(f"Opened TSC: {os.path.basename(file_path)} (cipher={best_cipher}, enc={best_encoding})")
        else:
            messagebox.showerror("Error", "No se pudo decodificar el archivo con ninguna combinación.")

    # ---------------------- CARGA DE .tsc ------------------
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title=self.tr['open_tsc'],
            filetypes=[("Archivos TSC", "*.tsc"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return
        self.load_specific_tsc(file_path)

    def load_specific_tsc(self, file_path):
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
            self.raw_bytes_for_hex = raw_data
            self.auto_detect_and_load(raw_data, file_path)
        except Exception as e:
            messagebox.showerror(self.tr['load_error'], f"Could not load {os.path.basename(file_path)}:\n{str(e)}")

    # ---------------------- SINTÁXIS (ahora reconoce + y -) ------------------
    def check_syntax(self, text):
        errors = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == '#':
                if i+5 <= n and text[i+1:i+5].isdigit():
                    i += 5
                else:
                    errors.append({
                        'offset': i,
                        'length': min(5, n-i),
                        'message': f"Invalid event number at position {i}: expected 4 digits after '#'."
                    })
                    i += 1
            elif ch == '<':
                j = i+1
                # Permitir letras y opcionalmente '+' o '-' al final
                while j < n and (text[j].isalpha() or (j == i+1 and text[j] in '+-')):
                    j += 1
                cmd_name = text[i+1:j].upper()
                # Eliminar el '+/-' final si existe para la búsqueda en el diccionario
                base_cmd = cmd_name.rstrip('+-')
                if base_cmd in self.commands_data:
                    num_args = int(self.commands_data[base_cmd][0])
                    pos = j
                    for arg_idx in range(num_args):
                        if pos+4 > n or not text[pos:pos+4].isdigit():
                            errors.append({
                                'offset': pos,
                                'length': min(4, n-pos),
                                'message': f"Missing or invalid parameter {arg_idx+1} for command <{base_cmd}>."
                            })
                            break
                        pos += 4
                        if arg_idx < num_args - 1:
                            if pos < n and text[pos] == ':':
                                pos += 1
                            else:
                                errors.append({
                                    'offset': pos,
                                    'length': 1,
                                    'message': f"Missing ':' separator for command <{base_cmd}>."
                                })
                    i = pos
                else:
                    # No es comando conocido, marcar solo si el nombre es de 1-4 letras (sin contar +/-)
                    if len(base_cmd) <= 4:
                        errors.append({
                            'offset': i,
                            'length': min(4, n-i),
                            'message': f"Unknown command '<{cmd_name}>' at position {i}."
                        })
                    i += 1
            else:
                i += 1
        return errors

    def highlight_syntax_errors(self):
        self.text_area.tag_remove("error", "1.0", tk.END)
        texto = self.text_area.get("1.0", tk.END)
        errors = self.check_syntax(texto)
        for err in errors:
            start = f"1.0 + {err['offset']} chars"
            end = f"1.0 + {err['offset'] + err['length']} chars"
            self.text_area.tag_add("error", start, end)

    # ---------------------- RESALTADO DE SINTAXIS ------------------
    def highlight_syntax(self):
        for tag in ("evento", "comando_letras", "comando_digitos", "comando_id", "error", "special_warning"):
            self.text_area.tag_remove(tag, "1.0", tk.END)

        texto = self.text_area.get("1.0", tk.END)
        if not texto:
            return

        # Eventos
        for match in re.finditer(r'#[0-9A-Fa-f]{4}\b', texto):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.text_area.tag_add("evento", start, end)

        # Comandos (1-3 letras + opcional +/-) y opcional 4 dígitos
        patron_comando = r'<([A-Z]{1,3}[+-]?)([0-9]{4})?'
        for match in re.finditer(patron_comando, texto):
            start_cmd = match.start()
            end_letters = match.end(1)
            start_pos = f"1.0 + {start_cmd} chars"
            end_letters_pos = f"1.0 + {end_letters} chars"
            self.text_area.tag_add("comando_letras", start_pos, end_letters_pos)
            if match.group(2):
                start_digits = match.start(2)
                end_digits = match.end(2)
                start_digits_pos = f"1.0 + {start_digits} chars"
                end_digits_pos = f"1.0 + {end_digits} chars"
                self.text_area.tag_add("comando_digitos", start_digits_pos, end_digits_pos)

        # IDs sueltos
        patron_id = r'\b([0-9]{4})\b'
        for match in re.finditer(patron_id, texto):
            start_match = match.start()
            start_index = f"1.0 + {start_match} chars"
            tags = self.text_area.tag_names(start_index)
            if not any(t in tags for t in ("evento", "comando_letras", "comando_digitos")):
                start_pos = f"1.0 + {start_match} chars"
                end_pos = f"1.0 + {match.end()} chars"
                self.text_area.tag_add("comando_id", start_pos, end_pos)

        # Caracteres no estándar (çÄËÏÖÜäëïöü) - advertencia roja
        patron_extra = r'[çÄËÏÖÜäëïöü]'
        for match in re.finditer(patron_extra, texto):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.text_area.tag_add("special_warning", start, end)

        # Errores de sintaxis
        errors = self.check_syntax(texto)
        for err in errors:
            start = f"1.0 + {err['offset']} chars"
            end = f"1.0 + {err['offset'] + err['length']} chars"
            self.text_area.tag_add("error", start, end)

    # ---------------------- BÚSQUEDA Y REEMPLAZO ------------------
    def create_search_widgets(self):
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

    def on_search_text_change(self, event=None):
        self.search_text = self.search_entry.get()
        self.search_case = self.case_var.get()
        self.search_whole = self.whole_var.get()
        self.refresh_search_highlight()

    def refresh_search_highlight(self):
        self.text_area.tag_remove("search_highlight", "1.0", tk.END)
        if not self.search_text:
            self.search_status.config(text="")
            return
        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)
        try:
            regex = re.compile(pattern, flags)
            text = self.text_area.get("1.0", tk.END)
            count = 0
            for match in regex.finditer(text):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_area.tag_add("search_highlight", start, end)
                count += 1
            self.search_status.config(text=f"Found {count} matches" if count > 0 else "No matches")
        except re.error:
            self.search_status.config(text="Invalid regular expression")

    def find_next(self):
        if not self.search_text:
            return
        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)
        try:
            regex = re.compile(pattern, flags)
            text = self.text_area.get("1.0", tk.END)
            cursor = self.text_area.index(tk.INSERT)
            cursor_char = len(self.text_area.get("1.0", cursor).replace('\n', ''))
            start_pos = cursor_char
            for match in regex.finditer(text):
                if match.start() >= start_pos:
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                    self.text_area.tag_add(tk.SEL, start, end)
                    self.text_area.mark_set(tk.INSERT, end)
                    self.text_area.see(start)
                    return
            # wrap around
            if len(regex.findall(text)) > 0:
                match = regex.search(text)
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_area.tag_add(tk.SEL, start, end)
                self.text_area.mark_set(tk.INSERT, end)
                self.text_area.see(start)
                self.search_status.config(text="Wrapped around")
            else:
                self.search_status.config(text="No matches")
        except re.error:
            self.search_status.config(text="Invalid regex")

    def find_prev(self):
        if not self.search_text:
            return
        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)
        try:
            regex = re.compile(pattern, flags)
            text = self.text_area.get("1.0", tk.END)
            cursor = self.text_area.index(tk.INSERT)
            cursor_char = len(self.text_area.get("1.0", cursor).replace('\n', ''))
            prev_match = None
            for match in regex.finditer(text):
                if match.start() < cursor_char:
                    prev_match = match
                else:
                    break
            if prev_match:
                start = f"1.0 + {prev_match.start()} chars"
                end = f"1.0 + {prev_match.end()} chars"
                self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_area.tag_add(tk.SEL, start, end)
                self.text_area.mark_set(tk.INSERT, end)
                self.text_area.see(start)
            else:
                matches = list(regex.finditer(text))
                if matches:
                    match = matches[-1]
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                    self.text_area.tag_add(tk.SEL, start, end)
                    self.text_area.mark_set(tk.INSERT, end)
                    self.text_area.see(start)
                    self.search_status.config(text="Wrapped around")
                else:
                    self.search_status.config(text="No matches")
        except re.error:
            self.search_status.config(text="Invalid regex")

    def replace_current(self):
        if not self.search_text:
            return
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.find_next()
            return
        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)
        try:
            regex = re.compile(pattern, flags)
            if regex.fullmatch(selected):
                self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.insert(tk.INSERT, self.replace_entry.get())
                self.add_history_entry("Replace")
                self.refresh_search_highlight()
        except re.error:
            pass
        self.find_next()

    def replace_all(self):
        if not self.search_text:
            return
        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)
        try:
            regex = re.compile(pattern, flags)
            text = self.text_area.get("1.0", tk.END)
            new_text = re.sub(regex, self.replace_entry.get(), text)
            if new_text != text:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", new_text)
                self.add_history_entry("Replace All")
                self.refresh_search_highlight()
                self.search_status.config(text="Replace all completed")
            else:
                self.search_status.config(text="No matches found")
        except re.error:
            self.search_status.config(text="Invalid regex")

    def focus_search_tab(self, event=None):
        self.right_notebook.select(self.search_tab)
        self.search_entry.focus_set()

    # ---------------------- MÉTODOS DE EDICIÓN Y HISTORIAL ------------------
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

    def add_history_entry(self, action):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {action}"
        self.history.append(entry)
        self.history_listbox.insert(tk.END, entry)
        self.history_listbox.see(tk.END)
        if len(self.history) > 1000:
            self.history.pop(0)
            self.history_listbox.delete(0)

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
        text = self.text_area.get("1.0", tk.END)
        lines = len(text.splitlines())
        chars = len(text) - 1
        self.stats_label.config(text=f"{self.tr['lines']}: {lines}  |  {self.tr['chars']}: {chars}")

    # ---------------------- SMART REPLACE SPECIAL CHARACTERS ------------------
    def smart_replace_special_chars(self):
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            has_selection = True
        except tk.TclError:
            selected = self.text_area.get("1.0", tk.END)
            has_selection = False
        if not selected.strip():
            messagebox.showinfo(self.tr['smart_replace_title'], "No text to process.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(self.tr['smart_replace_title'])
        dialog.geometry("450x320")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        var_nn = tk.BooleanVar(value=True)
        var_accents = tk.BooleanVar(value=True)
        var_symbols = tk.BooleanVar(value=True)
        var_all = tk.BooleanVar(value=False)

        def update_all():
            if var_all.get():
                var_nn.set(True)
                var_accents.set(True)
                var_symbols.set(True)

        tk.Label(dialog, text="Select which characters to replace/remove:", font=("Segoe UI", 10, "bold")).pack(pady=10)
        tk.Checkbutton(dialog, text=self.tr['option_nn'], variable=var_nn, command=lambda: var_all.set(False)).pack(anchor=tk.W, padx=20, pady=2)
        tk.Checkbutton(dialog, text=self.tr['option_accents'], variable=var_accents, command=lambda: var_all.set(False)).pack(anchor=tk.W, padx=20, pady=2)
        tk.Checkbutton(dialog, text=self.tr['option_symbols'], variable=var_symbols, command=lambda: var_all.set(False)).pack(anchor=tk.W, padx=20, pady=2)
        tk.Checkbutton(dialog, text=self.tr['option_all'], variable=var_all, command=update_all).pack(anchor=tk.W, padx=20, pady=10)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

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
                msg = self.tr['backup_warning']
                if not messagebox.askyesno(self.tr['confirm'], msg, parent=dialog):
                    return
                if has_selection:
                    self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    self.text_area.insert(tk.INSERT, new_text)
                else:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", new_text)
                self.add_history_entry("Applied smart character replacement")
                messagebox.showinfo(self.tr['done'], "Special characters replaced/removed.", parent=dialog)
            else:
                messagebox.showinfo(self.tr['no_changes'], "No characters to replace.", parent=dialog)
            dialog.destroy()

        tk.Button(btn_frame, text=self.tr['apply_btn'], command=apply_changes, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text=self.tr['close_btn'], command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=10)

    # ---------------------- FILTER SPECIAL CHARACTERS ------------------
    def filter_special_characters(self):
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected = self.text_area.get("1.0", tk.END)
        if not selected.strip():
            messagebox.showinfo("Filter Special Characters", "No text to analyze.")
            return

        groups = {
            'ñ': 'ñ', 'Ñ': 'Ñ',
            'á': 'á', 'é': 'é', 'í': 'í', 'ó': 'ó', 'ú': 'ú',
            'Á': 'Á', 'É': 'É', 'Í': 'Í', 'Ó': 'Ó', 'Ú': 'Ú',
            'ü': 'ü', 'Ü': 'Ü', '¡': '¡', '¿': '¿',
            'ç': 'ç', 'Ä': 'Ä', 'Ë': 'Ë', 'Ï': 'Ï', 'Ö': 'Ö', 'Ü': 'Ü', 'ä': 'ä', 'ë': 'ë', 'ï': 'ï', 'ö': 'ö', 'ü': 'ü'
        }
        counts = {}
        total = 0
        for ch in selected:
            if ch in groups:
                counts[ch] = counts.get(ch, 0) + 1
                total += 1
        if total == 0:
            messagebox.showinfo("Filter Special Characters", "No special characters found.")
            return
        msg = f"Total special characters: {total}\n\n"
        for ch, cnt in sorted(counts.items()):
            msg += f"{ch}: {cnt}\n"
        msg += "\n(These characters may not display correctly in Cave Story.)"
        messagebox.showinfo("Filter Special Characters", msg)

    # ---------------------- BARRA LATERAL Y BUSCADOR DE ARCHIVOS ------------------
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
        """Elimina el archivo actual de la lista lateral sin borrarlo del disco."""
        if not self.current_file:
            messagebox.showinfo("Info", "No hay un archivo cargado.")
            return
        rel_path = None
        for rp, fp in self.all_files:
            if fp == self.current_file:
                rel_path = rp
                break
        if rel_path:
            # Eliminar de la lista de archivos
            self.all_files = [(r, f) for r, f in self.all_files if f != self.current_file]
            self.filter_files()
            # Cerrar el archivo actual y limpiar editor
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            self.current_cipher = None
            self.status_label.config(text="Archivo eliminado de la lista.")
            self.add_history_entry("Removed current file from list")
        else:
            messagebox.showinfo("Info", "El archivo actual no está en la lista lateral.")

    # ---------------------- CARGA Y GUARDADO DE ARCHIVOS ------------------
    def load_text_to_editor(self, text, file_path, cipher, encoding, apply_load_conversion=False):
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
                filetypes=[("Archivos TSC", "*.tsc"), ("Todos los archivos", "*.*")]
            )
            if not save_path:
                return
        plain_bytes = text_to_save.encode("shift_jis", errors="replace")
        if self.current_cipher is not None:
            cipher = self.current_cipher
        else:
            middle = len(plain_bytes) // 2
            cipher = plain_bytes[middle] if middle < len(plain_bytes) else 0
        middle_pos = len(plain_bytes) // 2
        encrypted = self.encrypt_tsc(plain_bytes, cipher, middle_pos)
        try:
            with open(save_path, "wb") as f:
                f.write(encrypted)
            self.current_file = save_path
            self.current_cipher = cipher
            self.status_label.config(text=f"Exported: {os.path.basename(save_path)} | Cipher: {cipher}")
            self.add_history_entry(f"Saved TSC: {os.path.basename(save_path)}")
            messagebox.showinfo(self.tr['export_success'], f"{self.tr['export_success']}\nCipher: {cipher}")
        except Exception as e:
            messagebox.showerror(self.tr['save_error'], f"{self.tr['save_error']}:\n{str(e)}")

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
                filetypes=[("Proyectos TSC Editor+", "*.cstsc"), ("Texto", "*.txt"), ("Todos", "*.*")]
            )
            if not save_path:
                return
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text_to_save)
            self.current_file = save_path
            self.status_label.config(text=f"Project saved: {os.path.basename(save_path)}")
            self.add_history_entry(f"Saved project: {os.path.basename(save_path)}")
            messagebox.showinfo(self.tr['project_saved'], self.tr['project_saved'])
        except Exception as e:
            messagebox.showerror(self.tr['save_error'], str(e))

    def load_project(self):
        file_path = filedialog.askopenfilename(
            title=self.tr['open_project_dialog_title'],
            filetypes=[("Proyectos TSC Editor+", "*.cstsc"), ("Texto", "*.txt"), ("Todos", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.load_text_to_editor(text, file_path, None, "utf-8", apply_load_conversion=False)
            self.status_label.config(text=f"Project loaded: {os.path.basename(file_path)}")
            self.add_history_entry(f"Opened project: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror(self.tr['load_error'], f"{self.tr['load_error']}:\n{str(e)}")

    def refresh_current_file(self):
        if self.current_file and os.path.isfile(self.current_file):
            if self.current_file.endswith(".cstsc"):
                self.load_project()
            else:
                self.load_specific_tsc(self.current_file)

    def confirm_save_with_errors(self):
        texto = self.text_area.get("1.0", tk.END)
        errors = self.check_syntax(texto)
        if errors:
            return messagebox.askyesno(self.tr['syntax_errors'], self.tr['syntax_errors_found'])
        return True

    # ---------------------- CONFIGURACIÓN ------------------
    def detect_language(self):
        try:
            lang_code = locale.getdefaultlocale()[0]
            if lang_code:
                if lang_code.startswith('es'):
                    return 'es'
                elif lang_code.startswith('ja'):
                    return 'jp'
        except:
            pass
        return 'en'

    def update_ui_language(self):
        self.tr = self.langs[self.current_lang]
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
        self.context_menu.entryconfig(7, label=self.tr['smart_replace'])
        self.create_menus()
        self.update_stats()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except:
                pass

    def save_settings(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def apply_theme(self):
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        select_bg = "#0078D7"
        text_bg = "#ffffff"
        paned_bg = "#f0f0f0"
        button_bg = "#f0f0f0"

        self.root.configure(bg=bg_color)
        self.main_paned.configure(bg=paned_bg, sashrelief=tk.RAISED)
        self.sidebar_frame.configure(bg=bg_color)
        self.files_tab.configure(bg=bg_color)
        self.history_tab.configure(bg=bg_color)
        self.docs_tab.configure(bg=bg_color)
        self.search_tab.configure(bg=bg_color)
        self.history_label.configure(bg=bg_color, fg=fg_color)
        self.history_listbox.configure(bg=text_bg, fg=fg_color, selectbackground=select_bg)
        self.file_listbox.configure(bg=text_bg, fg=fg_color, selectbackground=select_bg)
        self.docs_listbox.configure(bg=text_bg, fg=fg_color, selectbackground=select_bg)
        self.docs_detail.configure(bg=text_bg, fg=fg_color)
        self.text_area.configure(bg=text_bg, fg=fg_color, insertbackground=fg_color)
        self.status_label.configure(bg=bg_color, fg=fg_color)
        self.stats_label.configure(bg=bg_color, fg=fg_color)
        self.clear_btn.configure(bg=button_bg, fg=fg_color)
        self.search_label.configure(bg=bg_color, fg=fg_color)

        self.text_area.tag_configure("comando_letras", foreground="#0000FF")
        self.text_area.tag_configure("comando_digitos", foreground="#C7158C")
        self.text_area.tag_configure("comando_id", foreground="#C7158C")
        self.text_area.tag_configure("error", foreground="#FF0000")
        self.text_area.tag_configure("special_warning", foreground="#FF0000")
        self.text_area.tag_configure("search_highlight", background="yellow")

    def open_settings(self):
        win = Toplevel(self.root)
        win.title(self.tr['settings_window_title'])
        win.geometry("450x300")
        win.transient(self.root)
        win.grab_set()

        auto_var = BooleanVar(value=self.settings["auto_save"])
        def toggle_auto():
            self.settings["auto_save"] = auto_var.get()
            if self.settings["auto_save"]:
                self.start_auto_save()
            else:
                self.stop_auto_save()
            self.save_settings()
        tk.Checkbutton(win, text=self.tr['auto_save_label'], variable=auto_var, command=toggle_auto).pack(anchor=tk.W, padx=20, pady=10)

        tk.Label(win, text=self.tr['language_label']).pack(anchor=tk.W, padx=20, pady=(10,0))
        lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.Combobox(win, textvariable=lang_var, values=['en', 'es', 'jp'], state="readonly")
        lang_menu.pack(anchor=tk.W, padx=20, pady=5)

        def apply_settings():
            if lang_var.get() != self.current_lang:
                self.current_lang = lang_var.get()
                self.settings["language"] = self.current_lang
                self.update_ui_language()
            self.save_settings()
            win.destroy()

        tk.Button(win, text=self.tr['apply_btn'], command=apply_settings).pack(pady=20)
        tk.Button(win, text=self.tr['close_btn'], command=win.destroy).pack(pady=5)

    # ---------------------- AUTO-GUARDADO (6 minutos) ------------------
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

    # ---------------------- MENÚS ------------------
    def create_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['file_menu'], menu=file_menu)
        file_menu.add_command(label=self.tr['open_tsc'], command=self.load_file, accelerator="Ctrl+O")
        file_menu.add_command(label=self.tr['open_project'], command=self.load_project)
        file_menu.add_command(label=self.tr['open_folder'], command=self.load_folder)
        file_menu.add_command(label=self.tr['delete_from_list'], command=self.delete_current_from_list)
        file_menu.add_separator()
        file_menu.add_command(label=self.tr['export_tsc'], command=self.export_file, accelerator="Ctrl+Shift+S")
        file_menu.add_command(label=self.tr['save_project'], command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label=self.tr['settings'], command=self.open_settings, accelerator="Ctrl+K")
        file_menu.add_separator()
        file_menu.add_command(label=self.tr['exit'], command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['edit_menu'], menu=edit_menu)
        edit_menu.add_command(label=self.tr['undo'], command=self.undo_action, accelerator="Ctrl+Z")
        edit_menu.add_command(label=self.tr['redo'], command=self.redo_action, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label=self.tr['check_syntax'], command=self.check_syntax_cmd)
        edit_menu.add_separator()
        edit_menu.add_command(label=self.tr['smart_replace'], command=self.smart_replace_special_chars, accelerator="Ctrl+R")

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['view_menu'], menu=view_menu)
        view_menu.add_command(label=self.tr['font_size'], command=self.open_view_options)
        view_menu.add_command(label=self.tr['hex_dump'], command=self.show_hex_dump)
        view_menu.add_command(label=self.tr['see_quick_docs'], command=self.show_quick_docs)
        view_menu.add_command(label=self.tr['search_tab'], command=self.focus_search_tab)
        view_menu.add_command(label=self.tr['edit_custom_cmds'], command=self.edit_custom_commands)

        font_submenu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label=self.tr['font_submenu'], menu=font_submenu)
        for f in self.available_fonts:
            font_submenu.add_radiobutton(label=f, variable=self.current_font_name, value=f, command=self.update_font)

        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['run_menu'], menu=run_menu)
        run_menu.add_command(label=self.tr['find_doukutsu'], command=self.lookup_doukutsu)
        run_menu.add_command(label=self.tr['test_game'], command=self.test_game, accelerator="F5")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['help_menu'], menu=help_menu)
        help_menu.add_command(label=self.tr['about'], command=self.show_about)

    def check_syntax_cmd(self):
        texto = self.text_area.get("1.0", tk.END)
        errors = self.check_syntax(texto)
        if errors:
            msg = f"{self.tr['syntax_errors']}:\n\n"
            for err in errors:
                msg += f"- {err['message']}\n"
            messagebox.showwarning(self.tr['syntax_error_window_title'], msg)
        else:
            messagebox.showinfo(self.tr['syntax_error_window_title'], self.tr['syntax_no_errors'])
        self.highlight_syntax_errors()

    def show_quick_docs(self):
        self.right_notebook.select(self.docs_tab)

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

    def open_view_options(self):
        win = Toplevel(self.root)
        win.title(self.tr['font_size'])
        win.geometry("300x150")
        current_size = self.base_font_size
        tk.Label(win, text="Tamaño:").pack(pady=5)
        scale = Scale(win, from_=8, to=24, orient=tk.HORIZONTAL, command=lambda v: self.change_font(int(float(v))))
        scale.set(current_size)
        scale.pack(pady=5, padx=20, fill=tk.X)
        Button(win, text=self.tr['close_btn'], command=win.destroy).pack(pady=10)

    def change_font(self, new_size):
        self.base_font_size = new_size
        self.update_font()

    def update_font(self):
        font_name = self.current_font_name.get()
        self.text_area.config(font=(font_name, self.base_font_size))
        self.text_area.tag_configure("evento", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_letras", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.delayed_highlight()

    def delayed_highlight(self):
        self.root.after(50, self.highlight_syntax)

    def count_characters_normal(self):
        self.count_characters(with_face=False)

    def count_characters_face(self):
        self.count_characters(with_face=True)

    def count_characters(self, with_face):
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
            subprocess.Popen([self.doukutsu_path], cwd=os.path.dirname(self.doukutsu_path))
            self.status_label.config(text=self.tr['game_launched'])
            self.add_history_entry("Game launched")
        except Exception as e:
            messagebox.showerror(self.tr['exe_not_found'], str(e))

    def show_about(self):
        messagebox.showinfo(self.tr['about'],
            "TSC Editor+ v23.0\n"
            "Editor profesional de archivos .tsc de Cave Story\n"
            "Cifrado compatible con Booster's Lab (Carrot Lord)\n"
            "Características: resaltado de sintaxis, historial, contadores, conteo de caracteres,\n"
            "documentación rápida con buscador, búsqueda/reemplazo con resaltado, auto-guardado cada 6 minutos,\n"
            "comandos personalizables (con +/-), cambio rápido de fuente con Ctrl+rueda, soporte multilenguaje.\n"
            "Atajos: Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Z, Ctrl+Y, Ctrl+F (buscar), Ctrl+R (reemplazar acentos), Ctrl+K, F5")

    def show_hex_dump(self):
        if self.raw_bytes_for_hex is None:
            messagebox.showwarning(self.tr['hex_info'], self.tr['hex_info'])
            return
        hex_str = binascii.hexlify(self.raw_bytes_for_hex[:512], ' ').decode('ascii')
        win = Toplevel(self.root)
        win.title(self.tr['hex_window_title'])
        win.geometry("800x400")
        text_w = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Courier New", 9))
        text_w.pack(fill=tk.BOTH, expand=True)
        text_w.insert(tk.END, hex_str)
        text_w.config(state=tk.DISABLED)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    # ---------------------- MÉTODOS DE CIFRADO ------------------
    @staticmethod
    def get_cipher_from_tsc(data: bytes) -> int:
        newline_dict = {}
        for i in range(len(data) - 1):
            b1 = data[i]
            b2 = data[i+1]
            if (b1 - b2) == 3:
                newline_dict[b1] = newline_dict.get(b1, 0) + 1
        if not newline_dict:
            return 0
        top_key = max(newline_dict, key=newline_dict.get)
        return top_key - 0x0D

    @staticmethod
    def decrypt_tsc(data: bytes, cipher: int) -> bytes:
        if cipher == 0:
            return data
        result = bytearray()
        for b in data:
            if b == cipher:
                result.append(cipher)
            else:
                val = b - cipher
                if val < 0:
                    val = 0
                result.append(val)
        return bytes(result)

    @staticmethod
    def encrypt_tsc(plain: bytes, cipher: int, middle_pos: int) -> bytes:
        if cipher == 0:
            return plain
        result = bytearray()
        for i, b in enumerate(plain):
            if i == middle_pos:
                result.append(cipher)
            else:
                val = b + cipher
                if val > 255:
                    val = 255
                result.append(val)
        return bytes(result)

if __name__ == "__main__":
    root = tk.Tk()
    app = TSCEditor(root)
    root.mainloop()
