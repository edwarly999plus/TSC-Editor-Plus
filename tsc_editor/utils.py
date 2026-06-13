# -*- coding: utf-8 -*-
"""
Utility functions: language detection, status updates, history, face/music names.
"""

import locale
from datetime import datetime
import tkinter as tk

def detect_language() -> str:
    try:
        lang_code = locale.getlocale()[0]
        if lang_code:
            if lang_code.startswith('es'):
                return 'es'
            elif lang_code.startswith('ja'):
                return 'jp'
    except:
        pass
    return 'en'

def update_stats(app):
    text = app.text_area.get("1.0", tk.END)
    lines = len(text.splitlines())
    chars = len(text) - 1
    app.stats_label.config(text=f"{app.tr['lines']}: {lines}  |  {app.tr['chars']}: {chars}")

def add_history_entry(app, action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {action}"
    app.history.append(entry)
    app.history_listbox.insert(tk.END, entry)
    app.history_listbox.see(tk.END)
    if len(app.history) > 1000:
        app.history.pop(0)
        app.history_listbox.delete(0)

def get_face_name(face_id: str, face_names: dict) -> str:
    return face_names.get(face_id, "Unknown")

def get_music_name(music_id: str) -> str:
    return f"Music {music_id}"