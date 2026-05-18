# -*- coding: utf-8 -*-
"""
Encryption/decryption utilities for Cave Story .tsc files (Carrot Lord cipher).
Now uses modulo 256 (wrap-around) and non-negative cipher.
"""

def get_cipher_from_tsc(data: bytes) -> int:
    newline_dict = {}
    for i in range(len(data) - 1):
        b1 = data[i]
        b2 = data[i+1]
        if (b1 - b2) == 3:
            newline_dict[b1] = newline_dict.get(b1, 0) + 1
    if not newline_dict:
        return 0
    top_key = max(newline_dict, key=newline_dict.get)
    # Asegurar que el cipher sea no negativo (0-255)
    return (top_key - 0x0D) % 0x100

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