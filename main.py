#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


# ======================================================================
# AUTO-INSTALL DEPENDENCIES
# ======================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")

if LIBS_DIR not in sys.path:
    sys.path.insert(0, LIBS_DIR)

# Dependencias base (siempre necesarias)
DEPENDENCIES = {
    "ttkbootstrap": "ttkbootstrap==1.10.1",
    "PIL": "pillow==10.0.0",
    "pywinstyles": "pywinstyles==1.8",
}

def install_package(package_spec, target_dir):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_spec, "--target", target_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False

def check_and_install():
    missing = []
    for module_name, pkg_spec in DEPENDENCIES.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append((module_name, pkg_spec))

    if not missing:
        return

    print("=" * 60)
    print("TSC Editor+ - Missing dependencies detected.")
    print("The following packages will be installed automatically:")
    for _, pkg_spec in missing:
        print(f"  - {pkg_spec}")
    print("=" * 60)

    os.makedirs(LIBS_DIR, exist_ok=True)

    total = len(missing)
    for i, (module_name, pkg_spec) in enumerate(missing, start=1):
        print(f"[{i}/{total}] Installing {pkg_spec}... ", end="", flush=True)
        if install_package(pkg_spec, LIBS_DIR):
            print("OK")
        else:
            print("FAILED")
            print(f"  Warning: Could not install {pkg_spec}. Some features may be missing.")
    print("=" * 60)
    print("Installation process completed. Launching editor...\n")

# Ejecutar verificación de dependencias
check_and_install()

# =====================================================================
# EXECUTE MAIN APP
# =====================================================================

import tkinter as tk

try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False
    tb = None

from tsc_editor import TSCEditor

if __name__ == "__main__":
    if TTKBOOTSTRAP_AVAILABLE:
        root = tb.Window(themename="darkly")
    else:
        root = tk.Tk()
    app = TSCEditor(root)
    root.mainloop()