# -*- coding: utf-8 -*-
"""
UI components: menubar, toolbar, context menu, theme application.
"""

import tkinter as tk
from tkinter import ttk

def create_menubar(app):
    menubar = tk.Menu(app.root, tearoff=0)
    app.root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=app.tr['file_menu'], menu=file_menu)
    file_menu.add_command(label=app.tr['open_tsc'], command=app.load_file, accelerator="Ctrl+O")
    file_menu.add_command(label=app.tr['open_project'], command=app.load_project, accelerator="Ctrl+Shift+O")
    file_menu.add_command(label=app.tr['open_folder'], command=app.load_folder, accelerator="Ctrl+Shift+Alt+O")
    file_menu.add_command(label=app.tr['delete_from_list'], command=app.delete_current_from_list, accelerator="Ctrl+Del")
    file_menu.add_command(label=app.tr['delete_all_from_list'], command=app.delete_all_from_list, accelerator="Ctrl+Shift+Del")
    file_menu.add_separator()
    file_menu.add_command(label=app.tr['export_tsc'], command=app.export_file, accelerator="Ctrl+Shift+S")
    file_menu.add_command(label=app.tr['save_project'], command=app.save_project, accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label=app.tr['settings'], command=app.open_settings, accelerator="Ctrl+K")
    file_menu.add_separator()
    file_menu.add_command(label=app.tr['exit'], command=app.root.quit, accelerator="Alt+F4")

    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=app.tr['edit_menu'], menu=edit_menu)
    edit_menu.add_command(label=app.tr['undo'], command=app.undo_action, accelerator="Ctrl+Z")
    edit_menu.add_command(label=app.tr['redo'], command=app.redo_action, accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label=app.tr['check_syntax'], command=app.check_syntax_cmd)
    edit_menu.add_separator()
    edit_menu.add_command(label=app.tr['smart_replace'], command=app.smart_replace_special_chars, accelerator="Ctrl+R")

    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=app.tr['view_menu'], menu=view_menu)
    view_menu.add_command(label=app.tr['font_size'], command=app.open_view_options)
    view_menu.add_command(label=app.tr['hex_dump'], command=app.show_hex_dump)
    view_menu.add_command(label=app.tr['see_quick_docs'], command=app.show_quick_docs)
    view_menu.add_command(label=app.tr['search_tab'], command=app.focus_search_tab, accelerator="Ctrl+F")
    view_menu.add_command(label=app.tr['show_history'], command=app.focus_history_tab, accelerator="Ctrl+H")
    view_menu.add_command(label=app.tr['edit_custom_cmds'], command=app.edit_custom_commands)
    view_menu.add_command(label=app.tr['custom_cmd_syntax'], command=app.open_custom_command_syntax_window, accelerator="Ctrl+Shift+C")
    view_menu.add_command(label=app.tr['customize_command_colors'], command=app.customize_command_colors)
    view_menu.add_separator()
    view_menu.add_command(label="Toggle Theme (Darkly/Vapor)", command=app.toggle_theme)

    font_submenu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label=app.tr['font_submenu'], menu=font_submenu)
    for f in app.available_fonts:
        font_submenu.add_radiobutton(label=f, variable=app.current_font_name, value=f, command=app.update_font)

    run_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=app.tr['run_menu'], menu=run_menu)
    run_menu.add_command(label=app.tr['find_doukutsu'], command=app.lookup_doukutsu)
    run_menu.add_command(label=app.tr['test_game'], command=app.test_game, accelerator="F5")

    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=app.tr['help_menu'], menu=help_menu)
    help_menu.add_command(label=app.tr['about'], command=app.show_about)

    return menubar

def create_toolbar(app):
    toolbar = tk.Frame(app.root)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    theme_btn = tk.Button(
        toolbar,
        text="🌙 Darkly" if app.current_theme.get() == "darkly" else "☀️ Vapor",
        command=app.toggle_theme
    )
    theme_btn.pack(side=tk.LEFT, padx=2, pady=2)
    return toolbar, theme_btn

def create_context_menu(app, text_widget):
    menu = tk.Menu(text_widget, tearoff=0)
    menu.add_command(label=app.tr['copy'], command=app.copy_text)
    menu.add_command(label=app.tr['paste'], command=app.paste_text)
    menu.add_command(label=app.tr['cut'], command=app.cut_text)
    menu.add_separator()
    menu.add_command(label=app.tr['count_chars'], command=app.count_characters_normal)
    menu.add_command(label=app.tr['count_chars_face'], command=app.count_characters_face)
    menu.add_separator()
    menu.add_command(label=app.tr['tsc_commands'], command=app.show_command_info)
    menu.add_separator()
    menu.add_command(label=app.tr['smart_replace'], command=app.smart_replace_special_chars)
    text_widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    return menu

def apply_theme_to_widgets(app, dark_theme):
    if dark_theme:
        bg, fg, select_bg = "#1e1e1e", "#ffffff", "#3c3c3c"
        text_bg, entry_bg = "#2b2b2b", "#2b2b2b"
        button_bg, button_fg = "#3c3c3c", "#ffffff"
        scrollbar_bg, scrollbar_trough = "#2b2b2b", "#1e1e1e"
        cmd_color, digit_color, id_color, error_color, special_color = "#88AAFF", "#FF88BB", "#FF88BB", "#FF6666", "#FF6666"
        search_bg = "#444400"
        cmd_pink, cmd_red = "#FF88BB", "#FF6666"
    else:
        bg, fg, select_bg = "#f0f0f0", "#000000", "#0078D7"
        text_bg, entry_bg = "#ffffff", "#ffffff"
        button_bg, button_fg = "#e0e0e0", "#000000"
        scrollbar_bg, scrollbar_trough = "#f0f0f0", "#e0e0e0"
        cmd_color, digit_color, id_color, error_color, special_color = "#0000FF", "#C7158C", "#C7158C", "#FF0000", "#FF0000"
        search_bg = "yellow"
        cmd_pink, cmd_red = "#C7158C", "#FF0000"

    app.root.configure(bg=bg)
    app.main_paned.configure(bg=bg, sashrelief=tk.RAISED)
    app.sidebar_frame.configure(bg=bg)

    app.file_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.history_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.docs_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.docs_detail.configure(bg=text_bg, fg=fg)
    app.text_area.configure(bg=text_bg, fg=fg, insertbackground=fg)

    app.status_label.configure(bg=bg, fg=fg)
    app.stats_label.configure(bg=bg, fg=fg)
    app.history_label.configure(bg=bg, fg=fg)
    app.search_label.configure(bg=bg, fg=fg)

    app.clear_btn.configure(bg=button_bg, fg=button_fg, activebackground=select_bg)
    if hasattr(app, 'theme_btn'):
        app.theme_btn.configure(bg=button_bg, fg=button_fg, activebackground=select_bg)

    for sb in (app.scrollbar_files, app.history_scrollbar, app.scrollbar_docs):
        sb.configure(bg=scrollbar_bg, troughcolor=scrollbar_trough, activebackground=select_bg)
    if hasattr(app.text_area, 'vbar'):
        app.text_area.vbar.configure(bg=scrollbar_bg, troughcolor=scrollbar_trough, activebackground=select_bg)

    app.text_area.tag_configure("comando_letras", foreground=cmd_color)
    app.text_area.tag_configure("comando_digitos", foreground=digit_color)
    app.text_area.tag_configure("comando_id", foreground=id_color)
    app.text_area.tag_configure("error", foreground=error_color)
    app.text_area.tag_configure("special_warning", foreground=special_color)
    app.text_area.tag_configure("search_highlight", background=search_bg)
    app.text_area.tag_configure("comando_personal_rosa", foreground=cmd_pink)
    app.text_area.tag_configure("comando_personal_rojo", foreground=cmd_red)