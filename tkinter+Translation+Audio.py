import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound

# Language codes dictionary
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

# Translator object
translator = Translator()

# Main window
root = tk.Tk()
root.title("• Live Translator with Voice")
root.geometry("500x400")
root.configure(bg="#f0f4f8")

# Fonts
label_font = ("Segoe UI", 12)
entry_font = ("Segoe UI", 11)

# Input label
tk.Label(root, text="Enter Text:", font=label_font, bg="#f0f4f8").pack(pady=5)

# Text entry
text_entry = tk.Text(root, height=5, font=entry_font)
text_entry.pack(padx=10, fill="x")

# Language selectors
frame = tk.Frame(root, bg="#f0f4f8")
frame.pack(pady=10)

tk.Label(frame, text="From:", font=label_font, bg="#f0f4f8").grid(row=0, column=0, padx=10)
src_lang = ttk.Combobox(frame, values=list(languages.keys()), state="readonly")
src_lang.set("English")
src_lang.grid(row=0, column=1)

tk.Label(frame, text="To:", font=label_font, bg="#f0f4f8").grid(row=0, column=2, padx=10)
dest_lang = ttk.Combobox(frame, values=list(languages.keys()), state="readonly")
dest_lang.set("Hindi")
dest_lang.grid(row=0, column=3)

# Output label
output_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"), bg="#f0f4f8",
                        wraplength=450, fg="darkblue")
output_label.pack(pady=15)

# Function to translate and speak
def translate_and_speak():
    input_text = text_entry.get("1.0", tk.END).strip()
    if not input_text:
        output_label.config(text="Please enter some text.")
        return

    src = languages[src_lang.get()]
    dest = languages[dest_lang.get()]

    try:
        translated = translator.translate(input_text, src=src, dest=dest)
        output_label.config(text=translated.text)

        # Save and play audio
        tts = gTTS(text=translated.text, lang=dest)
        tts.save("output.mp3")
        playsound("output.mp3")
        os.remove("output.mp3")  # Clean up after playing
    except Exception as e:
        output_label.config(text="Error: " + str(e))

# Button
translate_button = tk.Button(root, text="Translate & Speak", command=translate_and_speak,
                             font=("Segoe UI", 12), bg="#4caf50", fg="white",
                             padx=10, pady=5)
translate_button.pack(pady=10)

root.mainloop()
