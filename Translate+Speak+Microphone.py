import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound

# Language code dictionary
languages = {
    "English": "en",
    "Hindi": "hi",
    "Punjabi": "pa",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Tamil": "ta",
    "Bengali": "bn"
}

translator = Translator()
recognizer = sr.Recognizer()

# GUI Setup
root = tk.Tk()
root.title("Voice Translator with Microphone")
root.geometry("520x450")
root.configure(bg="#eef2f3")

# Fonts
label_font = ("Segoe UI", 12)
entry_font = ("Segoe UI", 11)

# Text Entry
tk.Label(root, text="Enter or Speak Text:", font=label_font, bg="#eef2f3").pack(pady=5)
text_entry = tk.Text(root, height=4, font=entry_font)
text_entry.pack(padx=10, fill="x")

# Dropdowns for language selection
frame = tk.Frame(root, bg="#eef2f3")
frame.pack(pady=10)

tk.Label(frame, text="From:", font=label_font, bg="#eef2f3").grid(row=0, column=0, padx=10)
src_lang = ttk.Combobox(frame, values=list(languages.keys()), state="readonly")
src_lang.set("English")
src_lang.grid(row=0, column=1)

tk.Label(frame, text="To:", font=label_font, bg="#eef2f3").grid(row=0, column=2, padx=10)
dest_lang = ttk.Combobox(frame, values=list(languages.keys()), state="readonly")
dest_lang.set("Hindi")
dest_lang.grid(row=0, column=3)

# Output label
output_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"), bg="#eef2f3", fg="darkblue", wraplength=480)
output_label.pack(pady=10)

# Translate and Speak Function
def translate_and_speak():
    input_text = text_entry.get("1.0", tk.END).strip()
    if not input_text:
        output_label.config(text="Please enter or record some text.")
        return

    src = languages[src_lang.get()]
    dest = languages[dest_lang.get()]

    try:
        translated = translator.translate(input_text, src=src, dest=dest)
        output_label.config(text=translated.text)

        # Save & play audio
        tts = gTTS(text=translated.text, lang=dest)
        tts.save("speak.mp3")
        playsound("speak.mp3")
    except Exception as e:
        output_label.config(text="Translation error: " + str(e))

# Microphone Function
def mic_input():
    with sr.Microphone() as source:
        output_label.config(text="[ Listening... ]")
        root.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, text)
            output_label.config(text="Recognized: " + text)
        except sr.UnknownValueError:
            output_label.config(text="Could not understand audio.")
        except sr.RequestError:
            output_label.config(text="Speech service unavailable.")
        except Exception as e:
            output_label.config(text="Mic error: " + str(e))

# Buttons
btn_frame = tk.Frame(root, bg="#eef2f3")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="🎤 Speak", command=mic_input, font=("Segoe UI", 11), bg="#2196f3", fg="white",
          padx=15, pady=5).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🌍 Translate & Speak", command=translate_and_speak,
          font=("Segoe UI", 11), bg="#4caf50", fg="white",
          padx=15, pady=5).grid(row=0, column=1, padx=10)

root.mainloop()
