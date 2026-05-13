# TSC Editor+

A powerful multi-language editor for `.tsc` script files used in the Cave Story engine and its variants.
Built with Python and Tkinter, **TSC Editor+** focuses on script editing, syntax highlighting, quick documentation, project management, and workflow improvements for modders.

---

## Features

* Multi-language interface

  * English
  * Español
  * 日本語

* Advanced `.tsc` support

  * Automatic encoding detection
  * Cipher detection/decryption
  * Syntax highlighting
  * Syntax validation
  * Smart special character replacement

* Project tools

  * Open/save `.cstsc` projects
  * Load full project folders
  * Auto-save support
  * History tracking

* Editing utilities

  * Search & Replace
  * Whole word / case sensitive search
  * Character counters
  * Hex dump viewer
  * Undo / Redo support

* Command system

  * Built-in TSC command documentation
  * Quick Docs panel
  * Custom commands
  * Custom command syntax analyzer
  * Command color customization

* Game integration

  * Launch game directly with `doukutsu.exe`
  * Quick testing with `F5`

* UI customization

  * Dark theme
  * Configurable fonts
  * Adjustable font sizes

---

## Screenshots
<img width="1366" height="719" alt="image" src="https://github.com/user-attachments/assets/e4d92741-0381-4349-85f4-e84f3abb4e6a"/>


---

## Requirements

* Python 3.9+
* Tkinter

---

## Installation

Clone the repository:

```bash
git clone https://github.com/edwarly999plus/TSC-Editor-Plus.git
cd tsc-editor-plus
```

Run the editor:

```bash
python main.py
```

---

## Supported File Types

| Extension | Description               |
| --------- | ------------------------- |
| `.tsc`    | Cave Story script files   |
| `.cstsc`  | TSC Editor+ project files |
| `.txt`    | Plain text                |

---

## Keyboard Shortcuts

| Shortcut                 | Action                  |
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

## Built-In Tools

### Syntax Highlighting

TSC commands, IDs, events, and errors are highlighted automatically.

### Quick Documentation

Browse built-in command documentation directly inside the editor.

### Smart Replace

Automatically converts problematic characters commonly unsupported by classic TSC encodings.

### Auto Encoding Detection

The editor attempts to detect:

* Shift-JIS
* CP932
* UTF-8
* Latin-1
* CP850

It also supports encrypted/freeware TSC formats.

---

## Project Structure

```text
project/
│
├── main.py
├── settings.json
├── custom_commands.json
├── command_colors.json
├── Cave-Story.ttf
└── Lucida Grande Regular.ttf
```

---

## Planned Features

* Plugin system
* More TSC command presets
* Better script analysis
* Linux/macOS testing
* Integrated event navigator
* Export improvements

---

## License

This project is currently unlicensed.
Add a license file if you plan to distribute or accept contributions.

---

## Credits

* Inspired by the modding community around Cave Story
* Developed with Python + Tkinter

---

## Contributing

Pull requests, bug reports, and suggestions are welcome.

If you find issues:

1. Open an issue
2. Describe the problem clearly
3. Include screenshots or sample `.tsc` files if possible

---

## Author

Created by **Edwarly Castillo Silverio**.
