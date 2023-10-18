import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import speech_recognition as sr
from pydub import AudioSegment
import pygame

def recognize_speech():
    recognizer = sr.Recognizer()
    audio_file = filedialog.askopenfilename(title="Select Audio File")
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, text)
        except sr.UnknownValueError:
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, "Could not understand the audio")
        except sr.RequestError:
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, "Could not request results")

def play_song(song_file):
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()

def load_music_files(folder):
    return [file for file in os.listdir(folder) if file.endswith(".mp3")]

def recommend_song():
    dataset_folder = filedialog.askdirectory(title="Select Music Dataset Folder")
    if not dataset_folder:
        song_listbox.insert(tk.END, "Please select a valid dataset folder.")
    else:
        song_files = [f for f in os.listdir(dataset_folder) if f.endswith(".mp3")]
        if not song_files:
            song_listbox.insert(tk.END, "No .mp3 files found in the dataset folder.")
        else:
            song_listbox.delete(0, tk.END)
            for song in song_files:
                song_listbox.insert(tk.END, song)

'''def play_selected_song():
    selected_song = music_listbox.get(music_listbox.curselection())
    if selected_song_index:
        selected_song_index = int(selected_song_index[0])
        selected_song = music_files[selected_song_index]
        play_song(os.path.join(music_folder, selected_song))'''

def play_song():
    selected_song = song_listbox.get(tk.ACTIVE)
    if selected_song:
        song_path = os.path.join(dataset_folder, selected_song)
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

root = tk.Tk()
root.title("VOICE-TO-TEXT-Based Music Recommendation System")

dataset_folder = None
# Create GUI elements
browse_button = tk.Button(root, text="Browse Audio File", command=recognize_speech)
browse_button.pack()

music_folder = filedialog.askdirectory(title="Select Music Folder")
music_files = load_music_files(music_folder)

text_box = scrolledtext.ScrolledText(root, width=30, height=10)
text_box.pack()

music_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
music_folder = filedialog.askdirectory(title="Select Music Folder")
music_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".mp3")]
for music_file in music_files:
    music_listbox.insert(tk.END, music_file)
music_listbox.pack()

song_listbox = tk.Listbox(root)
for song in music_files:
    song_listbox.insert(tk.END, song)
song_listbox.pack()

'''play_button = tk.Button(root, text="Play", command=play_selected_song)
play_button.pack()

root.mainloop()'''
recommend_button = tk.Button(root, text="Recommend Songs", command=recommend_song)
recommend_button.pack()

song_listbox = tk.Listbox(root, width=50, height=10)
song_listbox.pack()

play_button = tk.Button(root, text="Play Selected Song", command=play_song)
play_button.pack()

root.mainloop()



