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
    """
    Guarda un archivo .tsc con la codificación y cifrado especificados.
    Si encoding es None o utf-8, se fuerza shift_jis o cp1252 (nunca utf-8 a menos que se pida explícitamente y se advierta).
    """
    # Forzar codificaciones seguras si no se especificó una válida
    if encoding is None or encoding.lower() in ("utf-8", "utf8", "unicode"):
        # No permitir UTF-8 por defecto; elegir shift_jis o cp1252
        try:
            plain_text.encode('shift_jis')
            encoding = 'shift_jis'
        except UnicodeEncodeError:
            encoding = 'cp1252'
        print(f"[INFO] Codificación forzada a {encoding} (no se permite UTF-8 por defecto)")

    try:
        # Usar 'strict' para fallar ante caracteres no soportados
        plain_bytes = plain_text.encode(encoding, errors='strict')
    except UnicodeEncodeError as e:
        # Segundo intento con cp1252 si falló
        if encoding != 'cp1252':
            try:
                plain_bytes = plain_text.encode('cp1252', errors='strict')
                encoding = 'cp1252'
                print(f"[INFO] Fallback a cp1252 exitoso")
            except UnicodeEncodeError:
                raise RuntimeError(f"No se puede guardar el archivo. Caracteres no compatibles con {encoding} ni cp1252: {e}")
        else:
            raise RuntimeError(f"No se puede guardar el archivo en cp1252. Caracteres no compatibles: {e}")

    if cipher != 0 and encrypt_func:
        middle_pos = get_middle_pos(len(plain_bytes)) if get_middle_pos else len(plain_bytes)//2
        encrypted = encrypt_func(plain_bytes, cipher, middle_pos)
    else:
        encrypted = plain_bytes

    with open(file_path, "wb") as f:
        f.write(encrypted)
    return True

def load_project_file(file_path: str) -> tuple:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        text = text.replace('\r\n', '\n').replace('\r', '\n')
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