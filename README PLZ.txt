================================================================================
                    TSC EDITOR+ - VERSION 2.1
================================================================================

Thank you for using TSC Editor+, the professional editor for Cave Story .tsc files.

Version 2.1 is a major update focused on full internationalization, backup system,
batch character replacement, and many stability improvements.

--------------------------------------------------------------------------------
WHAT'S NEW IN VERSION 2.1
--------------------------------------------------------------------------------

1. FULL INTERNATIONALIZATION (English / Español / 日本語)
   • All menus, dialogs, messages, history entries, and status bar texts are now fully translatable.
   • No more hardcoded English strings – the interface adapts to your selected language.
   • Language can be changed at any time in Settings (Ctrl+K).

2. BACKUP SYSTEM
   • Backup current TSC file (Ctrl+B) – creates a dated subfolder and copies the file.
   • Backup all TSC files in the loaded folder (Ctrl+Shift+B) – batch backup with progress bar.
   • Configurable backup directory in Settings (custom folder or default "backups/" in project root).
   • Backups are never overwritten (new timestamp each time).

3. SMART REPLACE ALL TSC FILES
   • Applies the same smart character replacement (ñ→n, accents removal, ¡¿ removal) to every .tsc file in the loaded folder.
   • Shows a progress bar with file names and reports results (processed, modified, errors).
   • Ideal for mass‑cleaning TSC files before distribution.

4. ENCODING & CIPHER IMPROVEMENTS
   • Auto‑detection now properly distinguishes between cp1252 (Spanish) and shift_jis (Japanese/English).
   • Fallback chain for Shift‑JIS: shift_jis → cp1252 → cp932 → latin‑1.
   • Suspicious characters (»½«°©¾±÷×) trigger an automatic correction to shift_jis or cp1252.
   • Removed forced UTF‑8 when cipher=0 – TSC files are never saved as UTF‑8 unless explicitly chosen in manual export mode.

5. COMMAND INFO ENHANCEMENTS (continued)
   • <FAIxxxx> and <FAOxxxx> now display the direction name (Left, Up, Right, Down, Center, INVALID).
   • <TRAxxxx> shows the full map name (Arthur's House, Egg Corridor, etc.).
   • <AM+>, <AM->, <AMJ>, <GIT>, <TAM> show weapon names (Snake, Polar Star, etc.).
   • <GIT>, <IT+>, <IT->, <ITJ> show item names (Arthur's Key, Map System, etc.).
   • <SOUxxxx> includes descriptive sound effect names (e.g., "Message typing", "Door", "Explosion").

6. QUICK DOCS HINTS
   • A rotating hint panel appears at the bottom of the Quick Docs tab.
   • Hints change every 5 seconds and are translated into English, Spanish and Japanese.
   • Provides useful tips (e.g., character counter, saving backups, cipher issues).

7. MINOR UI & STABILITY IMPROVEMENTS
   • Unsaved changes detection is now reliable (no false positives).
   • The currently opened file in the sidebar is highlighted in a distinct colour.
   • Settings window respects the selected theme (dark/vapor/cosmo) and includes a scrollbar.
   • Removed all pygame dependencies – works natively on Python 3.14.
   • No AI assistant – removed due to API quotas and reliability concerns.
   • Fixed many small bugs (KeyError, UnboundLocalError, etc.) reported by users.

8. NEW KEYBOARD SHORTCUTS (v2.1)
   • Ctrl+B       – Backup current TSC file
   • Ctrl+Shift+B – Backup all TSC files in the list

--------------------------------------------------------------------------------
PERSISTENT RECENT FOLDER
--------------------------------------------------------------------------------

Settings → "Keep recent TSC folder on startup"
When enabled, the last opened folder is automatically loaded when you restart the editor.

--------------------------------------------------------------------------------
ENCODING & CIPHER SELECTION – MANUAL CONTROL
--------------------------------------------------------------------------------

• When opening a .tsc file, you can manually choose:
     - Encoding (Shift-JIS, CP932, Latin-1, UTF-8, CP850, CP1252)
     - Cipher (Auto-detect, None (0), or a manual value 0-255)
• A live preview shows the first 816 bytes decoded with your current settings.
• This completely solves the "?" character problem for Japanese TSC files.
• Auto-detection is still available as a "Suggest" button.

--------------------------------------------------------------------------------
PERSISTENT LOADING MODES (Settings)
--------------------------------------------------------------------------------

Three loading behaviours can be selected in the Settings window:
   • Always auto-detect (fast, no dialogs)
   • Always ask per file (the new manual dialog)
   • Always use a fixed encoding & cipher (manual override)
Your choice is saved in settings.json.

--------------------------------------------------------------------------------
EXPORT MODES (Settings)
--------------------------------------------------------------------------------

Three export behaviours are available:
   • Auto – uses the same encoding and cipher as the opened file (recommended)
   • Ask per export – shows a dialog to choose encoding and cipher each time
   • Manual – always uses a fixed encoding and cipher (set in Settings)

--------------------------------------------------------------------------------
UNSAVED CHANGES DETECTION
--------------------------------------------------------------------------------

The editor now correctly detects real modifications (no false positives).
When you try to change files, load a folder, or close the program, you will be asked:
   • Save changes (Yes) → saves current file, then continues
   • Discard changes (No) → reverts to last saved state
   • Cancel → stays on current file

--------------------------------------------------------------------------------
THEME ENHANCEMENTS
--------------------------------------------------------------------------------

Three built-in themes are available (change in Settings):
   • Darkly   – Standard dark theme (blue accents)
   • Vapor    – Dark theme with purple/magenta tones
   • Cosmo    – Light theme (white background, black text)

The theme toggle button on the toolbar alternates between Darkly and Cosmo.

--------------------------------------------------------------------------------
SIDEBAR IMPROVEMENTS
--------------------------------------------------------------------------------

• The currently opened TSC file is highlighted in blue (Darkly/Cosmo) or purple (Vapor).
• Clicking another file triggers the unsaved changes dialog.
• If you cancel file switching, the original highlight is restored.

--------------------------------------------------------------------------------
LANGUAGE SUPPORT
--------------------------------------------------------------------------------

The interface is fully translated into English, Spanish and Japanese.
The editor automatically detects your system language on first run, but you can change it manually in Settings (Ctrl+K).

--------------------------------------------------------------------------------
DEPENDENCIES (Libraries used by TSC Editor+)
--------------------------------------------------------------------------------

The program automatically installs the following Python libraries (if missing) into the
`libs` folder inside the program directory. No manual installation is required.

| Library         | Purpose                                                      | Version used | Python version requirement            |
|-----------------|--------------------------------------------------------------|--------------|----------------------------------------|
| ttkbootstrap    | Modern, theme‑able GUI widgets (dark/light themes)           | 1.10.1       | Python ≥ 3.7                           |
| Pillow (PIL)    | Displaying face images (FAC command)                         | 10.0.0       | Python ≥ 3.8                           |
| pywinstyles     | Change Windows title bar color to match dark/light theme     | 1.8          | Python ≥ 3.7 (Windows only)            |

**Additional notes:**
- The editor itself requires **Python 3.8 or newer**.
- `pywinstyles` works only on **Windows**. On other operating systems, the title bar color will not change.
- These libraries are only needed for enhanced features; the editor remains functional even if some are missing (e.g., without Pillow, face images will not be shown).

--------------------------------------------------------------------------------
MANUAL INSTALLATION COMMANDS (If automatic download fails)
--------------------------------------------------------------------------------

If the automatic installer cannot download the libraries (e.g., no internet, proxy issues,
or permission problems), you can install them manually using pip. Open a terminal (cmd
or PowerShell) in the program's root folder (where `main.py` is located) and run:

   python -m pip install ttkbootstrap==1.10.1 --target libs
   python -m pip install pillow==10.0.0 --target libs
   python -m pip install pywinstyles==1.8 --target libs

Alternatively, you can install them globally (without `--target libs`) if you prefer,
but then the program will not use the local `libs` folder.

After manual installation, run `main.py` normally.

--------------------------------------------------------------------------------
KEYBOARD SHORTCUTS
--------------------------------------------------------------------------------

| Shortcut              | Action                         |
|-----------------------|--------------------------------|
| Ctrl + O              | Open .tsc                      |
| Ctrl + Shift + O      | Open project (.cstsc)          |
| Ctrl + Shift + Alt + O| Open folder                    |
| Ctrl + S              | Save project                   |
| Ctrl + Shift + S      | Export .tsc (or .txt)          |
| Ctrl + B              | Backup current TSC             |
| Ctrl + Shift + B      | Backup all TSC files           |
| Ctrl + F              | Focus search tab               |
| Ctrl + R              | Smart replace                  |
| Ctrl + Z              | Undo                           |
| Ctrl + Y              | Redo                           |
| Ctrl + H              | Show history                   |
| Ctrl + K              | Open settings                  |
| Ctrl + Shift + C      | Command syntax analyzer        |
| Ctrl + N / Ctrl + T   | New empty tab                  |
| Ctrl + W              | Close current tab              |
| Ctrl + Shift + W      | Close all tabs                 |
| Ctrl + Alt + W        | Close other tabs               |
| F5                    | Test game                      |
| Alt + F4              | Exit                           |

--------------------------------------------------------------------------------
SWITCH ANIMATION FOLDER STRUCTURE
--------------------------------------------------------------------------------

For animated Switch faces, the editor expects the following folder layout
(in the root of the project, next to `main.py`):

faces/
└── switch/
    ├── anim1/   (Idle eyes open / Talk mouth closed)
    ├── anim2/   (Talk mouth half‑open)
    ├── anim3/   (Talk mouth fully open)
    ├── anim4/   (Idle eyes half‑closed)
    └── anim5/   (Idle eyes closed)

File naming examples for character ID 15 (Misery):
   • Idle (anim1):  fac_sprite_switch15.png
   • Idle (anim4):  fac_sprite_switch415.png
   • Idle (anim5):  fac_sprite_switch515.png
   • Talk (anim2):  fac_sprite_switch215.png
   • Talk (anim3):  fac_sprite_switch315.png

You can also use full 4‑digit codes (e.g., fac_sprite_switch1115.png) or padded codes
(e.g., fac_sprite_switch07.png). The editor searches in priority: full → padded → short.

--------------------------------------------------------------------------------
KNOWN ISSUES / NOTES
--------------------------------------------------------------------------------

• Face sprites (Freeware) require `faces/free/` with `fac_sprite_free00.png` to `fac_sprite_free30.png`
• Face sprites (Steam) require `faces/steam/` with `fac_sprite_steam00.png` to `fac_sprite_steam30.png`
• The hex dump view only shows the first 512 bytes (to avoid performance issues).
• For Japanese TSC files, always choose **Shift-JIS** or **CP932** encoding in the load dialog.
• The cipher value is rarely needed; “Auto-detect” works for 99.7% of original Cave Story TSC files.

--------------------------------------------------------------------------------
CREDITS & CONTACT
--------------------------------------------------------------------------------

TSC Editor+ is created for the Cave Story modding community.
Special thanks to IdioticBaka1824, LAIB and all testers who reported bugs and suggested improvements.

If you encounter any issue, please open a ticket on the project repository or the Cave Story Forum Thread.

Enjoy modding!

-- EdwarlyGamer999+
================================================================================
