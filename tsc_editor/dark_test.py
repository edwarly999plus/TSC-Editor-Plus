import tkinter as tk
from tkinter import Menu
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import pywinstyles

root = tb.Window(themename="darkly")
root.title("Mi App Oscura")
root.geometry("800x600")
pywinstyles.change_header_color(root, "#222222")

# Frame superior que actuará como barra de menús personalizada
menu_bar = tb.Frame(root, bootstyle="secondary", height=30)
menu_bar.pack(side="top", fill="x")
menu_bar.pack_propagate(False)

# Función para crear menú desplegable oscuro
def crear_menu_desplegable(parent, opciones):
    menu = Menu(parent, tearoff=0, bg="#222222", fg="white",
                activebackground="#444444", activeforeground="white")
    for opcion in opciones:
        if opcion == "-":
            menu.add_separator()
        else:
            menu.add_command(label=opcion, command=lambda o=opcion: print(f"Seleccionado: {o}"))
    return menu

# Botón "Archivo"
btn_archivo = tb.Button(menu_bar, text="Archivo", bootstyle="secondary-outline")
btn_archivo.pack(side="left", padx=2, pady=2)
menu_archivo = crear_menu_desplegable(root, ["Nuevo", "Abrir", "Guardar", "-", "Salir"])
btn_archivo.bind("<Button-1>", lambda e: menu_archivo.post(e.widget.winfo_rootx(), e.widget.winfo_rooty() + btn_archivo.winfo_height()))

# Botón "Editar"
btn_editar = tb.Button(menu_bar, text="Editar", bootstyle="secondary-outline")
btn_editar.pack(side="left", padx=2, pady=2)
menu_editar = crear_menu_desplegable(root, ["Cortar", "Copiar", "Pegar"])
btn_editar.bind("<Button-1>", lambda e: menu_editar.post(e.widget.winfo_rootx(), e.widget.winfo_rooty() + btn_editar.winfo_height()))

# Tu Canvas donde se escribe
canvas = tk.Canvas(root, bg="#333333", highlightthickness=0)
canvas.pack(fill="both", expand=True)

root.mainloop()