# -*- coding: utf-8 -*-
"""
Encryption/decryption utilities for Cave Story .tsc files (Carrot Lord cipher).
Now uses the middle byte of the file as the cipher key (more reliable).
"""

def get_cipher_from_tsc(data: bytes) -> int:
    """
    Detect the cipher key used in a .tsc file.
    Returns the byte at the middle of the file.
    """
    if not data:
        return 0
    return data[len(data) // 2]

def decrypt_tsc(data: bytes, cipher: int) -> bytes:
    if cipher == 0:
        return data
    result = bytearray()
    for b in data:
        if b == cipher:
            result.append(cipher)
        else:
            val = (b - cipher) % 256
            result.append(val)
    return bytes(result)

def encrypt_tsc(plain: bytes, cipher: int, middle_pos: int) -> bytes:
    if cipher == 0:
        return plain
    result = bytearray()
    for i, b in enumerate(plain):
        if i == middle_pos:
            result.append(cipher)
        else:
            val = (b + cipher) % 256
            result.append(val)
    return bytes(result)