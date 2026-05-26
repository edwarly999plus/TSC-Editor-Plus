# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import messagebox
import random

# Directorio raíz del proyecto (un nivel arriba de este archivo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def get_switch_config():
    config_path = os.path.join(BASE_DIR, "FaceAnimation.json")
    default = {
        "fps": 7,
        "image_size": 96,
        "blink": {"enabled": True, "min_interval": 1, "max_interval": 7}
    }
    if os.path.isfile(config_path):
        try:
            import json
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                default.update(cfg)
        except:
            pass
    return default


def is_placeholder_green(img):
    if not PIL_AVAILABLE:
        return False
    if img.mode != 'RGB':
        img = img.convert('RGB')
    colors = img.getcolors(maxcolors=2)
    return colors is not None and len(colors) == 1 and colors[0][1] == (0, 255, 33)


def _get_full_code(face_id):
    return str(face_id).strip().zfill(4)


def _get_padded_code(face_id):
    return _get_full_code(face_id)[-2:]


def _get_short_code(face_id):
    return str(int(_get_padded_code(face_id)))


def _get_prefixes_for_folder(folder_name, face_id):
    full = _get_full_code(face_id)
    padded = _get_padded_code(face_id)
    short = _get_short_code(face_id)
    base = "fac_sprite_switch"
    if folder_name == "anim2":
        base = "fac_sprite_switch2"
    elif folder_name == "anim3":
        base = "fac_sprite_switch3"
    elif folder_name == "anim4":
        base = "fac_sprite_switch4"
    elif folder_name == "anim5":
        base = "fac_sprite_switch5"
    return [base + full, base + padded, base + short]


def load_frames_from_folder(folder_name, face_id, image_size, skip_green=True):
    if not PIL_AVAILABLE:
        return []
    folder_path = os.path.join(BASE_DIR, "faces", "switch", folder_name)
    if not os.path.isdir(folder_path):
        return []
    prefixes = _get_prefixes_for_folder(folder_name, face_id)
    files = []
    for prefix in prefixes:
        candidates = [f for f in os.listdir(folder_path)
                      if f.lower().startswith(prefix.lower()) and f.lower().endswith('.png')]
        if candidates:
            files = candidates
            break
    files.sort()
    frames = []
    for fname in files:
        img_path = os.path.join(folder_path, fname)
        try:
            img = Image.open(img_path)
            if skip_green and is_placeholder_green(img):
                continue
            if img.width != image_size or img.height != image_size:
                img = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            frames.append(photo)
        except Exception:
            continue
    return frames


def animate_idle_with_blink(parent, face_id, settings):
    config = get_switch_config()
    size = config["image_size"]
    open_frames = load_frames_from_folder("anim1", face_id, size)
    half_frames = load_frames_from_folder("anim4", face_id, size)
    closed_frames = load_frames_from_folder("anim5", face_id, size)

    if not open_frames:
        messagebox.showerror("Error", f"No se encontraron imágenes válidas para la cara {face_id} en anim1")
        return

    # Si ambas half y closed están vacías (solo placeholders verdes) -> estático
    if not half_frames and not closed_frames:
        win = tk.Toplevel(parent)
        win.title(f"Switch - {face_id} (Idle estático)")
        dark = settings.get("dark_theme", False) if settings else False
        bg = "#1e1e1e" if dark else "#ffffff"
        win.configure(bg=bg)
        label = tk.Label(win, image=open_frames[0], bg=bg)
        label.image = open_frames[0]
        label.pack(padx=10, pady=10)
        btn_style = {"bg": "#3c3c3c" if dark else "#e0e0e0",
                     "fg": "white" if dark else "black"}
        tk.Button(win, text="Cerrar", command=win.destroy, **btn_style).pack(pady=5)
        return

    # Al menos una tiene imágenes reales -> hacemos parpadeo (fallback con open_frames)
    open_img = open_frames[0]
    half_img = half_frames[0] if half_frames else open_img
    closed_img = closed_frames[0] if closed_frames else open_img

    win = tk.Toplevel(parent)
    win.title(f"Switch - {face_id} (Idle con parpadeo)")
    dark = settings.get("dark_theme", False) if settings else False
    bg = "#1e1e1e" if dark else "#ffffff"
    win.configure(bg=bg)

    label = tk.Label(win, image=open_img, bg=bg)
    label.image = open_img
    label.pack(padx=10, pady=10)

    blink_id = None
    state = "open"
    min_int = config["blink"]["min_interval"]
    max_int = config["blink"]["max_interval"]

    def set_img(img):
        label.config(image=img)
        label.image = img

    def restore():
        nonlocal state, blink_id
        set_img(open_img)
        state = "open"
        blink_id = None
        schedule()

    def close_blink():
        nonlocal state, blink_id
        if state == "half":
            set_img(closed_img)
            state = "closed"
            blink_id = win.after(200, restore)
        elif state == "closed":
            restore()

    def do_blink():
        nonlocal state, blink_id
        if state != "open":
            return
        set_img(half_img)
        state = "half"
        blink_id = win.after(100, close_blink)

    def schedule():
        nonlocal blink_id
        if blink_id:
            win.after_cancel(blink_id)
        interval = random.randint(min_int, max_int) * 1000
        blink_id = win.after(interval, do_blink)

    schedule()

    def on_close():
        if blink_id:
            win.after_cancel(blink_id)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)
    btn_style = {"bg": "#3c3c3c" if dark else "#e0e0e0",
                 "fg": "white" if dark else "black"}
    tk.Button(win, text="Cerrar", command=on_close, **btn_style).pack(pady=5)


def animate_talk(parent, face_id, settings):
    config = get_switch_config()
    size = config["image_size"]
    fps = config["fps"]
    delay = int(1000 / fps) if fps > 0 else 143

    frames1 = load_frames_from_folder("anim1", face_id, size)
    frames2 = load_frames_from_folder("anim2", face_id, size)
    frames3 = load_frames_from_folder("anim3", face_id, size)

    if not frames1:
        messagebox.showerror("Error", f"No hay imágenes en anim1 para la cara {face_id}")
        return
    if not frames2:
        frames2 = frames1
    if not frames3:
        frames3 = frames1

    all_frames = frames1 + frames2 + frames3

    win = tk.Toplevel(parent)
    win.title(f"Switch - {face_id} (Talk)")
    dark = settings.get("dark_theme", False) if settings else False
    bg = "#1e1e1e" if dark else "#ffffff"
    win.configure(bg=bg)

    label = tk.Label(win, bg=bg)
    label.pack(padx=10, pady=10)

    idx = 0
    after_id = None

    def update():
        nonlocal idx, after_id
        label.config(image=all_frames[idx])
        label.image = all_frames[idx]
        idx += 1
        if idx >= len(all_frames):
            idx = 0
        after_id = win.after(delay, update)

    update()

    def on_close():
        if after_id:
            win.after_cancel(after_id)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)
    btn_style = {"bg": "#3c3c3c" if dark else "#e0e0e0",
                 "fg": "white" if dark else "black"}
    tk.Button(win, text="Cerrar", command=on_close, **btn_style).pack(pady=5)


def show_switch_anim_dialog(parent_window, face_id, settings=None):
    if face_id == "0000":
        messagebox.showinfo("Info", "ID 0000 representa 'Nada', no hay animación.")
        return

    anim1_path = os.path.join(BASE_DIR, "faces", "switch", "anim1")
    if not os.path.isdir(anim1_path):
        messagebox.showerror("Error", "No se encuentra la carpeta faces/switch/anim1\nAsegúrate de que exista en la raíz del proyecto.")
        return

    dark = settings.get("dark_theme", False) if settings else False
    bg = "#1e1e1e" if dark else "#ffffff"
    fg = "white" if dark else "black"
    btn_bg = "#3c3c3c" if dark else "#e0e0e0"
    btn_fg = "white" if dark else "black"

    dialog = tk.Toplevel(parent_window)
    dialog.title("Switch - Seleccionar modo")
    dialog.geometry("300x120")
    dialog.transient(parent_window)
    dialog.grab_set()
    dialog.configure(bg=bg)

    tk.Label(dialog, text=f"Cara ID: {face_id}\n¿Qué animación quieres ver?", bg=bg, fg=fg).pack(pady=10)

    btn_frame = tk.Frame(dialog, bg=bg)
    btn_frame.pack(pady=10)

    def start_idle():
        dialog.destroy()
        animate_idle_with_blink(parent_window, face_id, settings)

    def start_talk():
        dialog.destroy()
        animate_talk(parent_window, face_id, settings)

    tk.Button(btn_frame, text="Idle (parpadeo)", command=start_idle, bg=btn_bg, fg=btn_fg).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Talk (habla)", command=start_talk, bg=btn_bg, fg=btn_fg).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg=btn_bg, fg=btn_fg).pack(side=tk.LEFT, padx=5)


def auto_switch_animation(parent_window, face_id, settings=None):
    if face_id.startswith("10"):
        animate_idle_with_blink(parent_window, face_id, settings)
    elif face_id.startswith("11") or face_id.startswith("01"):
        animate_talk(parent_window, face_id, settings)
    else:
        show_switch_anim_dialog(parent_window, face_id, settings)