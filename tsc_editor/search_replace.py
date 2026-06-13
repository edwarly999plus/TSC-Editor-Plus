# -*- coding: utf-8 -*-
"""
Search and replace functionality with real-time highlighting and active match feedback.
"""

import re
import tkinter as tk

class SearchReplaceManager:
    def __init__(self, app):
        self.app = app
        self.search_text = ""
        self.search_case = False
        self.search_whole = False
        self.all_matches = []      
        self.current_match_index = -1

    def _get_text_widget(self):
        """Devuelve el widget de texto activo (pestaña actual)."""
        return self.app.text_area

    def refresh_highlight(self):
        """Resalta todas las coincidencias y reinicia el índice de coincidencia activa."""
        text_widget = self._get_text_widget()
        if not text_widget:
            return
        text_widget.tag_remove("search_highlight", "1.0", tk.END)
        text_widget.tag_remove("active_match", "1.0", tk.END)
        self.all_matches = []
        self.current_match_index = -1

        if not self.search_text:
            self.app.search_status.config(text="")
            return

        flags = 0 if self.search_case else re.IGNORECASE
        pattern = self.search_text
        if self.search_whole:
            pattern = r'\b' + re.escape(pattern) + r'\b'
        else:
            pattern = re.escape(pattern)

        try:
            regex = re.compile(pattern, flags)
            full_text = text_widget.get("1.0", tk.END)
            # Remove last character (extra line break) so positions match get()
            full_text = full_text.rstrip('\n')
            self.all_matches = [(m.start(), m.end()) for m in regex.finditer(full_text)]
            for start, end in self.all_matches:
                start_idx = f"1.0 + {start} chars"
                end_idx = f"1.0 + {end} chars"
                text_widget.tag_add("search_highlight", start_idx, end_idx)
            # Update counter
            total = len(self.all_matches)
            if total > 0:
                self.app.search_status.config(text=f"Found {total} matches")
            else:
                self.app.search_status.config(text="No matches")
            # Set the active highlight label style
            text_widget.tag_config("search_highlight", background="yellow")
            text_widget.tag_config("active_match", background="#03ff2d")  # Green
        except re.error:
            self.app.search_status.config(text="Invalid regular expression")

    def _goto_match(self, index):
        """Mueve el cursor a la coincidencia index y la resalta como activa."""
        text_widget = self._get_text_widget()
        if not text_widget:
            return False
        if index < 0 or index >= len(self.all_matches):
            return False
        text_widget.tag_remove("active_match", "1.0", tk.END)
        start, end = self.all_matches[index]
        start_idx = f"1.0 + {start} chars"
        end_idx = f"1.0 + {end} chars"
        text_widget.tag_add("active_match", start_idx, end_idx)
        text_widget.mark_set(tk.INSERT, end_idx)
        text_widget.see(start_idx)
        text_widget.tag_raise("active_match", "search_highlight")
        total = len(self.all_matches)
        self.app.search_status.config(text=f"Match {index+1} of {total}")
        return True

    def find_next(self):
        if not self.search_text:
            return
        if not self.all_matches:
            self.refresh_highlight()
            if not self.all_matches:
                return
        new_index = (self.current_match_index + 1) % len(self.all_matches)
        if self._goto_match(new_index):
            self.current_match_index = new_index
        else:
            self.app.search_status.config(text="No matches found")

    def find_prev(self):
        if not self.search_text:
            return
        if not self.all_matches:
            self.refresh_highlight()
            if not self.all_matches:
                return
        new_index = (self.current_match_index - 1) % len(self.all_matches)
        if self._goto_match(new_index):
            self.current_match_index = new_index
        else:
            self.app.search_status.config(text="No matches found")

    def replace_current(self, replace_text):
        if not self.search_text:
            return
        if self.current_match_index < 0 or self.current_match_index >= len(self.all_matches):
            self.find_next()
            if self.current_match_index < 0:
                return
        text_widget = self._get_text_widget()
        if not text_widget:
            return
        start, end = self.all_matches[self.current_match_index]
        start_idx = f"1.0 + {start} chars"
        end_idx = f"1.0 + {end} chars"
        # Perform replacement
        text_widget.delete(start_idx, end_idx)
        text_widget.insert(start_idx, replace_text)
        self.app.add_history_entry("Replace")
        # Recalculate all matches because text changed
        self.refresh_highlight()
        # Move to next match (if exists)
        if self.all_matches:
            self.current_match_index = min(self.current_match_index, len(self.all_matches)-1)
            self._goto_match(self.current_match_index)
        else:
            self.current_match_index = -1

    def replace_all(self, replace_text):
        if not self.search_text:
            return
        self.refresh_highlight()
        if not self.all_matches:
            return
        text_widget = self._get_text_widget()
        if not text_widget:
            return
        replaced_count = 0
        for start, end in reversed(self.all_matches):
            start_idx = f"1.0 + {start} chars"
            end_idx = f"1.0 + {end} chars"
            text_widget.delete(start_idx, end_idx)
            text_widget.insert(start_idx, replace_text)
            replaced_count += 1
        self.app.add_history_entry(f"Replace All ({replaced_count})")
        self.refresh_highlight()
        self.app.search_status.config(text=f"Replaced {replaced_count} occurrences")
