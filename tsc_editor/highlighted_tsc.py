# -*- coding: utf-8 -*-
"""
Helper to highlight the currently opened TSC file in the sidebar list.
"""

def highlight_current_file_in_list(app):
    """Resalta el archivo actual en la lista lateral con color azul."""
    if not app.current_file:
        return
    theme = app.current_theme.get()
    if theme == "darkly":
        default_bg = "#2b2b2b"
        default_fg = "white"
        select_bg = "#3c3c3c"
        highlight_bg = "#0055AA"
        highlight_fg = "white"
    elif theme == "vapor":
        default_bg = "#2d1b4e"
        default_fg = "#e0e0ff"
        select_bg = "#4a2a6a"
        highlight_bg = "#4a2a6a"   
        highlight_fg = "#e0e0ff"
    else:  # cosmo
        default_bg = "white"
        default_fg = "black"
        select_bg = "#0078D7"
        highlight_bg = "#0078D7"
        highlight_fg = "white"

    app.file_listbox.configure(selectbackground=select_bg)

    for i in range(app.file_listbox.size()):
        rel_path = app.file_listbox.get(i)
        full_path = getattr(app.file_listbox, '_paths', {}).get(rel_path)
        if full_path == app.current_file:
            app.file_listbox.itemconfig(i, bg=highlight_bg, fg=highlight_fg)
            app.file_listbox.selection_clear(0, "end")
            app.file_listbox.selection_set(i)
            app.file_listbox.see(i)
            app.file_listbox.activate(i)
        else:
            app.file_listbox.itemconfig(i, bg=default_bg, fg=default_fg)

    app.file_listbox.update()
