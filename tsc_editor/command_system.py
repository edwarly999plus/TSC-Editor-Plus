# -*- coding: utf-8 -*-
"""
Management of TSC commands: base commands, custom commands, colors.
"""

import json
import re
import os
import sys

def load_base_commands() -> dict:
    """Return the built-in TSC commands database."""
    return {
        "AE+":  ["0", "----", "Refill all weapon ammo."],
        "AM+":  ["2", "aA--", "Give weapon W with X ammo. Use 0000 for infinite ammo."],
        "AM-":  ["1", "a--", "Remove weapon W."],
        "AMJ":  ["2", "ae--", "Jump to event X if the PC has weapon W."],
        "ANP":  ["3", "N#d-", "Animate entity W to scriptstate X and direction Y."],
        "BOA":  ["1", "#---", "Give map-boss scriptstate W"],
        "BSL":  ["1", "N---", "Start boss fight with entity W. Use 0000 to end the boss fight."],
        "CAT":  ["0", "----", "Instantly display text until <END."],
        "CIL":  ["0", "----", "Clear illustration (during credits)."],
        "CLO":  ["0", "----", "Close message box."],
        "CLR":  ["0", "----", "Clear message box."],
        "CMP":  ["3", "xyt-", "Change tile at coordinates W:X to type Y (with smoke)."],
        "CMU":  ["1", "u---", "Change music to song W."],
        "CNP":  ["3", "Nnd-", "Change all entities W to type X, direction Y."],
        "CPS":  ["0", "----", "Stop propeller sound."],
        "CRE":  ["0", "----", "Roll credits."],
        "CSS":  ["0", "----", "Stop stream sound."],
        "DNA":  ["1", "n---", "Remove all entities of type W."],
        "DNP":  ["1", "N---", "Remove all entities W."],
        "ECJ":  ["2", "#e--", "Jump to event X if any entities W exist."],
        "END":  ["0", "----", "End current scripted event."],
        "EQ+":  ["1", "E---", "Equip item W (Booster, Map System, etc)."],
        "EQ-":  ["1", "E---", "Dequip item W."],
        "ESC":  ["0",  "----", "Quit to title screen."],
        "EVE":  ["1",  "e---", "Go to event W."],
        "FAC":  ["1",  "f---", "Show face W in message box."],
        "FAI":  ["1",  "d---", "Fade in with direction W."],
        "FAO":  ["1", "d---", "Fade out with direction W."],
        "FL+":  ["1", "F---", "Set flag W."],
        "FL-":  ["1", "F---", "Clear flag W."],
        "FLJ":  ["2", "##--", "Jump to event X if flag W is set."],
        "FLA":  ["0", "----", "Flash screen white."],
        "FMU":  ["0", "----", "Fade music out."],
        "FOB":  ["2", "N.--", "Focus on boss W in X ticks."],
        "FOM":  ["1", ".---", "Focus on PC in W ticks."],
        "FON":  ["2", "N.--", "Focus on entity W in X ticks."],
        "FRE":  ["0", "----", "Free game action and PC."],
        "GIT":  ["1", "g---", "Display item/weapon icon (add 1000 for items)."],
        "HMC":  ["0", "----", "Hide PC."],
        "INI":  ["0", "----", "Reset memory and restart game."],
        "INP":  ["3", "Nnd-", "Change entity W to type X, direction Y, set flag 0x8000."],
        "IT+":  ["1", "i---", "Give item W."],
        "IT-":  ["1", "i---", "Remove item W."],
        "ITJ":  ["2", "ie--", "Jump to event X if PC has item W."],
        "KEY":  ["0", "----", "Lock player controls and hide status bars until <END."],
        "LDP":  ["0", "----", "Load saved game."],
        "LI+":  ["1", "#---", "Recover W health."],
        "ML+":  ["1", "#---", "Increase max health by W."],
        "MLP":  ["0", "----", "Display map of current area."],
        "MM0":  ["0", "----", "Halt PC's forward motion."],
        "MNA":  ["0", "----", "Display map name."],
        "MNP":  ["4", "Nxyd", "Move entity W to coordinates X:Y, direction Z."],
        "MOV":  ["2", "xy--", "Move PC to coordinates W:X."],
        "MP+":  ["1", "#---", "Set map flag W (0-127)."],
        "MPJ":  ["1", "e---", "Jump to event W if current map flag set."],
        "MS2":  ["0", "----", "Open invisible message box at top."],
        "MS3":  ["0", "----", "Open message box at top."],
        "MSG":  ["0", "----", "Open message box at bottom."],
        "MYB":  ["1", "d---", "Bump PC in opposite direction."],
        "MYD":  ["1", "d---", "Set PC direction."],
        "NCJ":  ["2", "ne--", "Jump to event X if any entity type W exists."],
        "NOD":  ["0", "----", "Wait for player input."],
        "NUM":  ["1", "#---", "Print numeric value."],
        "PRI":  ["0", "----", "Lock controls and freeze game action."],
        "PS+":  ["2", "#m--", "Set teleporter slot W to event X."],
        "QUA":  ["1", ".---", "Shake screen for W ticks."],
        "RMU":  ["0", "----", "Resume previous music."],
        "SAT":  ["0", "----", "Instantly display text until <END."],
        "SIL":  ["1", "l---", "Show illustration W (credits)."],
        "SK+":  ["1", "F---", "Set skipflag W."],
        "SK-":  ["1", "F---", "Clear skipflag W."],
        "SKJ":  ["2", "Fe--", "Jump to event X if skipflag W set."],
        "SLP":  ["0", "----", "Show teleporter menu."],
        "SMC":  ["0", "----", "Unhide PC."],
        "SMP":  ["2", "xy--", "Subtract 1 from tile type at W:X (no smoke)."],
        "SNP":  ["4", "nxyd", "Create entity type W at X:Y, direction Z."],
        "SOU":  ["1", "s---", "Play sound effect W."],
        "SPS":  ["0", "----", "Start propeller sound."],
        "SSS":  ["1", "#---", "Start stream sound with volume W."],
        "STC":  ["0", "----", "Save current time to 290.rec."],
        "SVP":  ["0", "----", "Save current game."],
        "TAM":  ["3", "aaA-", "Trade weapon W for X, set max ammo Y."],
        "TRA":  ["4", "mexy", "Travel to map W, run event X, move to Y:Z."],
        "TUR":  ["0", "----", "Instantly display text until next <MSG/END."],
        "UNI":  ["1", "#---", "Set movement type (0000 normal, 0001 zero-G)."],
        "UNJ":  ["2", "#e--", "Jump if movement type W."],
        "WAI":  ["1", ".---", "Pause script for W ticks."],
        "WAS":  ["0", "----", "Wait until PC on ground."],
        "XX1":  ["1", "l---", "Show the island falling in manner W. Use 0000 to crash, 0001 to stop midway."],
        "XX2":  ["1", "#---", "Set TimgFILE.png over the screen. The 'tag' for the file name must be exactly 4 characters."],
        "YNJ":  ["1", "e---", "Yes/No prompt; jump to event W if No."],
        "ZAM":  ["0", "----", "Reset all weapon energy to zero."],
        "LRX":  ["3", "eee-", "Jump to W,X,Y if Left/Right/Shoot."],
        "FNJ":  ["2", "Fe--", "Jump if flag X not set."],
        "VAR":  ["2", "##--", "Store XXXX into variable WWWW."],
        "VAZ":  ["2", "##--", "Zero XXXX variables starting at WWWW."],
        "VAO":  ["2", "##--", "Perform operation on variable."],
        "VAJ":  ["4", "###e", "Compare variables and jump."],
        "RND":  ["3", "###-", "Random number into variable."],
        "PHY":  ["2", "##--", "Change physics variables."],
        "I+N":  ["2", "##--", "Adds 1 of item xxxx, with a max quantity of yyyy."],
        "2MV":  ["1", "#---", "Moves the other player."],
        "2PJ":  ["1", "#---", "Jump to event xxxx if P2 is active."],
        "HM2":  ["0", "----", "Hides only the player that triggered this event."],
        "FF-":  ["2", "##--", "Unsets the first set flag in the range."],
        "KE2":  ["0", "----", "Used in the inventory."],
        "FR2":  ["0", "----", "Sets game flags."],
        "INJ":  ["3", "###-", "Jump if player has at least yyyy quantity of item xxxx."],
        "POP":  ["0", "----", "Event stack pop."],
        "PSH":  ["1", "#---", "Event stack push."],
        "ACH":  ["1", "#---", "Get achievement xxxx."],
    }

def load_custom_commands(filepath: str) -> dict:
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_custom_commands(filepath: str, commands: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=2)

def update_commands_data(base: dict, custom: dict) -> dict:
    data = base.copy()
    data.update(custom)
    return data

def build_command_regex(commands_data: dict) -> re.Pattern:
    if not commands_data:
        return re.compile(r'<[A-Z0-9+\-]+')
    cmds = sorted(commands_data.keys(), key=len, reverse=True)
    escaped_cmds = (re.escape(cmd) for cmd in cmds)
    pattern = r'<(' + '|'.join(escaped_cmds) + r')'
    return re.compile(pattern)

def load_command_colors(filepath: str) -> dict:
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_command_colors(filepath: str, colors: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(colors, f, indent=2)

def get_command_color(colors: dict, cmd_name: str) -> str:
    return colors.get(cmd_name)
