import tkinter.font as font
import pygame
import time
from tkinter import *
import tkinter.ttk as ttk
from commands import Commands
from PIL import ImageTk, Image
 

root = Tk()
root.minsize(550, 300)
root.geometry('500x350')
root.title('Python MP3 Music Player')

root.rowconfigure(0,weight=1)
for index in range(0,6):
    root.columnconfigure(index,weight=1)
    

pygame.display.init()

commands = Commands(root)

defined_font = font.Font(family='Helvetica')

#Define Player Control Button Images
def ResizeButtons(file):
    img = Image.open(file)
    resized = img.resize((50,50), Image.Resampling.LANCZOS)
    return resized

previous_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Back.png'))
play_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Play.png'))
pause_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Pause.png'))
stop_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Stop.png'))
next_img = ImageTk.PhotoImage(ResizeButtons('Imgs\\Next.png'))
random_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Random.png'))

volume_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Volume.png'))
muted_img = ImageTk.PhotoImage(ResizeButtons('Imgs\Muted.png'))

#menu 
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add songs', menu=add_song_menu)
add_song_menu.add_command(label='Add songs', command=commands.AddSongs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Delete song', menu=remove_song_menu)
remove_song_menu.add_command(label='Delete song', command=commands.DeleteSong)

#previous button
previous_button=Button(root, text='Previous', image=previous_img, borderwidth=0, padx=10, command=commands.Previous)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=0, sticky='nsew')

#play Button
play_button = Button(root, text='Play',image=play_img, borderwidth=0, padx=10, command=commands.Play)
play_button['font'] = defined_font
play_button.grid(row=1, column=1, sticky='nsew')

#pause button 
pause_button=Button(root, text='Pause', image=pause_img, borderwidth=0, padx=10, command=commands.Pause)
pause_button['font'] = defined_font
pause_button.grid(row=1, column=2, sticky='nsew')

#stop button
stop_button=Button(root, text='Stop', image=stop_img, borderwidth=0, padx=10, command=commands.Stop)
stop_button['font'] = defined_font
stop_button.grid(row=1, column=3, sticky='nsew')

#nextbutton
next_button=Button(root, text='Next', image=next_img, borderwidth=0, padx=10, command=commands.Next)
next_button['font'] = defined_font
next_button.grid(row=1, column=4, sticky='nsew')

def RandomButton():
    commands.Random()
    if commands.random: rand_button.configure(bg = "black")
    else: rand_button.configure(bg = "white")

#randombutton
rand_button=Button(root, text='Random', image=random_img, borderwidth=0, padx=10, command=RandomButton)
rand_button['font'] = defined_font
rand_button.grid(row=1, column=5, sticky='nsew')

def UpdateSlider():
    current_pos = commands.GetPos()/1000
    song_length = commands.GetLength()
    if song_length > 0: slider_pos.config(value=current_pos*100/song_length)
    slider_pos.after(1000, UpdateSlider)

#slider_pos
slider_pos = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=commands.SlidePos)
slider_pos.grid(row=2, columnspan=3,padx=50, sticky='nsew')


status_bar = Label(root, text='',bd=1, relief=GROOVE)
status_bar.grid(row=2, column=3, sticky='nsew')


#volumebutton
volume = 100
muted = False
def Mute():
    global muted
    global volume
    muted = not muted
    if muted:
        volume = volume_slider.get()
        volume_slider.set(0)
        volume_button.configure(image=muted_img)
    else:
        volume_slider.set(volume)
        volume_button.configure(image=volume_img)

def SetVolume(vol):
    global muted
    if vol == '0':
        if not muted: Mute()
        commands.SetVolume(vol)
    elif muted:
        Mute()
    else:
        commands.SetVolume(vol)

volume_button=Button(root, text='Volume', image=volume_img, borderwidth=0, padx=10, command=Mute)
volume_button['font'] = defined_font
volume_button.grid(row=2, column=4, sticky='nsew')

#slidervolume
volume_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=SetVolume)
volume_slider.grid(row=2, column=5,padx=50, sticky='nsew')
volume_slider.set(100)



slider_pos.after(1000, UpdateSlider)
#MainLoop
while True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            commands.PlayNext()
    
    current_pos = commands.GetPos()/1000
    song_length = commands.GetLength()

    current_time = time.strftime('%M:%S',time.gmtime(current_pos))
    song_time = time.strftime('%M:%S',time.gmtime(song_length))
    status_bar.config(text=f'{current_time} / {song_time}')
    
    root.update_idletasks()
    root.update()