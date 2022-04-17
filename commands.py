from tkinter import *
from tkinter import filedialog
from pygame import mixer, USEREVENT
from random import randrange
from mutagen.mp3 import MP3

class Commands:
    def __init__(self, root):
        mixer.init()

        self.song_address_list = []
        self.songs_list = Listbox(root, selectmod=SINGLE, bg='black', fg='green', font=('arial',10), 
                                    selectbackground='gray', selectforeground='black')
        self.songs_list.grid(columnspan=9, padx=50,pady=25,sticky='nsew')


        self.music_index = 0
        self.song_length = 0
        self.current_time = 0
        self.volume = 1
        self.random = False
        self.paused = False

        mixer.music.set_endevent(USEREVENT)

    def AddSongs(self):
        temp_song = filedialog.askopenfilenames(initialdir='Music/', title='Choose a song', filetypes=(('mp3 Files', '*.mp3'),))

        for s in temp_song:
            
            txt = s.split("/")
            self.song_address_list.append(s)
            self.songs_list.insert(END,txt[len(txt) - 1])
          
    def DeleteSong(self):
        curr_song =  self.songs_list.curselection()
        for s in curr_song:
            self.song_address_list.pop(s)
            self.songs_list.delete(s)

    def Play(self):
        if len(self.song_address_list) <= 0: return
    
        if self.paused:
            self.paused = False
            song = self.song_address_list[self.music_index]
            mixer.music.load(song)
            mixer.music.set_volume(self.volume)
            mixer.music.play(loops=0, start=int(self.current_time))  
        
        else:
            selected = self.songs_list.curselection()
            if len(selected) > 0: self.music_index = self.songs_list.curselection()[0]
            else: self.music_index = 0
            
            self.songs_list.selection_clear(0,END)
            self.songs_list.activate(-1)
            self.Play_(self.music_index)
    
    def PlayNext(self):
        if self.random: self.music_index = randrange(len(self.song_address_list))
        else: self.music_index += 1

        if self.music_index >= len(self.song_address_list):
            self.music_index = 0
            self.current_time = 0
            self.Stop()
        else: self.Play_(self.music_index)
    
    def Play_(self, idx):
        index = idx
        self.songs_list.activate(index)
        song = self.song_address_list[index]

        self.song_length = MP3(song).info.length
        self.current_time = 0
        mixer.music.load(song)
        mixer.music.set_volume(self.volume)
        mixer.music.play(loops=0)  

    def Pause(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.paused = True

    def Stop(self):
        self.paused = False
        self.music_index = len(self.song_address_list)
        mixer.music.stop()
        mixer.music.unload()
        self.song_length = 0
        self.songs_list.selection_clear(ACTIVE)

    def Previous(self):
        if mixer.music.get_pos() < 1000:
            self.music_index -= 1
            if self.music_index < 0: self.music_index = 0
            
        self.paused = False
        self.Play_(self.music_index)

    def Next(self):
        self.paused = False
        self.music_index += 1
        if self.music_index >= len(self.song_address_list): 
            self.music_index = 0
            
        self.Play_(self.music_index)
    
    def Random(self):
        self.random = not self.random

    def SetVolume(self, volume):
        self.volume = float(volume)/100
        mixer.music.set_volume(self.volume)
    
    def GetPos(self):
        pos = mixer.music.get_pos()
        if pos <= 0: pos = 0
        return pos + (self.current_time*1000)
    
    def GetLength(self):
        return self.song_length

    def SlidePos(self, perc):
        
        self.current_time = float(perc)*self.song_length/100
        
        if not self.paused and self.music_index < len(self.song_address_list):
            song = self.song_address_list[self.music_index]
            mixer.music.load(song)
            mixer.music.set_volume(self.volume)
            mixer.music.play(loops=0, start=int(self.current_time))  