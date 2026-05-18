================================================================================
                    TSC EDITOR+ - PATCH 1.1
================================================================================

Thank you for using TSC Editor+, the professional editor for Cave Story .tsc files.

This patch (version 1.1) introduces important bug fixes, new features, and 
improvements to make your modding experience smoother and more reliable.

--------------------------------------------------------------------------------
WHAT'S NEW IN PATCH 1.1
--------------------------------------------------------------------------------

1. ENCODING & CIPHER SELECTION – MANUAL CONTROL
   • When opening a .tsc file, you now get a dialog to manually choose:
        - Encoding (Shift-JIS, CP932, Latin-1, UTF-8, CP850)
        - Cipher (Auto-detect, None (0), or a manual value 0-255)
   • A live preview shows the first 816 bytes decoded with your current settings.
   • This completely solves the "?" character problem for Japanese TSC files.
   • Auto detection is still available as a "Suggest" button.

2. PERSISTENT LOADING MODES (Settings)
   • Three loading behaviours can be selected in the Settings window:
        - Always auto detect (fast, no dialogs)
        - Always ask per file (the new manual dialog)
        - Always use a fixed encoding & cipher (manual override)
   • Your choice is saved in settings.json.

3. UNSAVED CHANGES DETECTION
   • The editor now correctly detects real modifications
   • When you try to change files, load a folder, or close the program, you will be asked:
        - Save changes (Yes) → saves current file, then continues
        - Discard changes (No) → reverts to last saved state
        - Cancel → stays on current file

4. THEME ENHANCEMENTS
   • Three built-in themes:
        - Darkly   (standard dark, blue accents)
        - Vapor    (dark with purple/magenta tones) (go to settings)
        - Cosmo    (light theme, white background)
   • The theme toggle button on the toolbar alternates between Darkly and Cosmo.

5. SIDEBAR IMPROVEMENTS
   • The currently opened TSC file is highlighted in blue (or purple in Vapor theme).
   • Clicking another file triggers the unsaved changes dialog.
   • If you cancel file switching, the original highlight is restored.

6. ENCRYPTION FIX
   • The `get_cipher_from_tsc` function now returns a non-negative cipher (0-255).
   • Solves a rare bug that caused garbled text when the calculated cipher was negative.

7. COMMAND INFO ENHANCEMENTS
   • For `<CMUxxxx>`: shows the official song name (based on the built-in list).
   • For `<FACxxxx>`: shows the face name and, if available, displays the corresponding
        sprite from `faces/free/fac_sprite_freeXX.png` (XX = two-digit ID).
   • For `<SOUxxxx>`: shows the sound effect name (based on the full Cave Story sound list).

8. LANGUAGE SUPPORT
   • Interface fully translated into English, Spanish and Japanese.
   • Automatically detects your system language on first run.
   • Can be changed manually in Settings.

--------------------------------------------------------------------------------
DEPENDENCIES (Libraries used by TSC Editor+)
--------------------------------------------------------------------------------

The program automatically installs the following Python libraries (if missing) into the
`libs` folder inside the program directory. No manual installation is required.

| Library         | Purpose                                                      | Version used | Python version requirement            |
|-----------------|--------------------------------------------------------------|--------------|----------------------------------------|
| ttkbootstrap    | Modern, theme-able GUI widgets (dark/light themes)           | 1.10.1       | Python ≥ 3.7                           |
| Pillow (PIL)    | Displaying face images (FAC command)                         | 10.0.0       | Python ≥ 3.8                           |
| pywinstyles     | Change Windows title bar color to match dark/light theme     | 1.8          | Python ≥ 3.7 (Windows only)            |

**Additional notes:**
- The editor itself requires **Python 3.7 or newer**. Python 3.14 is supported (ttkthemes and customtkinter removed for compatibility)
- `pywinstyles` works only on **Windows**. On other operating systems, the title bar color will not change.
- Pillow 10.0.0 requires Python ≥ 3.8; if you have Python 3.7, the installer will automatically pick an older compatible version.
- ttkbootstrap 1.10.1 works on Python 3.7–3.12, but also runs on 3.13/3.14 without issues.

These libraries are only needed for enhanced features; the editor remains functional
even if some are missing (e.g., without Pillow, face images will not be shown).

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
FILE CHANGES (If you are updating from an older version)
--------------------------------------------------------------------------------

Replace the following files in your `tsc_editor` folder:

   • editor_app.py          – Main application logic (unsaved changes, themes, load modes)
   • encryption.py          – Cipher calculation fix (modulo 0x100)
   • languages.py           – Added `unsaved_title` and `unsaved_message` keys for all languages
   • ui_components.py       – Theming for menubar, context menu, and sidebar colors
   • highlighted_tsc.py     – Blue/purple highlighting for the current file
   • dialogs.py             – Manual encoding/cipher selector (already updated, no change needed)

Also ensure you have the new `highlighted_tsc.py` (provided in this patch).  

No other files need to be changed. Your existing `settings.json`, `custom_commands.json` and 
`command_colors.json` will be automatically migrated.

--------------------------------------------------------------------------------
INSTALLATION
--------------------------------------------------------------------------------

1. Download the patch ZIP.
2. Extract the contents.
3. Copy all `.py` files into your `tsc_editor` folder (overwrite when prompted).
4. Run `main.py` as usual.

If you are using Python 3.14+, the automatic dependency installer will handle `ttkbootstrap`, 
`pillow` and `pywinstyles`.

--------------------------------------------------------------------------------
KNOWN ISSUES / NOTES
--------------------------------------------------------------------------------

• Face sprites require the `faces/free/` folder with PNG files named 
  `fac_sprite_free00.png`, `fac_sprite_free01.png`, … up to `fac_sprite_free30.png`.
• The hex dump view only shows the first 816 bytes (to avoid performance issues).
• For Japanese TSC files, always choose **Shift-JIS** or **CP932** encoding in the load dialog.
• The cipher value is rarely needed; “Auto-detect” works for 99% of original Cave Story TSC files.

--------------------------------------------------------------------------------
CREDITS & CONTACT
--------------------------------------------------------------------------------

TSC Editor+ is created for the Cave Story modding community.
Special thanks to IdioticBaka1824, LAIB who reported bugs and suggested improvements.

If you encounter any issue, please open a ticket on the project repository or the Cave Story Forum Thread.

Enjoy modding!

-- EdwarlyGamer999+
================================================================================