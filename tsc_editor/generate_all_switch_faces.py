import os
from PIL import Image, ImageDraw, ImageFont

def generate_all_switch_faces():
    size = 96
    bg_color = (50, 50, 50)
    text_color = (255, 255, 255)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    switch_dir = os.path.join(base_dir, "faces", "switch")

    # Definir carpetas y prefijos
    folders = {
        "anim1": "fac_sprite_switch",
        "anim2": "fac_sprite_switch2",
        "anim3": "fac_sprite_switch3",
        "anim4": "fac_sprite_switch4",
        "anim5": "fac_sprite_switch5"
    }

    for face_id in range(1, 30):  # IDs 1 al 29
        id_str = str(face_id)  # "1", "2", ...
        for folder, prefix in folders.items():
            folder_path = os.path.join(switch_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            filename = f"{prefix}{id_str}.png"
            filepath = os.path.join(folder_path, filename)
            img = Image.new("RGB", (size, size), bg_color)
            draw = ImageDraw.Draw(img)
            text = f"ID {face_id:02d}\n{folder}"
            draw.text((size//2, size//2), text, fill=text_color, font=font, anchor="mm")
            img.save(filepath)
            print(f"Generado: {filepath}")
    print("¡Todas las imágenes placeholder generadas para anim1..anim5!")

if __name__ == "__main__":
    generate_all_switch_faces()