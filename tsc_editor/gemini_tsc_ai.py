# -*- coding: utf-8 -*-
"""
Módulo para el asistente Gemini AI especializado en TSC.
Requiere Python 3.9+ y la librería google-genai.
"""

import sys

if sys.version_info < (3, 9):
    raise ImportError("GeminiTSCAI requiere Python 3.9 o superior. Tu versión: {}.{}".format(
        sys.version_info.major, sys.version_info.minor))

import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Nuevo SDK de Google GenAI
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

from .encryption import get_cipher_from_tsc, decrypt_tsc


class GeminiTSCAI:
    def __init__(self, parent, editor, settings):
        self.parent = parent
        self.editor = editor
        self.settings = settings
        self.ai_chat_area = None
        self.ai_input = None
        self.ai_system_prompt = self._get_ai_system_prompt()
        self._create_widgets()

    def _get_ai_system_prompt(self):
        return (
            "Eres un asistente experto en el lenguaje de script TSC (Text Script Command) "
            "del juego Cave Story (Doukutsu Monogatari). Conoces todos los comandos, su sintaxis, "
            "parámetros y efectos. Puedes ayudar a escribir, corregir, traducir o explicar scripts TSC. "
            "Responde siempre en el mismo idioma que el usuario. Sé conciso pero útil.\n\n"
            "Ejemplos de comandos: <MSG>, <NOD>, <CLR>, <FACxxxx>, <CMUxxxx>, <SOUxxxx>, <TRAxxxx>, "
            "<AM+xxxx>, <AM-xxxx>, <GITxxxx>, <IT+xxxx>, etc. También conoces los IDs de mapas, caras, músicas y sonidos."
        )

    def _create_widgets(self):
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Gemini Icon.png")
        if os.path.isfile(logo_path) and PIL_AVAILABLE:
            try:
                img = Image.open(logo_path)
                img = img.resize((48, 48), Image.Resampling.LANCZOS)
                self.ai_logo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(main_frame, image=self.ai_logo)
                logo_label.pack(pady=5)
            except:
                pass

        tk.Label(main_frame, text="Gemini AI Assistant (TSC Expert)", font=("Segoe UI", 12, "bold")).pack(pady=5)

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Cargar archivo TSC/TXT", command=self.load_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Limpiar historial", command=self.clear_history).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Explicar selección", command=self.explain_selection).pack(side=tk.LEFT, padx=2)

        # Mensajes rápidos
        quick_frame = tk.Frame(main_frame)
        quick_frame.pack(fill=tk.X, pady=2)
        tk.Button(quick_frame, text="Traducir diálogos a...", command=lambda: self.set_quick_message(
            "Traduce este TSC al español, inglés, japonés. No toques el código, solo los diálogos.")).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="Ayuda con mi mod", command=lambda: self.set_quick_message(
            "Ayúdame con mi mod de Cave Story. Tengo dudas sobre:")).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="Resolver problema", command=lambda: self.set_quick_message(
            "Resuelve este problema en mi script TSC:")).pack(side=tk.LEFT, padx=2)

        # Área de chat
        self.ai_chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20, font=("Segoe UI", 10))
        self.ai_chat_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.ai_chat_area.config(state=tk.DISABLED)
        self.ai_chat_area.tag_configure("bold", font=("Segoe UI", 10, "bold"))

        # Entrada
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        self.ai_input = tk.Entry(input_frame, font=("Segoe UI", 10))
        self.ai_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.ai_input.bind("<Return>", lambda e: self.send_query())
        tk.Button(input_frame, text="Enviar", command=self.send_query).pack(side=tk.RIGHT)

        self.add_message("Asistente", "¡Hola! Soy tu asistente experto en TSC de Cave Story. Pregúntame cualquier duda sobre comandos, sintaxis o traducciones. Puedes cargar un archivo .tsc o .txt para analizar.")

    def add_message(self, sender, text):
        self.ai_chat_area.config(state=tk.NORMAL)
        self.ai_chat_area.insert(tk.END, f"{sender}: ", "bold")
        self.ai_chat_area.insert(tk.END, f"{text}\n\n")
        self.ai_chat_area.config(state=tk.DISABLED)
        self.ai_chat_area.see(tk.END)

    def clear_history(self):
        self.ai_chat_area.config(state=tk.NORMAL)
        self.ai_chat_area.delete(1.0, tk.END)
        self.ai_chat_area.config(state=tk.DISABLED)
        self.add_message("Asistente", "Historial limpiado. ¿En qué puedo ayudarte?")

    def set_quick_message(self, msg):
        self.ai_input.delete(0, tk.END)
        self.ai_input.insert(0, msg)
        self.ai_input.focus()

    def send_query(self):
        user_text = self.ai_input.get().strip()
        if not user_text:
            return
        self.add_message("Tú", user_text)
        self.ai_input.delete(0, tk.END)
        self.add_message("Asistente", "Pensando...")
        self.ai_chat_area.see(tk.END)
        self.editor.root.update()
        threading.Thread(target=self._call_gemini, args=(user_text,), daemon=True).start()

    def _call_gemini(self, user_text):
        try:
            if not GENAI_AVAILABLE:
                self._show_error("La librería 'google-genai' no está instalada. Ejecuta: pip install google-genai")
                return
            api_key = self.settings.get("gemini_api_key", "")
            if not api_key:
                self._show_error("No se ha configurado la API key de Gemini. Ve a Configuración.")
                return
            # Nuevo cliente
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash',  # o 'gemini-1.5-flash'
                contents=user_text,
                config=types.GenerateContentConfig(
                    system_instruction=self.ai_system_prompt
                )
            )
            reply = response.text
            self.editor.root.after(0, lambda: self._replace_last_assistant_message(reply))
        except Exception as e:
            self.editor.root.after(0, lambda: self._replace_last_assistant_message(f"Error: {str(e)}"))

    def _replace_last_assistant_message(self, new_text):
        self.ai_chat_area.config(state=tk.NORMAL)
        end_index = self.ai_chat_area.index("end-1c")
        last_start = self.ai_chat_area.search("Asistente:", "1.0", end_index, backwards=True)
        if last_start:
            self.ai_chat_area.delete(last_start, "end-1c")
        self.ai_chat_area.insert(tk.END, f"Asistente: {new_text}\n\n")
        self.ai_chat_area.config(state=tk.DISABLED)
        self.ai_chat_area.see(tk.END)

    def _show_error(self, msg):
        self.editor.root.after(0, lambda: self.add_message("Sistema", f"⚠️ {msg}"))

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Cargar archivo TSC o TXT",
            filetypes=[("TSC Files", "*.tsc"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
        self.add_message("Sistema", f"Cargando archivo: {os.path.basename(file_path)}...")
        threading.Thread(target=self._process_file, args=(file_path,), daemon=True).start()

    def _process_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
        except Exception as e:
            self._show_error(f"No se pudo leer el archivo: {str(e)}")
            return

        is_tsc = file_path.lower().endswith('.tsc')
        text_content = None
        used_encoding = "utf-8"

        if is_tsc:
            cipher = get_cipher_from_tsc(raw_data)
            if cipher != 0:
                self._show_error("El archivo TSC está encriptado. Desencripta el texto en el editor principal y cópialo aquí manualmente.")
                return
            else:
                # Detectar encoding (similar al editor)
                for enc in ('shift_jis', 'utf-8', 'latin-1'):
                    try:
                        text = raw_data.decode(enc)
                        if '�' not in text:
                            text_content = text
                            used_encoding = enc
                            break
                    except:
                        continue
                if text_content is None:
                    text_content = raw_data.decode('latin-1', errors='replace')
                    used_encoding = 'latin-1'
        else:
            for enc in ('utf-8', 'latin-1'):
                try:
                    text_content = raw_data.decode(enc)
                    used_encoding = enc
                    break
                except:
                    continue
            if text_content is None:
                text_content = raw_data.decode('utf-8', errors='replace')
                used_encoding = 'utf-8'

        if not text_content:
            self._show_error("No se pudo extraer texto del archivo.")
            return

        if len(text_content) > 20000:
            text_content = text_content[:20000] + "\n...[truncado]..."
        prompt = f"Analiza el siguiente contenido de un archivo TSC (codificación {used_encoding}) y explica brevemente qué hace, señala posibles errores o sugiere mejoras:\n\n```\n{text_content}\n```"
        self.editor.root.after(0, lambda: self._send_text_to_ai(prompt))

    def _send_text_to_ai(self, prompt):
        self.add_message("Sistema", "Enviando archivo a Gemini para análisis...")
        self.ai_input.delete(0, tk.END)
        self.ai_input.insert(0, prompt)
        self.send_query()

    def explain_selection(self):
        if not self.editor.text_area:
            self._show_error("No hay editor activo.")
            return
        try:
            selected = self.editor.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self._show_error("No hay texto seleccionado en el editor.")
            return
        if not selected.strip():
            self._show_error("La selección está vacía.")
            return
        prompt = f"Explica brevemente qué hace este fragmento de código TSC:\n```\n{selected}\n```"
        self._send_text_to_ai(prompt)