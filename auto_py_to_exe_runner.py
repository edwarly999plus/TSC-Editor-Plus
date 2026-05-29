#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejecuta auto-py-to-exe buscando en múltiples instalaciones de Python.
Evita la doble ejecución y permite instalar el módulo si no se encuentra.
"""

import subprocess
import sys
import os
import shutil
import platform

def find_python_interpreters():
    """Devuelve una lista de rutas a ejecutables de python encontrados en el sistema."""
    interpreters = []
    sistema = platform.system()
    
    if sistema == "Windows":
        cmd = ["where", "python"]
    else:  # Linux, macOS, etc.
        # Usar 'which -a' si está disponible, sino 'type -a'
        try:
            subprocess.run(["which", "-a", "python"], capture_output=True, check=False)
            cmd = ["which", "-a", "python"]
        except FileNotFoundError:
            cmd = ["type", "-a", "python"]
    
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, shell=(sistema == "Windows"))
        if resultado.returncode == 0:
            for linea in resultado.stdout.splitlines():
                linea = linea.strip()
                if linea and os.path.isfile(linea):
                    interpreters.append(linea)
    except Exception:
        pass
    
    # También agregar el python actual si no está ya en la lista
    actual = sys.executable
    if actual and actual not in interpreters:
        interpreters.append(actual)
    
    # Eliminar duplicados (por si acaso)
    interpreters = list(dict.fromkeys(interpreters))
    return interpreters

def check_auto_py_to_exe(python_path):
    """Verifica si auto-py-to-exe está disponible en el intérprete dado."""
    try:
        result = subprocess.run(
            [python_path, "-c", "import auto_py_to_exe"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def run_auto_py_to_exe(python_path):
    """Ejecuta auto-py-to-exe usando el intérprete especificado."""
    print(f"Ejecutando auto-py-to-exe con: {python_path}")
    subprocess.run([python_path, "-m", "auto_py_to_exe"])

def install_auto_py_to_exe(python_path):
    """Instala auto-py-to-exe usando pip para el intérprete dado."""
    print(f"Instalando auto-py-to-exe en {python_path} ...")
    result = subprocess.run([python_path, "-m", "pip", "install", "auto-py-to-exe"])
    if result.returncode == 0:
        print("Instalación exitosa.")
        return True
    else:
        print("Error en la instalación.")
        return False

def main():
    print("=" * 55)
    print("    Buscando e iniciando auto-py-to-exe (sin duplicados)")
    print("=" * 55)
    print()
    
    # 1. Intentar comando directo (si está en PATH)
    direct_cmd = shutil.which("auto-py-to-exe")
    if direct_cmd:
        print("[OK] auto-py-to-exe encontrado en PATH.")
        print("Ejecutando...")
        subprocess.run([direct_cmd])
        return
    
    # 2. Buscar intérpretes Python
    pythons = find_python_interpreters()
    if not pythons:
        print("[ERROR] No se encontró ninguna instalación de Python.")
        input("Presiona Enter para salir...")
        return
    
    print("[*] Buscando auto-py-to-exe en las instalaciones de Python disponibles...")
    for py in pythons:
        print(f"    Probando: {py}")
        if check_auto_py_to_exe(py):
            print(f"[OK] auto-py-to-exe encontrado en: {py}")
            run_auto_py_to_exe(py)
            return
    
    # 3. No encontrado: ofrecer instalación
    print("\n[ERROR] No se encontró auto-py-to-exe en ninguna instalación de Python.\n")
    respuesta = input("¿Deseas instalarlo ahora con pip? (S/N): ").strip().lower()
    if respuesta == "s":
        print("\nInstalaciones de Python disponibles:")
        for i, py in enumerate(pythons, start=1):
            print(f"  {i}. {py}")
        try:
            seleccion = int(input("Selecciona el número de Python para instalar: "))
            if 1 <= seleccion <= len(pythons):
                py_elegido = pythons[seleccion - 1]
                if install_auto_py_to_exe(py_elegido):
                    print("\nInstalación completada. Ejecutando auto-py-to-exe...")
                    run_auto_py_to_exe(py_elegido)
                else:
                    print("No se pudo instalar. Verifica tu conexión y permisos.")
                    input("Presiona Enter para salir...")
            else:
                print("Número inválido.")
                input("Presiona Enter para salir...")
        except ValueError:
            print("Entrada inválida.")
            input("Presiona Enter para salir...")
    else:
        print("Instalación cancelada.")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
