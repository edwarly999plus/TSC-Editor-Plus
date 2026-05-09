#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Añadir la carpeta 'Dependencias' al path si existe
deps_path = os.path.join(os.path.dirname(__file__), "Dependencias")
if os.path.isdir(deps_path):
    sys.path.insert(0, deps_path)

# Intentar importar PIL, pero continuar si falla
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None
    ImageTk = None
    print("Advertencia: Pillow no instalado. Las imágenes de caras no estarán disponibles.")

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, Toplevel, Scale, Button, BooleanVar, ttk, simpledialog
import subprocess
import re
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
                'export_tsc': 'Export .tsc...',
                'save_project': 'Save project .cstsc...',
                'settings': 'Settings...',
                'exit': 'Exit',
                'edit_menu': 'Edit',
                'undo': 'Undo',
                'redo': 'Redo',
                'search': 'Search...',
                'view_menu': 'View',
                'font_size': 'Font size...',
                'hex_dump': 'Hex dump of current file...',
                'show_history': 'Show History',
                'see_quick_docs': 'See Quick Docs',
                'spanish_mode': 'Spanish compatibility mode',
                'highlight_converted': 'Highlight converted chars (Spanish mode)',
                'edit_rules': 'Edit conversion rules...',
                'font_submenu': 'Font',
                'run_menu': 'Run',
                'find_doukutsu': 'Find doukutsu.exe...',
                'test_game': 'Test (F5)',
                'help_menu': 'Help',
                'tsc_commands': 'TSC commands...',
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
                'dark_theme_label': 'Dark theme',
                'auto_save_label': 'Auto-save project (.cstsc)',
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
            },
            'es': {
                'window_title': 'TSC Editor+ - Edición Profesional',
                'file_menu': 'Archivo',
                'open_tsc': 'Abrir .tsc...',
                'open_project': 'Abrir proyecto .cstsc...',
                'open_folder': 'Abrir carpeta de proyectos...',
                'export_tsc': 'Exportar .tsc...',
                'save_project': 'Guardar proyecto .cstsc...',
                'settings': 'Configuración...',
                'exit': 'Salir',
                'edit_menu': 'Editar',
                'undo': 'Deshacer',
                'redo': 'Rehacer',
                'search': 'Buscar...',
                'view_menu': 'Ver',
                'font_size': 'Tamaño de fuente...',
                'hex_dump': 'Ver hexadecimal del archivo actual...',
                'show_history': 'Mostrar historial',
                'see_quick_docs': 'Ver documentación rápida',
                'spanish_mode': 'Modo compatibilidad española',
                'highlight_converted': 'Resaltar caracteres convertidos',
                'edit_rules': 'Configurar reglas de conversión...',
                'font_submenu': 'Fuente',
                'run_menu': 'Ejecutar',
                'find_doukutsu': 'Buscar doukutsu.exe...',
                'test_game': 'Probar (F5)',
                'help_menu': 'Ayuda',
                'tsc_commands': 'Comandos TSC...',
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
                'dark_theme_label': 'Tema oscuro',
                'auto_save_label': 'Auto-guardar proyecto (.cstsc)',
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
            },
            'jp': {
                'window_title': 'TSC Editor+ - プロフェッショナル版',
                'file_menu': 'ファイル',
                'open_tsc': '.tscを開く...',
                'open_project': '.cstscプロジェクトを開く...',
                'open_folder': 'プロジェクトフォルダを開く...',
                'export_tsc': '.tscにエクスポート...',
                'save_project': 'プロジェクトを保存.cstsc...',
                'settings': '設定...',
                'exit': '終了',
                'edit_menu': '編集',
                'undo': '元に戻す',
                'redo': 'やり直し',
                'search': '検索...',
                'view_menu': '表示',
                'font_size': 'フォントサイズ...',
                'hex_dump': '現在のファイルの16進ダンプ...',
                'show_history': '履歴を表示',
                'see_quick_docs': 'クイックドキュメントを表示',
                'spanish_mode': 'スペイン語互換モード',
                'highlight_converted': '変換文字をハイライト',
                'edit_rules': '変換ルールを編集...',
                'font_submenu': 'フォント',
                'run_menu': '実行',
                'find_doukutsu': 'doukutsu.exeを検索...',
                'test_game': 'テスト（F5）',
                'help_menu': 'ヘルプ',
                'tsc_commands': 'TSCコマンド...',
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
                'dark_theme_label': 'ダークテーマ',
                'auto_save_label': 'プロジェクトを自動保存（.cstsc）',
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
            }
        }

        self.current_lang = self.detect_language()
        self.tr = self.langs[self.current_lang]

        # ---------- DOCUMENTACIÓN DE COMANDOS ----------
        self.commands_data = {
            "AE+": ["0", "----", "Refill all weapon ammo."],
            "AM+": ["2", "aA--", "Give weapon W with X ammo. Use 0000 for infinite ammo. If you already have the weapon, adds to max ammo."],
            "AM-": ["1", "a---", "Remove weapon W."],
            "AMJ": ["2", "ae--", "Jump to event X if the PC has weapon W."],
            "ANP": ["3", "N#d-", "Give all entities W scriptstate X and direction Y. Used for animation."],
            "BOA": ["1", "#---", "Give map-boss (eg Omega) scriptstate W"],
            "BSL": ["1", "N---", "Start boss fight with entity W. Use 0000 to end the boss fight."],
            "CAT": ["0", "----", "Instantly display text. Use before a <MSG/2/3; works until <END. Same command as <SAT."],
            "CIL": ["0", "----", "Clear illustration (during credits)."],
            "CLO": ["0", "----", "Close message box."],
            "CLR": ["0", "----", "Clear message box."],
            "CMP": ["3", "xyt-", "Change the tile at coordinates W:X to type Y. Produces smoke."],
            "CMU": ["1", "u---", "Change music to song W."],
            "CNP": ["3", "Nnd-", "Change all entities W to type X with direction Y."],
            "CPS": ["0", "----", "Stops the propeller sound."],
            "CRE": ["0", "----", "Rolls credits."],
            "CSS": ["0", "----", "Stops the stream sound."],
            "DNA": ["1", "n---", "Remove all entities of type W."],
            "DNP": ["1", "N---", "Remove all entities W."],
            "ECJ": ["2", "#e--", "Jump to event X if any entities W exist."],
            "END": ["0", "----", "End the current scripted event."],
            "EQ+": ["1", "E---", "Equip item W. Valid values: 0001 Booster v0.8, 0002 Map System, 0004 Arms Barrier, 0008 Turbocharge, 0016 Curly's Air Tank, 0032 Booster v2.0, 0064 Mimiga Mask, 0128 Whimsical Star, 0256 Nikumaru Counter."],
            "EQ-": ["1", "E---", "Dequip item W."],
            "ESC": ["0", "----", "Quit to title screen."],
            "EVE": ["1", "e---", "Go to event W."],
            "FAC": ["1", "f---", "Show face W in the message box."],
            "FAI": ["1", "d---", "Fade in with direction W."],
            "FAO": ["1", "d---", "Fade out with direction W."],
            "FL+": ["1", "F---", "Set flag W. Using flags over 8000 is inadvisable."],
            "FL-": ["1", "F---", "Clear flag W."],
            "FLA": ["0", "----", "Flash the screen white."],
            "FLJ": ["2", "Fe--", "Jump to event X if flag W is set."],
            "FMU": ["0", "----", "Fade the music out."],
            "FOB": ["2", "N.--", "Focus on boss W in X ticks. Use X > 0."],
            "FOM": ["1", ".---", "Focus on the PC in W ticks. Use W > 0."],
            "FON": ["2", "N.--", "Focus on entity W in X ticks. Use X > 0."],
            "FRE": ["0", "----", "Free game action and the PC."],
            "GIT": ["1", "g---", "Display an item or weapon icon above the message box. Add 1000 to W for items. Use 0000 to remove."],
            "HMC": ["0", "----", "Hide the PC."],
            "INI": ["0", "----", "Reset memory and restart game."],
            "INP": ["3", "Nnd-", "Change entity W to type X with direction Y and set entity flag 100 (0x8000)."],
            "IT+": ["1", "i---", "Give item W."],
            "IT-": ["1", "i---", "Remove item W."],
            "ITJ": ["2", "ie--", "Jump to event X if the PC has item W."],
            "KEY": ["0", "----", "Lock player controls and hide status bars until <END."],
            "LDP": ["0", "----", "Load the saved game."],
            "LI+": ["1", "#---", "Recover W health."],
            "ML+": ["1", "#---", "Increase the current and maximum health by W."],
            "MLP": ["0", "----", "Display a map of the current area."],
            "MM0": ["0", "----", "Halt the PC's forward motion."],
            "MNA": ["0", "----", "Display the map name."],
            "MNP": ["4", "Nxyd", "Move entity W to coordinates X:Y with direction Z."],
            "MOV": ["2", "xy--", "Move the PC to coordinates W:X."],
            "MP+": ["1", "#---", "Set map flag W. Map flags cannot be unset. Highest usable flag is 127."],
            "MPJ": ["1", "e---", "Jump to event W if the map flag for the current area is set."],
            "MS2": ["0", "----", "Open an invisible message box at the top of screen."],
            "MS3": ["0", "----", "Open a message box at the top of screen."],
            "MSG": ["0", "----", "Open a message box at the bottom of the screen."],
            "MYB": ["1", "d---", "Causes the PC to hop in the direction opposite of W. Using up or down causes the jump to be vertical."],
            "MYD": ["1", "d---", "Causes the PC to face direction W."],
            "NCJ": ["2", "ne--", "Jump to event X if any entity of type W exists."],
            "NOD": ["0", "----", "Wait for player input before resuming script."],
            "NUM": ["1", "#---", "Prints the value [4a5b34+W*4] to the message box. Use 0000 to print the last used W from compatible commands (eg AM+)."],
            "PRI": ["0", "----", "Lock player controls and freeze game action."],
            "PS+": ["2", "#m--", "Set teleporter slot W to event X. Selecting slot W while using the teleporter menu will jump to event X."],
            "QUA": ["1", ".---", "Shake the screen for W ticks."],
            "RMU": ["0", "----", "Resume the song last played."],
            "SAT": ["0", "----", "Instantly display text. Use before a <MSG/2/3; works until <END. Same command as <CAT."],
            "SIL": ["1", "l---", "Show illustration W (during credits)."],
            "SK+": ["1", "F---", "Set skipflag W. Not saved to Profile.dat."],
            "SK-": ["1", "F---", "Clear skipflag W."],
            "SKJ": ["2", "Fe--", "Jump to event X if skipflag W is set."],
            "SLP": ["0", "----", "Show the teleporter menu."],
            "SMC": ["0", "----", "Unhides the PC."],
            "SMP": ["2", "xy--", "Subtract 1 from the tile type at coordinates W:X. Does not create smoke."],
            "SNP": ["4", "nxyd", "Create an entity of type W at coordinates X:Y with direction Z."],
            "SOU": ["1", "s---", "Play sound effect W."],
            "SPS": ["0", "----", "Start the propeller sound."],
            "SSS": ["1", "#---", "Start the stream sound with volume W."],
            "STC": ["0", "----", "Save current time to 290.rec."],
            "SVP": ["0", "----", "Saves current game."],
            "TAM": ["3", "aaA-", "Trade weapon W for weapon X and set max ammo to Y. Use 0000 to keep the same amount of ammo."],
            "TRA": ["4", "mexy", "Travel to map W, run event X, and move the PC to coordinates Y:Z."],
            "TUR": ["0", "----", "Instantly display text. Use after a <MSG/2/3; works until another <MSG/2/3 or an <END."],
            "UNI": ["1", "#---", "Set character movement type. Use 0000 for normal, 0001 for zero-G and 0002 to disallow movement."],
            "UNJ": ["2", "#e--", "Jump to event X if movement is of type W (0000 for normal, 0001 for zero-G)."],
            "WAI": ["1", ".---", "Pause script for W ticks."],
            "WAS": ["0", "----", "Pause script until character is on ground."],
            "XX1": ["1", "l---", "Show the island falling in manner W. Use 0000 to have it crash and 0001 to have it stop midway."],
            "YNJ": ["1", "e---", "Prompt Yes/No; jump to event W if No is selected."],
            "ZAM": ["0", "----", "Sets all weapon energy to zero."],
            "LRX": ["3", "eee-", "Jump to W, X, or Y if player moves Left, Right, or Shoots."],
            "FNJ": ["2", "Fe--", "Jump if flag X is not set."],
            "VAR": ["2", "##--", "Puts XXXX into variable WWWW"],
            "VAZ": ["2", "##--", "Zeros XXXX variables, starting at variable WWWW"],
            "VAO": ["2", "##--", "Performs operation $ on WWWW using XXXX. Valid values of $ are listed in help file."],
            "VAJ": ["4", "###e", "Compare XXXX to WWWW using method YYYY, if true jump to ZZZZ. YYYY is listed in the help file."],
            "RND": ["3", "###-", "Puts random # between WWWW (min) and XXXX (max) into variable YYYY."],
            "IMG": ["1", "#---", "will set TimgFILE.bmp over the screen. The 'tag' for the file name must be exactly 4 characters."],
            "PHY": ["2", "##--", "Change physics variables. List in help file. BE SURE TO DEFINE WHEN STARTING YOUR GAME BEFORE PLAYER IS ABLE TO MOVE!"],
        }

        self.face_names = {
            "0000": "Nothing",
            "0001": "Sue Smile",
            "0002": "Sue Serious",
            "0003": "Sue Angry",
            "0004": "Sue Injured",
            "0005": "Balrog Serious",
            "0006": "Toroko",
            "0007": "King",
            "0008": "Toroko Scared",
            "0009": "Jack",
            "0010": "Kazuma",
            "0011": "Toroko Red",
            "0012": "Igor",
            "0013": "Jenka",
            "0014": "Balrog Happy!",
            "0015": "Misery",
            "0016": "Misery Happy!",
            "0017": "Booster Injured",
            "0018": "Booster",
            "0019": "Curly Smile",
            "0020": "Curly Sad",
            "0021": "The Doctor",
            "0022": "Momorin",
            "0023": "Balrog Injured",
            "0024": "A Random Surface Robot",
            "0025": "Curly Serious",
            "0026": "Misery Angry",
            "0027": "Human Sue? (Unused)",
            "0028": "Itoh",
            "0029": "Ballos",
            "0030": "Out Of Bounds!",
        }

        # ---------- CONFIGURACIÓN ----------
        self.settings_file = os.path.join(os.path.dirname(sys.argv[0]), "settings.json")
        self.settings = {
            "dark_theme": False,
            "auto_save": False,
            "auto_save_path": "",
            "language": self.current_lang,
            "show_history": True,
            "show_quick_docs": False
        }
        self.load_settings()
        if self.settings.get("language") != self.current_lang:
            self.current_lang = self.settings["language"]
            self.tr = self.langs[self.current_lang]

        self.spanish_mode = BooleanVar(value=False)
        self.highlight_converted = BooleanVar(value=False)
        self.rules_file = os.path.join(os.path.dirname(sys.argv[0]), "rules_spanish.json")
        self.load_rules()

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

        # Cargar imágenes de caras desde Face.png (solo si PIL está disponible)
        self.face_images = {}
        if PIL_AVAILABLE:
            self.load_face_images()

        # ---------- INTERFAZ PRINCIPAL ----------
        self.main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Barra lateral izquierda (solo pestaña Files)
        self.sidebar_frame = tk.Frame(self.main_paned, width=250, height=700)
        self.main_paned.add(self.sidebar_frame, minsize=180, width=250)
        self.files_tab = tk.Frame(self.sidebar_frame)
        self.files_tab.pack(fill=tk.BOTH, expand=True)
        # Buscador
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

        # Panel central: editor de texto
        self.text_area = scrolledtext.ScrolledText(
            self.main_paned, wrap=tk.WORD, undo=True, autoseparators=True, maxundo=50
        )
        self.main_paned.add(self.text_area, minsize=400)

        # Panel derecho: Notebook con pestañas History y Quick Docs
        self.right_notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.right_notebook, minsize=250, width=250)

        # --- Pestaña History ---
        self.history_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.history_tab, text=self.tr['history'])
        self.history_label = tk.Label(self.history_tab, text=self.tr['history'], font=("Segoe UI", 10, "bold"))
        self.history_label.pack(pady=5)
        self.history_listbox = tk.Listbox(self.history_tab, bg="#f0f0f0", selectbackground="#0078D7")
        self.history_scrollbar = tk.Scrollbar(self.history_tab, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Pestaña Quick Docs ---
        self.docs_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.docs_tab, text=self.tr['quick_docs'])
        # Dividir la pestaña en dos: lista de comandos arriba, detalles abajo
        docs_paned = tk.PanedWindow(self.docs_tab, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        docs_paned.pack(fill=tk.BOTH, expand=True)

        # Lista de comandos (scroll)
        top_frame = tk.Frame(docs_paned)
        docs_paned.add(top_frame, minsize=150)
        self.docs_listbox = tk.Listbox(top_frame, bg="#f0f0f0", selectbackground="#0078D7")
        scrollbar_docs = tk.Scrollbar(top_frame, orient=tk.VERTICAL, command=self.docs_listbox.yview)
        self.docs_listbox.config(yscrollcommand=scrollbar_docs.set)
        self.docs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_docs.pack(side=tk.RIGHT, fill=tk.Y)
        self.docs_listbox.bind("<<ListboxSelect>>", self.on_doc_select)

        # Área de detalles (texto)
        bottom_frame = tk.Frame(docs_paned)
        docs_paned.add(bottom_frame, minsize=150)
        self.docs_detail = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, font=("Segoe UI", 9), state=tk.NORMAL)
        self.docs_detail.pack(fill=tk.BOTH, expand=True)

        self.populate_quick_docs()

        # Control de visibilidad del panel derecho
        self.right_panel_visible = True
        self.toggle_history()  # aplica el estado inicial según settings["show_history"]

        # Menú contextual sobre el editor
        self.context_menu = tk.Menu(self.text_area, tearoff=0)
        self.context_menu.add_command(label=self.tr['copy'], command=self.copy_text)
        self.context_menu.add_command(label=self.tr['paste'], command=self.paste_text)
        self.context_menu.add_command(label=self.tr['cut'], command=self.cut_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.tr['count_chars'], command=self.count_characters_normal)
        self.context_menu.add_command(label=self.tr['count_chars_face'], command=self.count_characters_face)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.tr['tsc_commands'], command=self.show_command_info)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.update_font()

        # Tags de resaltado
        self.text_area.tag_configure("evento", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_letras", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_digitos", foreground="#C7158C")
        self.text_area.tag_configure("comando_id", foreground="#C7158C")
        self.text_area.tag_configure("caracter_convertido", foreground="#FF0000")

        # Eventos para contadores e historial
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
        self.current_folder = None
        self.all_files = []

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
        self.root.bind("<Control-f>", lambda e: self.open_search_dialog())
        self.root.bind("<Control-k>", lambda e: self.open_settings())
        self.root.bind("<F5>", lambda e: self.test_game())

        self.auto_save_timer = None
        if self.settings["auto_save"]:
            self.start_auto_save()

        self.history = []
        self.add_history_entry("Editor started")

    # ---------------------- CARGA DE CARAS (con PIL opcional) ------------------
    def load_face_images(self):
        script_dir = os.path.dirname(sys.argv[0])
        face_path = os.path.join(script_dir, "Face.png")
        if not os.path.isfile(face_path):
            return
        try:
            img = Image.open(face_path)
            if img.size != (288, 240):
                print("Face.png size is not 288x240, may cause errors")
            tile_width, tile_height = 48, 48
            cols = img.width // tile_width  # 6
            rows = img.height // tile_height # 5
            id_counter = 0
            for row in range(rows):
                for col in range(cols):
                    left = col * tile_width
                    top = row * tile_height
                    right = left + tile_width
                    bottom = top + tile_height
                    tile = img.crop((left, top, right, bottom))
                    photo = ImageTk.PhotoImage(tile)
                    face_id = f"{id_counter:04d}"
                    self.face_images[face_id] = photo
                    id_counter += 1
            # Añadir manualmente el ID 0030 (Out of Bounds) si no hay suficiente
            if "0030" not in self.face_images:
                self.face_images["0030"] = None
        except Exception as e:
            print(f"Could not load Face.png: {e}")

    # ---------------------- QUICK DOCS ------------------
    def populate_quick_docs(self):
        self.docs_listbox.delete(0, tk.END)
        cmds = sorted(self.commands_data.keys())
        for cmd in cmds:
            self.docs_listbox.insert(tk.END, cmd)

    def on_doc_select(self, event):
        selection = self.docs_listbox.curselection()
        if not selection:
            return
        cmd = self.docs_listbox.get(selection[0])
        if cmd in self.commands_data:
            num_args, types, desc = self.commands_data[cmd]
            # Construir sintaxis
            if num_args == "0":
                syntax = f"<{cmd}>"
            else:
                arg_list = []
                for i in range(int(num_args)):
                    arg_char = types[i] if i < len(types) else "?"
                    arg_list.append(f"<{arg_char}>")
                syntax = f"<{cmd} " + " ".join(arg_list) + ">"
            # Obtener detalles adicionales
            extra = ""
            if cmd == "FAC":
                extra = f"\n{self.tr['face_name']}: {self.face_names.get('0000', '?')} (el ID determina la cara)"
            elif cmd == "CMU":
                extra = f"\n{self.tr['music_name']}: Ver lista de IDs de música (0010 = Get Item!, etc.)"
            info = f"{self.tr['command']}: {cmd}\n\n"
            info += f"{self.tr['syntax']}: {syntax}\n\n"
            info += f"{self.tr['description']}: {desc}\n"
            if extra:
                info += f"\n{self.tr['details']}:{extra}"
            self.docs_detail.config(state=tk.NORMAL)
            self.docs_detail.delete(1.0, tk.END)
            self.docs_detail.insert(tk.END, info)
            self.docs_detail.config(state=tk.DISABLED)

    # ---------------------- CONTEOS DE CARACTERES ------------------
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
        # Eliminar comandos TSC (cualquier cosa entre < y >) y eventos (#XXXX)
        clean_text = re.sub(r'<[^>]+>', '', selected)
        clean_text = re.sub(r'#[0-9A-Fa-f]{4}\b', '', clean_text)
        char_count = len(clean_text)
        limit = 27 if with_face else 34
        if char_count <= limit:
            msg = f"{self.tr['fits']} ({self.tr['limit']}: {limit})"
        else:
            msg = f"{self.tr['not_fits']} ({self.tr['limit']}: {limit})"
        title = self.tr['count_face_title'] if with_face else self.tr['count_normal_title']
        messagebox.showinfo(title, f"{msg}\n\nCharacters: {char_count}\nLimit: {limit}")

    # ---------------------- MÉTODOS DE EDICIÓN ------------------
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

    # ---------------------- IDIOMA ------------------
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
        self.context_menu.entryconfig(0, label=self.tr['copy'])
        self.context_menu.entryconfig(1, label=self.tr['paste'])
        self.context_menu.entryconfig(2, label=self.tr['cut'])
        self.context_menu.entryconfig(4, label=self.tr['count_chars'])
        self.context_menu.entryconfig(5, label=self.tr['count_chars_face'])
        self.context_menu.entryconfig(7, label=self.tr['tsc_commands'])
        self.create_menus()
        self.update_stats()
        # Forzar actualización de la pestaña de documentación si está visible
        self.on_doc_select(None)

    # ---------------------- HISTORIAL ------------------
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

    # ---------------------- CONFIGURACIÓN ------------------
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
        if self.settings["dark_theme"]:
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            select_bg = "#3c3c3c"
            text_bg = "#1e1e1e"
            paned_bg = "#2b2b2b"
            button_bg = "#3c3c3c"
        else:
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

        if self.settings["dark_theme"]:
            self.text_area.tag_configure("comando_letras", foreground="#88AAFF")
            self.text_area.tag_configure("comando_digitos", foreground="#FF88BB")
            self.text_area.tag_configure("comando_id", foreground="#FF88BB")
            self.text_area.tag_configure("caracter_convertido", foreground="#FF0000")
        else:
            self.text_area.tag_configure("comando_letras", foreground="#0000FF")
            self.text_area.tag_configure("comando_digitos", foreground="#C7158C")
            self.text_area.tag_configure("comando_id", foreground="#C7158C")
            self.text_area.tag_configure("caracter_convertido", foreground="#FF0000")

    def open_settings(self):
        win = Toplevel(self.root)
        win.title(self.tr['settings_window_title'])
        win.geometry("450x350")
        win.transient(self.root)
        win.grab_set()

        dark_var = BooleanVar(value=self.settings["dark_theme"])
        def toggle_dark():
            self.settings["dark_theme"] = dark_var.get()
            self.apply_theme()
            self.save_settings()
        tk.Checkbutton(win, text=self.tr['dark_theme_label'], variable=dark_var, command=toggle_dark).pack(anchor=tk.W, padx=20, pady=5)

        auto_var = BooleanVar(value=self.settings["auto_save"])
        def toggle_auto():
            self.settings["auto_save"] = auto_var.get()
            if self.settings["auto_save"]:
                self.start_auto_save()
            else:
                self.stop_auto_save()
            self.save_settings()
        tk.Checkbutton(win, text=self.tr['auto_save_label'], variable=auto_var, command=toggle_auto).pack(anchor=tk.W, padx=20, pady=5)

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

        tk.Button(win, text=self.tr['apply_btn'], command=apply_settings).pack(pady=10)
        tk.Button(win, text=self.tr['close_btn'], command=win.destroy).pack(pady=5)

    # ---------------------- AUTO-GUARDADO ------------------
    def start_auto_save(self):
        if self.auto_save_timer:
            self.root.after_cancel(self.auto_save_timer)
        self.schedule_auto_save()

    def schedule_auto_save(self):
        if self.settings["auto_save"] and self.current_file and self.current_file.endswith(".cstsc"):
            self.save_project()
        self.auto_save_timer = self.root.after(30000, self.schedule_auto_save)

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
        edit_menu.add_command(label=self.tr['search'], command=self.open_search_dialog, accelerator="Ctrl+F")

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr['view_menu'], menu=view_menu)
        view_menu.add_command(label=self.tr['font_size'], command=self.open_view_options)
        view_menu.add_command(label=self.tr['hex_dump'], command=self.show_hex_dump)
        # Opciones para mostrar/ocultar el panel derecho y seleccionar pestaña
        view_menu.add_checkbutton(label=self.tr['show_history'], 
                                  variable=tk.BooleanVar(value=self.right_panel_visible),
                                  command=self.toggle_history)
        view_menu.add_command(label=self.tr['see_quick_docs'], command=self.show_quick_docs)
        view_menu.add_separator()
        view_menu.add_checkbutton(label=self.tr['spanish_mode'], 
                                  variable=self.spanish_mode, 
                                  command=lambda: self.refresh_current_file())
        view_menu.add_checkbutton(label=self.tr['highlight_converted'], 
                                  variable=self.highlight_converted, 
                                  command=self.delayed_highlight)
        view_menu.add_command(label=self.tr['edit_rules'], command=self.edit_rules)

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
        help_menu.add_command(label=self.tr['tsc_commands'], command=self.show_tsc_docs)
        help_menu.add_command(label=self.tr['about'], command=self.show_about)

    def toggle_history(self):
        if self.right_panel_visible:
            self.main_paned.remove(self.right_notebook)
            self.right_panel_visible = False
            self.settings["show_history"] = False
        else:
            self.main_paned.add(self.right_notebook, minsize=250, width=250)
            self.right_panel_visible = True
            self.settings["show_history"] = True
        self.save_settings()

    def show_quick_docs(self):
        # Asegurar que el panel derecho esté visible y seleccionar la pestaña Quick Docs
        if not self.right_panel_visible:
            self.toggle_history()
        self.right_notebook.select(self.docs_tab)

    # ---------------------- CIFRADO CARROT LORD ------------------
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

    # ---------------------- CARGA Y GUARDADO DE .tsc ------------------
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
            cipher = self.get_cipher_from_tsc(raw_data)
            decrypted = self.decrypt_tsc(raw_data, cipher)
            for enc in ["shift_jis", "cp932", "utf-8", "latin-1", "cp850"]:
                try:
                    text = decrypted.decode(enc, errors="strict")
                    self.load_text_to_editor(text, file_path, cipher, enc, apply_load_conversion=True)
                    self.add_history_entry(f"Opened TSC: {os.path.basename(file_path)} (cipher={cipher}, enc={enc})")
                    return
                except:
                    continue
            text = decrypted.decode("shift_jis", errors="replace")
            self.load_text_to_editor(text, file_path, cipher, "shift_jis", apply_load_conversion=True)
            self.add_history_entry(f"Opened TSC: {os.path.basename(file_path)} (fallback, cipher={cipher})")
        except Exception as e:
            messagebox.showerror(self.tr['load_error'], f"Could not load {os.path.basename(file_path)}:\n{str(e)}")

    def export_file(self):
        text_to_save = self.text_area.get("1.0", tk.END)
        if not text_to_save.strip():
            if not messagebox.askyesno(self.tr['empty_warning'], self.tr['empty_warning']):
                return

        text_to_save = self.apply_spanish_conversion(text_to_save, to_spanish=False)

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

    # ---------------------- PROYECTOS .cstsc ------------------
    def save_project(self):
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

    def load_text_to_editor(self, text, file_path, cipher, encoding, apply_load_conversion=True):
        if apply_load_conversion and self.spanish_mode.get():
            text = self.apply_spanish_conversion(text, to_spanish=True)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text)
        self.text_area.edit_reset()
        self.current_file = file_path
        self.current_cipher = cipher
        self.current_encoding = encoding
        self.delayed_highlight()
        self.update_stats()

    def refresh_current_file(self):
        if self.current_file and os.path.isfile(self.current_file):
            if self.current_file.endswith(".cstsc"):
                self.load_project()
            else:
                self.load_specific_tsc(self.current_file)

    # ---------------------- BARRA LATERAL Y BUSCADOR ------------------
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

    # ---------------------- REGLAS DE CONVERSIÓN ESPAÑOLA ------------------
    def load_rules(self):
        default_rules = [
            ("｡", "¡"),
            ("ｿ", "¿"),
            ("ｱ", "á"), ("ｲ", "é"), ("ｳ", "í"), ("ｴ", "ó"), ("ｵ", "ú"),
            ("ｶ", "Á"), ("ｷ", "É"), ("ｸ", "Í"), ("ｹ", "Ó"), ("ｺ", "Ú"),
            ("ｻ", "ü"), ("ｼ", "Ü")
        ]
        if os.path.exists(self.rules_file):
            try:
                with open(self.rules_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.rules = [(item[0], item[1]) for item in data]
                return
            except:
                pass
        self.rules = default_rules
        self.save_rules()

    def save_rules(self):
        with open(self.rules_file, "w", encoding="utf-8") as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)

    def apply_spanish_conversion(self, text: str, to_spanish: bool) -> str:
        if not self.spanish_mode.get():
            return text
        result = text
        if to_spanish:
            for orig, target in self.rules:
                result = result.replace(orig, target)
        else:
            for orig, target in self.rules:
                result = result.replace(target, orig)
        return result

    def edit_rules(self):
        win = Toplevel(self.root)
        win.title(self.tr['edit_rules'])
        win.geometry("600x400")
        win.transient(self.root)
        win.grab_set()

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("original", "mostrado")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("original", text="Carácter original (en el .tsc)")
        tree.heading("mostrado", text="Carácter mostrado (en el editor)")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        for orig, target in self.rules:
            tree.insert("", tk.END, values=(orig, target))

        btn_frame = tk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        def add_rule():
            orig = simpledialog.askstring("Nueva regla", "Carácter original (en el archivo .tsc):", parent=win)
            if not orig or len(orig) != 1:
                messagebox.showerror("Error", "Debe ser un único carácter.", parent=win)
                return
            target = simpledialog.askstring("Nueva regla", "Carácter mostrado (en el editor):", parent=win)
            if not target or len(target) != 1:
                messagebox.showerror("Error", "Debe ser un único carácter.", parent=win)
                return
            self.rules.append((orig, target))
            tree.insert("", tk.END, values=(orig, target))
            self.save_rules()
            if self.spanish_mode.get():
                self.refresh_current_file()

        def remove_rule():
            selected = tree.selection()
            if not selected:
                return
            for item in selected:
                values = tree.item(item, "values")
                orig = values[0]
                self.rules = [r for r in self.rules if r[0] != orig]
                tree.delete(item)
            self.save_rules()
            if self.spanish_mode.get():
                self.refresh_current_file()

        def modify_rule():
            selected = tree.selection()
            if not selected or len(selected) > 1:
                messagebox.showinfo("Info", "Selecciona una sola regla para modificar.", parent=win)
                return
            item = selected[0]
            values = tree.item(item, "values")
            orig, target = values
            new_orig = simpledialog.askstring("Modificar original", "Nuevo carácter original:", initialvalue=orig, parent=win)
            if new_orig and len(new_orig) == 1:
                new_target = simpledialog.askstring("Modificar mostrado", "Nuevo carácter mostrado:", initialvalue=target, parent=win)
                if new_target and len(new_target) == 1:
                    for i, (o, t) in enumerate(self.rules):
                        if o == orig:
                            self.rules[i] = (new_orig, new_target)
                            break
                    tree.item(item, values=(new_orig, new_target))
                    self.save_rules()
                    if self.spanish_mode.get():
                        self.refresh_current_file()

        tk.Button(btn_frame, text="Añadir regla", command=add_rule).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Modificar regla", command=modify_rule).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar regla", command=remove_rule).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=win.destroy).pack(side=tk.RIGHT, padx=5)

    # ---------------------- FUENTES ------------------
    def update_font(self):
        font_name = self.current_font_name.get()
        self.text_area.config(font=(font_name, self.base_font_size))
        self.text_area.tag_configure("evento", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.text_area.tag_configure("comando_letras", font=(self.current_font_name.get(), self.base_font_size, "bold"))
        self.delayed_highlight()

    # ---------------------- RESALTADO DE SINTAXIS ------------------
    def delayed_highlight(self):
        self.root.after(50, self.highlight_syntax)

    def highlight_syntax(self):
        for tag in ("evento", "comando_letras", "comando_digitos", "comando_id", "caracter_convertido"):
            self.text_area.tag_remove(tag, "1.0", tk.END)

        texto = self.text_area.get("1.0", tk.END)
        if not texto:
            return

        # Eventos #XXXX
        for match in re.finditer(r'#[0-9A-Fa-f]{4}\b', texto):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.text_area.tag_add("evento", start, end)

        # Comandos TSC
        patron_comando = r'<([A-Z]{1,3})([0-9]{4})?'
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

        # Caracteres especiales españoles (siempre rojo)
        patron_especial = r'[áéíóúüñÁÉÍÓÚÜÑ¡¿]'
        for match in re.finditer(patron_especial, texto):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.text_area.tag_add("caracter_convertido", start, end)

    # ---------------------- OTRAS FUNCIONES ------------------
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

    def open_search_dialog(self):
        # Implementación básica (puede ampliarse)
        messagebox.showinfo("Info", "Search dialog not yet fully implemented.")

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

    def show_tsc_docs(self):
        doc_text = "TSC commands:\n\n" + "\n".join([f"<{cmd} - {desc[2]}" for cmd, desc in self.commands_data.items()])
        messagebox.showinfo(self.tr['tsc_commands'], doc_text)

    def show_about(self):
        messagebox.showinfo(self.tr['about'],
            "TSC Editor+ v17.0\n"
            "Editor profesional de archivos .tsc de Cave Story\n"
            "Cifrado compatible con Booster's Lab (Carrot Lord)\n"
            "Características: resaltado de sintaxis, historial, contadores, contador de caracteres,\n"
            "documentación rápida, tema oscuro, auto-guardado, soporte multilenguaje.\n"
            "Atajos: Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Z, Ctrl+Y, Ctrl+F, Ctrl+K, F5")

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

        after_lt = line_text[start_col+1:]
        match = re.match(r'[A-Z]{1,4}[0-9]{0,4}[+-]?', after_lt)
        if not match:
            messagebox.showinfo(self.tr['cmd_info_title'], self.tr['cmd_unrecognized'])
            return
        cmd_body = match.group(0)
        cmd_key = ''.join(ch for ch in cmd_body if ch.isalpha())
        if cmd_key in self.commands_data:
            desc = self.commands_data[cmd_key][2]
            extra = ""
            if cmd_key == "FAC" and len(cmd_body) > 3:
                face_id = cmd_body[3:7]
                if face_id in self.face_names:
                    extra = f"\nFace: {self.face_names[face_id]}"
            elif cmd_key == "CMU" and len(cmd_body) > 3:
                music_id = cmd_body[3:7]
                extra = f"\nMusic ID: {music_id}"
            messagebox.showinfo(f"{self.tr['cmd_info_title']}: {cmd_key}", f"{desc}{extra}")
        else:
            messagebox.showinfo(self.tr['cmd_info_title'], f"{self.tr['cmd_unknown']} '<{cmd_body}>'")

if __name__ == "__main__":
    root = tk.Tk()
    app = TSCEditor(root)
    root.mainloop()
