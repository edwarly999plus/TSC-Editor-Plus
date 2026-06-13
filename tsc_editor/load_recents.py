# -*- coding: utf-8 -*-
"""
Handles saving and restoring the recent TSC folder (sidebar list).
"""

import os

def save_recent_folder(settings, folder_path):
    """Save the recent folder path in settings."""
    settings["last_folder"] = folder_path

def get_recent_folder(settings):
    """Return the recent folder path if it exists and is a directory."""
    folder = settings.get("last_folder", "")
    if folder and os.path.isdir(folder):
        return folder
    return None

def should_restore_recent(settings):
    """Check if the 'keep recent TSC' option is enabled."""
    return settings.get("keep_recent_tsc", False)