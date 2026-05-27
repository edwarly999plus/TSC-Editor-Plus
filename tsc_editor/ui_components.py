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
    view_menu.add_command(label="Toggle Theme (Darkly/Cosmo)", command=app.toggle_theme)

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
        text="🌙 Darkly" if app.current_theme.get() == "darkly" else "☀️ Cosmo",
        command=app.toggle_theme
    )
    theme_btn.pack(side=tk.RIGHT, padx=5, pady=9)
    return toolbar, theme_btn

def create_context_menu(app):
    menu = tk.Menu(app.root, tearoff=0)
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
    return menu

def apply_syntax_tags_to_widget(widget, theme_name):
    """Aplica los colores de sintaxis a un widget de texto según el tema."""
    if theme_name == "darkly":
        cmd_color, digit_color, id_color = "#88AAFF", "#FF88BB", "#FF88BB"
        error_color, special_color = "#FF6666", "#FF6666"
        search_bg = "#444400"
        cmd_pink, cmd_red = "#FF88BB", "#FF6666"
    elif theme_name == "vapor":
        cmd_color, digit_color, id_color = "#b77aff", "#ff77aa", "#ff77aa"
        error_color, special_color = "#ff6666", "#ffcc66"
        search_bg = "#553300"
        cmd_pink, cmd_red = "#ff77aa", "#ff6666"
    else:  # cosmo
        cmd_color, digit_color, id_color = "#0000FF", "#C7158C", "#C7158C"
        error_color, special_color = "#FF0000", "#FF0000"
        search_bg = "yellow"
        cmd_pink, cmd_red = "#C7158C", "#FF0000"

    widget.tag_configure("comando_letras", foreground=cmd_color)
    widget.tag_configure("comando_digitos", foreground=digit_color)
    widget.tag_configure("comando_id", foreground=id_color)
    widget.tag_configure("error", foreground=error_color)
    widget.tag_configure("special_warning", foreground=special_color)
    widget.tag_configure("search_highlight", background=search_bg)
    widget.tag_configure("comando_personal_rosa", foreground=cmd_pink)
    widget.tag_configure("comando_personal_rojo", foreground=cmd_red)
    widget.tag_configure("current_match", background="#00FF00", foreground="black")

def apply_theme_to_widgets(app, dark_theme=None):
    current_theme = app.current_theme.get()

    if current_theme == "darkly":
        bg, fg, select_bg = "#1e1e1e", "#ffffff", "#3c3c3c"
        text_bg, entry_bg = "#2b2b2b", "#2b2b2b"
        button_bg, button_fg = "#3c3c3c", "#ffffff"
        scrollbar_bg, scrollbar_trough = "#2b2b2b", "#1e1e1e"
        menu_bg, menu_fg = "#2b2b2b", "#ffffff"
    elif current_theme == "vapor":
        bg, fg, select_bg = "#1a1a2e", "#e0e0ff", "#4a2a6a"
        text_bg, entry_bg = "#2d1b4e", "#2d1b4e"
        button_bg, button_fg = "#4a2a6a", "#e0e0ff"
        scrollbar_bg, scrollbar_trough = "#2d1b4e", "#1a1a2e"
        menu_bg, menu_fg = "#2d1b4e", "#e0e0ff"
    else:  # cosmo
        bg, fg, select_bg = "#ffffff", "#000000", "#0078D7"
        text_bg, entry_bg = "#ffffff", "#ffffff"
        button_bg, button_fg = "#e0e0e0", "#000000"
        scrollbar_bg, scrollbar_trough = "#f0f0f0", "#e0e0e0"
        menu_bg, menu_fg = "#f0f0f0", "#000000"

    app.root.configure(bg=bg)
    app.main_paned.configure(bg=bg, sashrelief=tk.RAISED)
    app.sidebar_frame.configure(bg=bg)

    app.file_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.history_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.docs_listbox.configure(bg=text_bg, fg=fg, selectbackground=select_bg)
    app.docs_detail.configure(bg=text_bg, fg=fg)
    if app.text_area:
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

    if app.text_area:
        apply_syntax_tags_to_widget(app.text_area, current_theme)
    if hasattr(app, 'tab_manager') and app.tab_manager:
        for buf in app.tab_manager.buffers:
            apply_syntax_tags_to_widget(buf['widget'], current_theme)

    if hasattr(app, 'menubar') and app.menubar:
        app.menubar.configure(bg=menu_bg, fg=menu_fg, activebackground=select_bg, activeforeground=menu_fg)
        for menu in app.menubar.winfo_children():
            if isinstance(menu, tk.Menu):
                menu.configure(bg=menu_bg, fg=menu_fg, activebackground=select_bg, activeforeground=menu_fg)
                for submenu in menu.winfo_children():
                    if isinstance(submenu, tk.Menu):
                        submenu.configure(bg=menu_bg, fg=menu_fg, activebackground=select_bg, activeforeground=menu_fg)

    if hasattr(app, 'context_menu') and app.context_menu:
        app.context_menu.configure(bg=menu_bg, fg=menu_fg, activebackground=select_bg, activeforeground=menu_fg)

    select_color = "#00FF00"
    app.root.option_add('*Text.selectBackground', select_color, 'widgetDefault')
    if app.text_area:
        app.text_area.configure(selectbackground=select_color)
        app.text_area.tag_config("sel", background=select_color)
    if hasattr(app, 'tab_manager') and app.tab_manager:
        for buf in app.tab_manager.buffers:
            buf['widget'].configure(selectbackground=select_color)
            buf['widget'].tag_config("sel", background=select_color)
