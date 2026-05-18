# -*- coding: utf-8 -*-
"""
File I/O for .tsc and .cstsc files.
"""

import os

def load_tsc_file(file_path: str) -> tuple:
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return data, True
    except Exception:
        return None, False

def save_tsc_file(file_path: str, plain_text: str, cipher: int, encoding: str = "shift_jis",
                  encrypt_func=None, get_middle_pos=None) -> bool:
    try:
        plain_bytes = plain_text.encode(encoding, errors="replace")
        if cipher != 0 and encrypt_func:
            middle_pos = get_middle_pos(len(plain_bytes)) if get_middle_pos else len(plain_bytes)//2
            encrypted = encrypt_func(plain_bytes, cipher, middle_pos)
        else:
            encrypted = plain_bytes
        with open(file_path, "wb") as f:
            f.write(encrypted)
        return True
    except Exception:
        return False

def load_project_file(file_path: str) -> tuple:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text, True
    except Exception:
        return None, False

def save_project_file(file_path: str, text: str) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception:
        return False