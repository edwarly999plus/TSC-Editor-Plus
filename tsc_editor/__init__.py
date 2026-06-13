# -*- coding: utf-8 -*-
"""
TSC Editor+ - Professional editor for Cave Story .tsc files
"""

from .editor_app import TSCEditor
from .encryption import get_cipher_from_tsc, decrypt_tsc, encrypt_tsc
from .command_system import load_base_commands, load_custom_commands
from .settings_manager import load_settings, save_settings
from .syntax_highlight import check_syntax, highlight_syntax
from .dialogs import ask_encoding_and_cipher, smart_replace_dialog

__version__ = "2.0.0"
__all__ = [
    "TSCEditor",
    "get_cipher_from_tsc",
    "decrypt_tsc",
    "encrypt_tsc",
    "load_base_commands",
    "load_custom_commands",
    "load_settings",
    "save_settings",
    "check_syntax",
    "highlight_syntax",
    "ask_encoding_and_cipher",
    "smart_replace_dialog",
]