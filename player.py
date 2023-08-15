import tkinter as tk
from tkinter import ttk
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
            "CodeClauseInternship_MusicPlayer/ncs_music/Tokyo Cafe.mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/ALVYN & JSTN DMND - SKY BRI [NCS Release].mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Andrew A - Fall Too Deep (feat. Barmuda) [NCS Release].mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Clarx & Zaug - No Money [NCS Release].mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Idle Days - Over It [NCS Release].mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Keep Me Closer - Low Mileage [NCS Release].mp3",
            "CodeClauseInternship_MusicPlayer/ncs_music/Speedboys - techno on my mind [NCS Release].mp3",
        ]

        self.song_coverArt = [
            "CodeClauseInternship_MusicPlayer/song_coverart/happy_minds.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/motivational_electronic_music.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/onelasttime.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/peaceful-cinematic.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/summer-time.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/tokyo-cafe.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/sky-bri-1691107245-KUkZF7wsv5.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/fall-to-deep.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/no-moneu.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/over-it-1691539246-eJfK4kk2cC.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/keep-me-closer-1689638445-k0HC0Cujj8.png",
            "CodeClauseInternship_MusicPlayer/song_coverart/artwork-440x440.png"
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
        self.cover_art_label.grid(row=0, column=4, columnspan=3, padx=60, pady=10)
        
        #Buttons and Icons
        self.play_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\play_arrow.png").subsample(2,2)
        self.pause_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\pause.png").subsample(2,2)
        self.next_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\skip_next.png").subsample(2,2)
        self.prev_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer\icons\skip_prev.png").subsample(2,2)
        self.volume_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer/icons/volumne_up.png").subsample(2,2)
        self.no_volume_icon = tk.PhotoImage(file="CodeClauseInternship_MusicPlayer/icons/no_volumne.png").subsample(2,2)

        self.prev_button = tk.Button(self.root, image=self.prev_icon, command=self.prev_song)
        self.prev_button.grid(row=1, column=0, padx=5, pady=10)
        
        self.play_pause_button = tk.Button(self.root, image=self.play_icon, command=self.toggle_play_pause_song)
        self.play_pause_button.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = tk.Button(self.root, image=self.next_icon, command=self.next_song)
        self.next_button.grid(row=1, column=2, padx=5, pady=10)


        self.volume_button = tk.Button(self.root, image=self.volume_icon)
        self.volume_button.grid(row=2, column=0, padx=5, pady=10)

        #volumne adjuster slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.grid(row=2, column=1, columnspan=3, padx=5, pady=10)

         # Create a label to display playback time
        self.playback_time_label = tk.Label(self.root, text="00:00", font=("Helvetica", 12))
        self.playback_time_label.grid(row=1, column=6, columnspan=2, padx=10, pady=5)

        #progressbar of the playback song
        self.progress_bar = ttk.Progressbar(self.root, mode="determinate", length=200)
        self.progress_bar.grid(row=1, column=4, columnspan=2, padx=20, pady=5)

        #initialize pygame
        pygame.init()
        pygame.mixer.init()

        self.music = pygame.mixer.music
        
        # Update playback time label
        self.update_playback_time()

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

    def toggle_play_pause_song(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_pause_button.config(image=self.pause_icon)
            if not self.audio_thread.is_alive():
                self.audio_thread.start()
        else:
            self.music.pause()
            self.play_pause_button.config(image=self.play_icon)
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
        cover_art_image = cover_art_image.resize((200, 150))  # Resize the image
        self.cover_art_image_resized = ImageTk.PhotoImage(cover_art_image)  # Convert to PhotoImage
        self.cover_art_label.config(image=self.cover_art_image_resized)

    def set_volume(self, volume):
        self.music.set_volume(int(volume)/100)


    def update_playback_time(self):
        playback_position = self.music.get_pos() // 1000  # Convert milliseconds to seconds
        minutes = playback_position // 60
        seconds = playback_position % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.playback_time_label.config(text=time_string)

         # Update progress bar
        total_duration = pygame.mixer.Sound(self.playlist[self.current_song_index]).get_length()
        progress_value = (playback_position / total_duration) * 100
        self.progress_bar["value"] = progress_value


        self.root.after(1000, self.update_playback_time)  # Update every second

root = tk.Tk()
music_player = MusicPlayer(root)
root.mainloop()
