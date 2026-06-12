<div align="center">

<img width="154" height="154" alt="TSC Editor+ Logo" src="https://github.com/user-attachments/assets/13de0e36-b6f7-47fe-9043-5aa3e78dfaa7" /> 

# 🚀 TSC Editor+ v2.1

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)
![Cave Story](https://img.shields.io/badge/Game-Cave%20Story-orange)
![Encoding](https://img.shields.io/badge/Encoding-Shift--JIS%20%7C%20UTF--8%20%7C%20CP850-informational)
![Version](https://img.shields.io/badge/Version-2.1-blueviolet)

**A professional multi‑language editor for `.tsc` script files (Cave Story engine).**  
Built with **Python + Tkinter**, TSC Editor+ streamlines modding, translation, and script editing with advanced tools, syntax highlighting, inline documentation, and full support for **Nintendo Switch animated faces**.

---

</div>

## ✨ Features

### 🌍 Fully Multi‑language Interface (v2.1)
- 🇺🇸 English – 🇪🇸 Español – 🇯🇵 日本語  
- All dialogs, menus, messages, and history entries are now translatable (no hardcoded strings).

### 🛠️ Advanced `.tsc` Support
- 🔍 **Manual encoding/cipher selection** – live preview (Shift‑JIS, CP932, Latin‑1, UTF‑8, CP850)  
- ⚙️ **Persistent loading modes** – auto‑detect, ask per file, or fixed encoding/cipher (saved in `settings.json`)  
- 🔐 Full cipher detection (fixed for non‑negative values)  
- 🎨 **Syntax highlighting** (commands, events, numbers, special characters)  
- ⚠️ **Syntax validation**  
- 🧠 **Smart replace** (single file or **batch all TSC files**) – converts unsupported characters (ñ, accents, ¡¿)  
- 📚 **Quick command documentation** – song names, face sprites, sound effects, map names, weapon/item names, direction names  
- 🧩 **Custom command support** (add/edit/delete your own commands)  
- 🎨 **Custom command colors** (blue, pink, red)

### 🎮 Nintendo Switch Animation Support
- **Switch animated faces** for commands `<FAC10XX>` (Idle blinking), `<FAC11XX>` (Talk), `<FAC00XX>` (static)  
- **Auto‑detection** – right‑click and the correct animation starts immediately  
- **Smart image loading** – placeholders (pure green `#00FF21`) are automatically skipped  
- **Multiple naming formats** – accepts full 4‑digit codes, padded or short names  
- **Fallback to static** when blink frames are missing

### 📁 Project Management & Backup
- 📂 Open/save `.cstsc` projects (UTF‑8, no encryption)  
- 📦 Load entire folders of `.tsc` files  
- 💾 Auto‑save every 6 minutes (optional)  
- 🕘 Edit history tracking  
- 🔒 **Backup individual TSC (Ctrl+B)** or **all TSC files (Ctrl+Shift+B)**  
- 🗂️ Configurable backup directory (custom folder or default `backups/` in project root)

### ✏️ Editing Utilities
- 🔎 Search & Replace with real‑time highlighting  
- 📏 **Character counters** (normal and with face limit)  
- 🧮 **Command syntax analyzer** (Ctrl+Shift+C)  
- 🧬 Hex dump viewer (first 512 bytes)  
- ↩️ Undo / Redo  
- ⚠️ **Unsaved changes detection** (no false positives)  
- 🗂️ **Modern tabs** – Ctrl+T new tab, Ctrl+W close, Ctrl+Shift+W close all, Ctrl+Alt+W close others  
- ❌ Tab close button (“✕”) and right‑click context menu

### 🎮 Game Integration
- 🚀 Launch the game directly from the editor  
- ⚡ Quick test with `F5`

### 🎨 UI Customization
- 🌙 **Three themes**: Darkly (blue/dark), Vapor (purple/dark), Cosmo (light)  
- 🔤 Custom fonts (Courier New, Consolas, Lucida Grande, Noto Sans JP, etc.)  
- 🔍 Adjustable font size (Ctrl+MouseWheel)  
- 🎨 **Custom command colors** (blue, pink, red)  
- 📋 **Sidebar file highlight** – current file in blue/purple  
- 💡 **Rotating hints** in the Quick Docs panel (every 5 seconds, translated)

### 🆕 What's New in v2.1
- **Full internationalization** – all UI strings, dialogs, history entries, and error messages are translatable (en/es/jp).  
- **Backup system** – backup current TSC (Ctrl+B) or all TSC files (Ctrl+Shift+B) to a custom folder or default `backups/`.  
- **Smart Replace All TSC Files** – batch replace special characters (ñ, accents, ¡¿) in every `.tsc` file of the loaded folder.  
- **Improved encoding auto-detection** – now properly detects cp1252 (Spanish) vs shift_jis (Japanese/English).  
- **Command info enhancements** – `FAI`/`FAO` (directions), `TRA` (map names), weapons/items (`AM+`, `GIT`, etc.), sound effect descriptions.  
- **Item ID normalisation for Switch** – `GIT1004` now shows “Silver Locket”.  
- **Quick Docs hints panel** – rotating tips (English/Spanish/Japanese).  
- **Compatibility with Python 3.14** – no pygame required.

---

## 📸 Screenshots

<img width="1366" height="701" alt="Screenshot Darkly" src="https://github.com/user-attachments/assets/30023c3a-871b-4dfb-a5d8-81035215c41e" />

<img width="1366" height="717" alt="Screenshot Vapor" src="https://github.com/user-attachments/assets/ba4ced39-8c84-4eae-a759-d770d2b20896" />

<img width="1366" height="720" alt="Screenshot Cosmo" src="https://github.com/user-attachments/assets/d969445c-920a-473a-bf36-b611ffbaee82" />

---
<div align="left">

## 📦 Requirements

- 🐍 **Python 3.8+** (3.14 fully supported)  
- 🪟 Tkinter (usually bundled with Python)

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/edwarly999plus/tsc-editor-plus.git
cd tsc-editor-plus
```

Run the editor:

```bash
python main.py
```

On first run, required libraries (`ttkbootstrap`, `Pillow`, `pywinstyles`) are automatically installed into a local `libs/` folder.  
If automatic installation fails, you can manually install them:

```bash
python -m pip install ttkbootstrap==1.10.1
python -m pip install pillow==10.0.0
python -m pip install pywinstyles==1.8
```

---

## 📂 Supported File Types

| Extension | Description                   |
| --------- | ----------------------------- |
| `.tsc`    | Cave Story script files       |
| `.cstsc`  | TSC Editor+ project files     |
| `.txt`    | Plain text export             |

---

## ⌨️ Keyboard Shortcuts

| Shortcut                  | Action                         |
| ------------------------- | ------------------------------ |
| `Ctrl + O`                | Open `.tsc`                    |
| `Ctrl + Shift + O`        | Open `.cstsc` project          |
| `Ctrl + Shift + Alt + O`  | Open folder                    |
| `Ctrl + S`                | Save project                   |
| `Ctrl + Shift + S`        | Export `.tsc` (or `.txt`)      |
| `Ctrl + B`                | Backup current TSC             |
| `Ctrl + Shift + B`        | Backup all TSC files           |
| `Ctrl + F`                | Focus search tab               |
| `Ctrl + R`                | Smart replace                  |
| `Ctrl + Z`                | Undo                           |
| `Ctrl + Y`                | Redo                           |
| `F5`                      | Test game                      |
| `Ctrl + H`                | Show history                   |
| `Ctrl + K`                | Open settings                  |
| `Ctrl + Shift + C`        | Command syntax analyzer        |
| `Ctrl + N` / `Ctrl + T`   | New empty tab                  |
| `Ctrl + W`                | Close current tab              |
| `Ctrl + Shift + W`        | Close all tabs                 |
| `Ctrl + Alt + W`          | Close other tabs               |
| `Alt + F4`                | Exit                           |

---

## 🧠 Built‑In Tools

### 🎨 Syntax Highlighting  
Commands, IDs, events, errors – automatically coloured.

### 📚 Quick Documentation  
Browse command documentation directly inside the editor. Now includes:  
- Song names for `<CMU>`  
- Face names for Freeware/Steam/Switch (`<FAC>`)  
- Sound effect names for `<SOU>`  
- Map names for `<TRA>`  
- Direction names for `<FAI>`/`<FAO>`  
- Weapon names for `<AM+>`, `<AM->`, `<AMJ>`, `<GIT>`, `<TAM>`  
- Item names for `<GIT>`, `<IT+>`, `<IT->`, `<ITJ>`

### 🧹 Smart Replace  
Automatically converts problematic characters (e.g., `ñ`, accents, `¡¿`) that break classic TSC encodings.  
**Batch mode** applies to all `.tsc` files in the loaded folder (with progress bar).

### 🔍 Manual Encoding Selection  
Choose encoding and cipher with a live preview – solves the `?` character problem for Japanese TSC files.

### 💡 Rotating Hints  
Useful tips appear in the Quick Docs panel, changing every 5 seconds (translated).

### 💾 Backup System  
Create instant backups of your current `.tsc` file or all files in the project. Backups are stored in dated subfolders inside a user‑defined directory (or the default `backups/` folder).

---

## 🗂️ Project Structure

```text
tsc-editor-plus/
├── main.py
├── settings.json
├── custom_commands.json
├── command_colors.json
├── tsc_editor/          # Main package
├── libs/                # Auto‑installed dependencies
├── backups/             # Default backup folder (created on first backup)
├── faces/               # Face sprites
│   ├── free/            # Freeware sprites (fac_sprite_freeXX.png)
│   ├── steam/           # Steam sprites (fac_sprite_steamXX.png)
│   └── switch/          # Switch animated sprites
│       ├── anim1/       # Eyes open / mouth closed
│       ├── anim2/       # Talk mouth half‑open
│       ├── anim3/       # Talk mouth fully open
│       ├── anim4/       # Idle eyes half‑closed
│       └── anim5/       # Idle eyes closed
└── Cave-Story.ttf       # Optional font
```

---

## 🔧 Configuration

Settings are stored in `settings.json`:

- **Auto‑save** interval (6 min)  
- **Language** (en/es/jp)  
- **Theme** (darkly/vapor/cosmo)  
- **Default font** and size  
- **Load mode** (auto/ask/manual)  
- **Export mode** (auto/ask/manual)  
- **Backup directory** (custom path, empty = default `backups/`)  
- **Keep recent TSC folder** on startup  
- **Recent folder path**  

---

## 📜 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 EdwarlyGamer999+

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

Pull requests, ideas, and bug reports are welcome!

1. 🍴 Fork the repository  
2. 🛠️ Make your changes  
3. 📩 Submit a pull request  

---

## ❤️ Credits

- Inspired by the Cave Story modding community  
- Developed with 🐍 Python + Tkinter  
- Encryption logic based on Carrot Lord's (Booster's Lab / Cave Editor)  

---

## 👨‍💻 Author

**EdwarlyGamer999+**  
[GitHub](https://github.com/edwarly999plus)
