# -*- coding: utf-8 -*-
"""
Load and save application settings (settings.json).
"""

import os
import json

def load_settings(settings_file: str, default_settings: dict) -> dict:
    settings = default_settings.copy()
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                settings.update(data)
        except:
            pass
    return settings

def save_settings(settings_file: str, settings: dict):
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)