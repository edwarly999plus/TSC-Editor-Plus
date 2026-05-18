<div align="center">

<img width="154" height="154" alt="a779d220-24ba-4e2f-810a-0c4fcc022194" src="https://github.com/user-attachments/assets/13de0e36-b6f7-47fe-9043-5aa3e78dfaa7" /> 

# 🚀 TSC Editor+


![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)
![Cave Story](https://img.shields.io/badge/Game-Cave%20Story-orange)
![Encoding](https://img.shields.io/badge/Encoding-Shift--JIS%20%7C%20UTF--8-informational)
![Version](https://img.shields.io/badge/Version-1.1-blueviolet)

A powerful multi-language editor for `.tsc` script files used in the Cave Story engine and its variants.
Built with **Python + Tkinter**, **TSC Editor+** is focused on improving the workflow of modders, translators, and script editors with advanced tools, syntax highlighting, documentation systems, and project management features.

---

<div align="left">

# ✨ Features

## 🌍 Multi-language Interface

Supports:

* 🇺🇸 English
* 🇪🇸 Español
* 🇯🇵 日本語

---

## 🛠️ Advanced `.tsc` Support

* 🔍 **Manual encoding/cipher selection** – Dialog with live preview (Shift-JIS, CP932, Latin-1, UTF-8, CP850)
* ⚙️ **Persistent loading modes** – Auto‑detect, ask per file, or fixed encoding/cipher (saved in settings)
* 🔐 Cipher/encryption detection (fixed for non‑negative values)
* 🎨 Syntax highlighting
* ⚠️ Syntax validation
* 🧠 Smart replacement of unsupported special characters
* 🧾 Quick command documentation (now with song names, face sprites, sound effect names)
* 🧩 Custom command support

---

## 📁 Project Management

* 📂 Open/save `.cstsc` projects
* 📦 Load full folders of `.tsc` files
* 💾 Auto-save system
* 🕘 Edit history tracking

---

## ✏️ Editing Utilities

* 🔎 Search & Replace
* 🔠 Whole word / case-sensitive search
* 📏 Character counters
* 🧮 Syntax analyzer
* 🧬 Hex dump viewer
* ↩️ Undo / Redo support
* ⚠️ Unsaved changes detection

---

## 🎮 Game Integration

* 🚀 Launch the game directly using `doukutsu.exe`
* ⚡ Quick testing with `F5`

---

## 🎨 UI Customization

* 🌙 **Three themes**: Darkly (blue/dark), Vapor (purple/dark), Cosmo (light)
* 🔤 Custom fonts
* 🔍 Adjustable font sizes
* 🎨 Custom command colors
* 📋 **Sidebar file highlight** – current file in blue/purple

---

# 📸 Screenshots

<img width="1366" height="700" alt="image" src="https://github.com/user-attachments/assets/7dc320a7-5ecd-4aea-954b-1f6b2b2dbaac" />
<img width="1366" height="718" alt="image" src="https://github.com/user-attachments/assets/5fd3f5b1-4316-480c-b5f1-85aff28d86aa" />
<img width="1366" height="718" alt="image" src="https://github.com/user-attachments/assets/f33a6b13-811e-4db1-94da-cb3a922d00cb" />


---

# 📦 Requirements

* 🐍 Python 3.8+
* 🪟 Tkinter

*Note: Python 3.14 is fully supported.*

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/edwarly999plus/tsc-editor-plus.git
cd tsc-editor-plus
```

Run the editor:

```bash
python main.py
```

The first run will automatically install required libraries (`ttkbootstrap`, `Pillow`, `pywinstyles`) into a local `libs/` folder.  
If automatic installation fails, you can manually install them with:

```bash
python -m pip install ttkbootstrap==1.10.1
python -m pip install pillow==10.0.0
python -m pip install pywinstyles==1.8
```

---

# 📂 Supported File Types

| 📄 Extension | 📘 Description            |
| ------------ | ------------------------- |
| `.tsc`       | Cave Story script files   |
| `.cstsc`     | TSC Editor+ project files |
| `.txt`       | Plain text files          |

---

# ⌨️ Keyboard Shortcuts

| ⌨️ Shortcut              | 🧩 Action               |
| ------------------------ | ----------------------- |
| `Ctrl + O`               | Open `.tsc`             |
| `Ctrl + Shift + O`       | Open project            |
| `Ctrl + Shift + Alt + O` | Open folder             |
| `Ctrl + S`               | Save project            |
| `Ctrl + Shift + S`       | Export `.tsc`           |
| `Ctrl + F`               | Search                  |
| `Ctrl + R`               | Smart replace           |
| `Ctrl + Z`               | Undo                    |
| `Ctrl + Y`               | Redo                    |
| `F5`                     | Test game               |
| `Ctrl + H`               | Show history            |
| `Ctrl + Shift + C`       | Command syntax analyzer |

---

# 🧠 Built-In Tools

## 🎨 Syntax Highlighting

TSC commands, IDs, events, and errors are highlighted automatically.

## 📚 Quick Documentation

Browse built-in command documentation directly inside the editor.  
Now with extra info: song names for `<CMU>`, face sprites for `<FAC>`, sound effect names for `<SOU>`.

## 🧹 Smart Replace

Automatically converts problematic characters commonly unsupported by classic TSC encodings.

## 🔍 Manual Encoding Selection

You can now choose the exact encoding and cipher when opening a `.tsc` file, with a live preview.  
This completely solves the “?” character problem for Japanese TSC files.

---

# 🗂️ Project Structure

```text
project/
│
├── main.py
├── settings.json
├── /libs
├── /tsc_editor
├── /faces
└── /Test TSC
```

*Additional folders (optional):*  
`faces/free/` – for face sprites (`fac_sprite_free00.png`, …)  
`libs/` – auto‑downloaded dependencies

---

# 📜 License

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

# 🤝 Contributing

Pull requests, ideas, and bug reports are welcome! 🎉

If you find an issue:

1. 🍴 Fork the repository
2. 🛠️ Make your changes
3. 📩 Submit a pull request

---

# ❤️ Credits

* Inspired by the amazing modding community around Cave Story
* Developed with 🐍 Python + Tkinter
* Carrot Lord's Encryptor and Decryptor (Booster's Lab / Cave Editor) was used

---

# 👨‍💻 Author

Created by **EdwarlyGamer999+** ✨
