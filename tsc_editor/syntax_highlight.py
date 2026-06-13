# -*- coding: utf-8 -*-
"""
Syntax checking and highlighting for TSC scripts.
"""

import re

def check_syntax(text: str, commands_data: dict, command_pattern: re.Pattern) -> list:
    errors = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '#':
            if i+5 <= n and text[i+1:i+5].isdigit():
                i += 5
            else:
                errors.append({
                    'offset': i,
                    'length': min(5, n-i),
                    'message': f"Invalid event number at position {i}: expected 4 digits after '#'."
                })
                i += 1
        elif ch == '<':
            match = command_pattern.match(text, i)
            if match:
                cmd_name = match.group(1)
                if cmd_name in commands_data:
                    num_args = int(commands_data[cmd_name][0])
                    pos = match.end()
                    arg_idx = 0
                    while arg_idx < num_args and pos < n:
                        if text[pos] == ':':
                            pos += 1
                        if pos+4 <= n and text[pos:pos+4].isdigit():
                            pos += 4
                            arg_idx += 1
                        else:
                            errors.append({
                                'offset': pos,
                                'length': min(4, n-pos),
                                'message': f"Missing or invalid parameter {arg_idx+1} for command <{cmd_name}>."
                            })
                            break
                    i = pos
                else:
                    errors.append({
                        'offset': i,
                        'length': match.end() - i,
                        'message': f"Unknown command '<{cmd_name}>' at position {i}."
                    })
                    i = match.end()
            else:
                i += 1
        else:
            i += 1
    return errors

def highlight_syntax(text_widget, commands_data: dict, command_pattern: re.Pattern, command_colors: dict):
    for tag in ("evento", "comando_letras", "comando_digitos", "comando_id", "error",
                "special_warning", "comando_personal_rosa", "comando_personal_rojo"):
        text_widget.tag_remove(tag, "1.0", "end")

    texto = text_widget.get("1.0", "end")
    if not texto:
        return

    for match in re.finditer(r'#[0-9A-Fa-f]{4}\b', texto):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_widget.tag_add("evento", start, end)

    for match in command_pattern.finditer(texto):
        cmd_name = match.group(1)
        start_cmd = match.start()
        end_cmd = match.end()
        start_cmd_pos = f"1.0 + {start_cmd} chars"
        end_cmd_pos = f"1.0 + {end_cmd} chars"

        custom_color = command_colors.get(cmd_name)
        if custom_color == "pink":
            text_widget.tag_add("comando_personal_rosa", start_cmd_pos, end_cmd_pos)
        elif custom_color == "red":
            text_widget.tag_add("comando_personal_rojo", start_cmd_pos, end_cmd_pos)
        else:
            text_widget.tag_add("comando_letras", start_cmd_pos, end_cmd_pos)

        pos = end_cmd
        n = len(texto)
        while pos < n and texto[pos] in '0123456789:':
            if texto[pos] == ':':
                pos += 1
            elif texto[pos].isdigit() and pos+4 <= n and texto[pos:pos+4].isdigit():
                start_arg = pos
                end_arg = pos+4
                start_arg_pos = f"1.0 + {start_arg} chars"
                end_arg_pos = f"1.0 + {end_arg} chars"
                text_widget.tag_add("comando_digitos", start_arg_pos, end_arg_pos)
                pos = end_arg
            else:
                break

    for match in re.finditer(r'\b([0-9]{4})\b', texto):
        start_match = match.start()
        start_index = f"1.0 + {start_match} chars"
        tags = text_widget.tag_names(start_index)
        if not any(t in tags for t in ("evento", "comando_letras", "comando_digitos",
                                       "comando_personal_rosa", "comando_personal_rojo")):
            start_pos = f"1.0 + {start_match} chars"
            end_pos = f"1.0 + {match.end()} chars"
            text_widget.tag_add("comando_id", start_pos, end_pos)

    for match in re.finditer(r'[áéíóúüñÁÉÍÓÚÜÑ¡¿çÄËÏÖÜäëïöü]', texto):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_widget.tag_add("special_warning", start, end)

    errors = check_syntax(texto, commands_data, command_pattern)
    for err in errors:
        start = f"1.0 + {err['offset']} chars"
        end = f"1.0 + {err['offset'] + err['length']} chars"
        tags = text_widget.tag_names(start)
        if not any(t in tags for t in ("comando_letras", "comando_digitos",
                                       "comando_personal_rosa", "comando_personal_rojo")):
            text_widget.tag_add("error", start, end)

    text_widget.tag_raise("comando_letras")
    text_widget.tag_raise("comando_personal_rosa")
    text_widget.tag_raise("comando_personal_rojo")
    text_widget.tag_raise("comando_digitos")