# -*- coding: utf-8 -*-
"""
Modern tab manager for TSC Editor+.
Implements a notebook with close button, right-click menu, and keyboard shortcuts.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

class TabManager:
    def __init__(self, parent, app):
        self.app = app
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.buffers = []          
        self.next_temp_id = 1
        self.tab_counter = 1

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[2, 2])
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Floating button "✕" to close the current tab
        self.close_button = ttk.Button(self.notebook, text="✕", width=3, command=self.close_current_tab)
        self.notebook.bind("<Configure>", self._place_close_button)
        self._place_close_button()

        # Contextual menu
        self.tab_menu = tk.Menu(self.notebook, tearoff=0)
        self.tab_menu.add_command(label="Close", command=self.close_current_tab)
        self.tab_menu.add_command(label="Close Others", command=self.close_other_tabs)
        self.tab_menu.add_command(label="Close All", command=self.close_all_tabs)
        self.notebook.bind("<Button-3>", self.show_tab_menu)
        self.notebook.bind("<Button-2>", self.on_middle_click)

    def _place_close_button(self, event=None):
        """Coloca el botón de cierre en la esquina superior derecha del notebook."""
        self.close_button.place(relx=1.0, x=-5, y=5, anchor="ne")

    def add_tab(self, file_path, content, encoding=None, cipher=None):
        for buf in self.buffers:
            if buf['key'] == file_path:
                self.notebook.select(buf['tab_id'])
                return

        tab_frame = tk.Frame(self.notebook)
        text_widget = self.app.create_new_text_widget(tab_frame)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", content)
        text_widget.edit_reset()
        text_widget.file_path = file_path
        text_widget.encoding = encoding
        text_widget.cipher = cipher

        tab_id = self.notebook.add(tab_frame, text=os.path.basename(file_path))
        buffer = {
            'key': file_path,
            'widget': text_widget,
            'tab_id': tab_id,
            'saved_content': content,
            'title': os.path.basename(file_path)
        }
        self.buffers.append(buffer)
        self.notebook.select(tab_id)
        self.update_active_text_area()
        return file_path

    def add_empty_tab(self, custom_name=None):
        tab_frame = tk.Frame(self.notebook)
        text_widget = self.app.create_new_text_widget(tab_frame)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.edit_reset()
        temp_key = f"__temp_{self.next_temp_id}"
        self.next_temp_id += 1
        if custom_name:
            title = custom_name
        else:
            title = f"New File {self.tab_counter}"
            self.tab_counter += 1
        text_widget.file_path = None
        text_widget.encoding = None
        text_widget.cipher = None

        tab_id = self.notebook.add(tab_frame, text=title)
        buffer = {
            'key': temp_key,
            'widget': text_widget,
            'tab_id': tab_id,
            'saved_content': "",
            'title': title
        }
        self.buffers.append(buffer)
        self.notebook.select(tab_id)
        self.update_active_text_area()
        self.app.add_history_entry(f"New empty tab: {title}")
        return temp_key

    def close_tab(self, key):
        index = None
        buffer = None
        for i, buf in enumerate(self.buffers):
            if buf['key'] == key:
                index = i
                buffer = buf
                break
        if index is None:
            return True

        text_widget = buffer['widget']
        saved_content = buffer['saved_content']
        current_text = text_widget.get("1.0", "end-1c")

        if current_text != saved_content:
            tab_name = buffer['title']
            title = self.app.tr.get('unsaved_tab_title', 'Unsaved Changes')
            msg = self.app.tr.get('unsaved_tab_message', 'There are unsaved changes in "{}".\nDo you want to save them before closing?')
            answer = messagebox.askyesnocancel(title, msg.format(tab_name))
            if answer is None:
                return False
            elif answer:
                if key.startswith('__temp'):
                    if not self.app.save_file_as(text_widget):
                        return False
                else:
                    self.app.save_specific_file(key, text_widget)
                buffer['saved_content'] = text_widget.get("1.0", "end-1c")

        self.notebook.forget(index)
        del self.buffers[index]
        self.update_active_text_area()
        return True

    def close_current_tab(self):
        if not self.buffers:
            return
        try:
            current_idx = self.notebook.index("current")
        except tk.TclError:
            current_idx = 0 if self.buffers else -1
        if 0 <= current_idx < len(self.buffers):
            self.close_tab(self.buffers[current_idx]['key'])

    def close_other_tabs(self):
        if not self.buffers:
            return
        try:
            current_idx = self.notebook.index("current")
        except tk.TclError:
            current_idx = 0 if self.buffers else -1
        if current_idx < 0:
            return
        for i in range(len(self.buffers)-1, -1, -1):
            if i != current_idx:
                self.close_tab(self.buffers[i]['key'])

    def close_all_tabs(self):
        for i in range(len(self.buffers)-1, -1, -1):
            if not self.close_tab(self.buffers[i]['key']):
                return

    def show_tab_menu(self, event):
        tab_id = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        if tab_id:
            self.notebook.select(tab_id)
            self.tab_menu.post(event.x_root, event.y_root)

    def on_middle_click(self, event):
        tab_id = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        if tab_id:
            for buf in self.buffers:
                if buf['tab_id'] == tab_id:
                    self.close_tab(buf['key'])
                    break

    def on_tab_changed(self, event):
        self.update_active_text_area()

    def update_active_text_area(self):
        if not self.buffers:
            self.app.text_area = None
            self.app.current_file = None
            self.app.saved_content = ""
            return
        try:
            current_idx = self.notebook.index("current")
        except tk.TclError:
            current_idx = 0 if self.buffers else -1
        if current_idx < 0 or current_idx >= len(self.buffers):
            current_idx = 0 if self.buffers else -1
        if current_idx >= 0:
            buffer = self.buffers[current_idx]
            self.app.text_area = buffer['widget']
            self.app.saved_content = buffer['saved_content']
            if buffer['key'].startswith('__temp'):
                self.app.current_file = None
                self.app.current_cipher = None
                self.app.current_encoding = None
            else:
                self.app.current_file = buffer['key']
                self.app.current_cipher = buffer['widget'].cipher
                self.app.current_encoding = buffer['widget'].encoding
            self.app.delayed_highlight()
            self.app.update_stats()
        else:
            self.app.text_area = None

    def get_current_text_widget(self):
        if not self.buffers:
            return None
        try:
            current_idx = self.notebook.index("current")
        except tk.TclError:
            current_idx = 0
        if 0 <= current_idx < len(self.buffers):
            return self.buffers[current_idx]['widget']
        return None

    def update_tab_file_path(self, old_key, new_path, content, encoding, cipher):
        for i, buf in enumerate(self.buffers):
            if buf['key'] == old_key:
                try:
                    self.notebook.tab(buf['tab_id'])   
                except tk.TclError:
                    self.add_tab(new_path, content, encoding, cipher)
                    return
                buf['key'] = new_path
                buf['widget'].file_path = new_path
                buf['widget'].encoding = encoding
                buf['widget'].cipher = cipher
                buf['saved_content'] = content
                buf['title'] = os.path.basename(new_path)
                try:
                    self.notebook.tab(buf['tab_id'], text=buf['title'])
                except tk.TclError:
                    pass
                self.update_active_text_area()
                return
        self.add_tab(new_path, content, encoding, cipher)
