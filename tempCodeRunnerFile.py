import tkinter as tk
from tkinter import *
import pygame
import os
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x300")

        self.playlist = [
            "CodeClauseInternship_MusicPlayer/ncs_music/Happy Day.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Motivational Electronic Music.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/One Last Time.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Peaceful Cinematic.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Summer Party.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Tokyo Cafe.mp3"
        ]

        self.song_coverArt = [
            "CodeClauseInternship_MusicPlayer/song_coverart/happy_minds.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/motivational_electronic_music.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/onelasttime.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/peaceful-cinematic.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/summer-time.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/tokyo-cafe.png"
        ]

        

        self.current_song_index = 0

        self.is_playing = False

        #Scrollbar
        scrollbar = Scrollbar(self.root)
        scrollbar.grid(row=0, column=3, sticky=N+S)

        #listBox
        self.song_list = tk.Listbox(self.root, bg="white", fg="black", selectbackground="yellow", selectforeground="gray", yscrollcommand=scrollbar.set)
        for song_path in self.playlist:
            song_name = os.path.basename(song_path)
            self.song_list.insert("end", song_name)
        self.song_list.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Bind the function to play the selected song
        self.song_list.bind("<<ListboxSelect>>", self.play_selected_song)
        
        # Cover art label
        self.cover_art_label = tk.Label(self.root, image=None)
        self.cover_art_label.grid(row=0, column=5, padx=10, pady=10)
        
        #Buttons and Icons
        self.play_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\play_arrow.png").subsample(2,2)
        self.pause_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\pause.png").subsample(2,2)
        self.next_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\skip_next.png").subsample(2,2)
        self.prev_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\skip_prev.png").subsample(2,2)


        self.prev_button = tk.Button(self.root, image=self.prev_icon, command=self.prev_song)
        self.prev_button.grid(row=1, column=0, padx=5, pady=10)
        
        self.play_pause_button = tk.Button(self.root, image=self.play_icon, command=self.toggle_play_pause_song)
        self.play_pause_button.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = tk.Button(self.root, image=self.next_icon, command=self.next_song)
        self.next_button.grid(row=1, column=2, padx=5, pady=10)


        #initialize pygame
        pygame.init()
        pygame.mixer.init()

        self.music = pygame.mixer.music

    def toggle_play_pause_song(self):
        if not self.is_playing:
            self.music.load(self.playlist[self.current_song_index])
            self.music.play()
            self.play_pause_button.config(image=self.pause_icon)
            self.is_playing = True
            self.update_cover_art()  
        else:
            self.music.pause()
            self.play_pause_button.config(image = self.play_icon)
            self.is_playing = False

    def play_song(self):
        self.music.load(self.playlist[self.current_song_index])
        self.music.play()

    def next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        self.is_playing = True
        self.play_song()
        self.update_cover_art()  

    def prev_song(self):
        if not (self.current_song_index - 1) < 0:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.is_playing = True
            self.play_song()
            self.update_cover_art()  
        else:
            self.current_song_index = (self.current_song_index) % len(self.playlist)
            self.is_playing = True
            self.play_song()
            self.update_cover_art() 

    def play_selected_song(self, event):
        self.current_song_index = self.song_list.curselection()[0]
        self.is_playing = True
        self.play_pause_button.config(image=self.pause_icon)
        self.play_song()
        self.update_cover_art()  

    def update_cover_art(self):
        cover_art_path = self.song_coverArt[self.current_song_index]
        cover_art_image = Image.open(cover_art_path)
        cover_art_image = cover_art_image.resize((300, 150))  # Resize the image
        self.cover_art_image_resized = ImageTk.PhotoImage(cover_art_image)  # Convert to PhotoImage
        self.cover_art_label.config(image=self.cover_art_image_resized)



root = tk.Tk()
music_player = MusicPlayer(root)
root.mainloop()
