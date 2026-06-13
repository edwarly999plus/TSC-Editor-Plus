# -*- coding: utf-8 -*-
"""
Hints manager for TSC Editor+ Quick Docs panel.
Displays rotating tips every 5 seconds.
"""

import tkinter as tk

class HintsManager:
    def __init__(self, parent, editor):
        """
        parent: widget donde se colocará el frame de hints (normalmente docs_tab)
        editor: instancia de TSCEditor (para acceder a root, settings, tr)
        """
        self.editor = editor
        self.parent = parent
        self.hint_frame = None
        self.hint_label = None
        self.hint_index = 0
        self.after_id = None
        self._create_widgets()
        self.start_rotation()

    def _create_widgets(self):
        dark = self.editor.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        self.hint_frame = tk.Frame(self.parent, bg=bg)
        self.hint_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.hint_label = tk.Label(
            self.hint_frame, text="", font=("Segoe UI", 9, "italic"),
            wraplength=280, justify=tk.LEFT, bg=bg, fg=fg
        )
        self.hint_label.pack(fill=tk.BOTH, expand=True)

    def start_rotation(self):
        self._rotate_hint()

    def _rotate_hint(self):
        if self.after_id:
            self.editor.root.after_cancel(self.after_id)
        hints = self.editor.tr.get('hints', [])
        if hints:
            hint = hints[self.hint_index % len(hints)]
            self.hint_label.config(text=hint)
            self.hint_index += 1
            self.after_id = self.editor.root.after(5000, self._rotate_hint)

    def update_language(self):
        """Actualiza las pistas al cambiar de idioma."""
        if self.after_id:
            self.editor.root.after_cancel(self.after_id)
        self.hint_index = 0
        self.start_rotation()

    def update_theme(self):
        dark = self.editor.settings.get("dark_theme", False)
        bg = "#1e1e1e" if dark else "#ffffff"
        fg = "white" if dark else "black"
        if self.hint_frame:
            self.hint_frame.config(bg=bg)
        if self.hint_label:
            self.hint_label.config(bg=bg, fg=fg)

    def destroy(self):
        """Limpia recursos al cerrar el editor."""
        if self.after_id:
            self.editor.root.after_cancel(self.after_id)
        if self.hint_frame:
            self.hint_frame.destroy()