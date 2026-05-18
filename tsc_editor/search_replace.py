# -*- coding: utf-8 -*-
"""
Search and replace functionality with real-time highlighting.
"""

import re
import tkinter as tk

class SearchReplaceManager:
    def __init__(self, app):
        self.app = app
        self.search_text = ""
        self.search_case = False
        self.search_whole = False

    def refresh_highlight(self):
        self.app.text_area.tag_remove("search_highlight", "1.0", tk.END)
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
            text = self.app.text_area.get("1.0", tk.END)
            count = 0
            for match in regex.finditer(text):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.app.text_area.tag_add("search_highlight", start, end)
                count += 1
            self.app.search_status.config(text=f"Found {count} matches" if count > 0 else "No matches")
        except re.error:
            self.app.search_status.config(text="Invalid regular expression")

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
            text = self.app.text_area.get("1.0", tk.END)
            cursor = self.app.text_area.index(tk.INSERT)
            cursor_char = len(self.app.text_area.get("1.0", cursor).replace('\n', ''))
            for match in regex.finditer(text):
                if match.start() >= cursor_char:
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    self.app.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                    self.app.text_area.tag_add(tk.SEL, start, end)
                    self.app.text_area.mark_set(tk.INSERT, end)
                    self.app.text_area.see(start)
                    return
            matches = list(regex.finditer(text))
            if matches:
                match = matches[0]
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.app.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.app.text_area.tag_add(tk.SEL, start, end)
                self.app.text_area.mark_set(tk.INSERT, end)
                self.app.text_area.see(start)
                self.app.search_status.config(text="Wrapped around")
            else:
                self.app.search_status.config(text="No matches")
        except re.error:
            self.app.search_status.config(text="Invalid regex")

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
            text = self.app.text_area.get("1.0", tk.END)
            cursor = self.app.text_area.index(tk.INSERT)
            cursor_char = len(self.app.text_area.get("1.0", cursor).replace('\n', ''))
            prev_match = None
            for match in regex.finditer(text):
                if match.start() < cursor_char:
                    prev_match = match
                else:
                    break
            if prev_match:
                start = f"1.0 + {prev_match.start()} chars"
                end = f"1.0 + {prev_match.end()} chars"
                self.app.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.app.text_area.tag_add(tk.SEL, start, end)
                self.app.text_area.mark_set(tk.INSERT, end)
                self.app.text_area.see(start)
            else:
                matches = list(regex.finditer(text))
                if matches:
                    match = matches[-1]
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    self.app.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                    self.app.text_area.tag_add(tk.SEL, start, end)
                    self.app.text_area.mark_set(tk.INSERT, end)
                    self.app.text_area.see(start)
                    self.app.search_status.config(text="Wrapped around")
                else:
                    self.app.search_status.config(text="No matches")
        except re.error:
            self.app.search_status.config(text="Invalid regex")

    def replace_current(self, replace_text):
        if not self.search_text:
            return
        try:
            selected = self.app.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
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
                self.app.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.app.text_area.insert(tk.INSERT, replace_text)
                self.app.add_history_entry("Replace")
                self.refresh_highlight()
        except re.error:
            pass
        self.find_next()

    def replace_all(self, replace_text):
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
            text = self.app.text_area.get("1.0", tk.END)
            new_text = re.sub(regex, replace_text, text)
            if new_text != text:
                self.app.text_area.delete("1.0", tk.END)
                self.app.text_area.insert("1.0", new_text)
                self.app.add_history_entry("Replace All")
                self.refresh_highlight()
                self.app.search_status.config(text="Replace all completed")
            else:
                self.app.search_status.config(text="No matches found")
        except re.error:
            self.app.search_status.config(text="Invalid regex")