# -*- coding: utf-8 -*-
"""
Helper to highlight the currently opened TSC file in the sidebar list.
"""

def highlight_current_file_in_list(app):
    """Resalta el archivo actual en la lista lateral con color azul."""
    if not app.current_file:
        return
    # Recorrer los ítems de la lista y buscar la ruta completa
    for i in range(app.file_listbox.size()):
        rel_path = app.file_listbox.get(i)
        full_path = getattr(app.file_listbox, '_paths', {}).get(rel_path)
        if full_path == app.current_file:
            # Color azul según tema
            if app.settings.get("dark_theme", False):
                app.file_listbox.itemconfig(i, bg="#0055AA", fg="white")
            else:
                app.file_listbox.itemconfig(i, bg="#0078D7", fg="white")
        else:
            # Restablecer color por defecto
            if app.settings.get("dark_theme", False):
                app.file_listbox.itemconfig(i, bg="#2b2b2b", fg="white")
            else:
                app.file_listbox.itemconfig(i, bg="white", fg="black")