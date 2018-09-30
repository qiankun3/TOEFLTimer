# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 20:08:31 2018

@author: ray
"""
import tkinter as tk
from tkinter import font, ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
import winsound
import math
import wave
import contextlib
import subprocess
import sys
import re
import datetime
import os

# get the path of the target file
def path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# generate the file name with date and time
def filename_generator():
    time_startrecord = re.sub('[^A-Za-z0-9]+', '', str(datetime.datetime.now()))
    return time_startrecord[:14] + ".wav"

# get the duaration time of a audio file
def get_duration(filename):
    pf = filename
    with contextlib.closing(wave.open(pf,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return math.ceil(round(frames / float(rate), 3))/100
    
def display(time):
    m, s = divmod(time, 60)
    return "%02d:%02d" % (m, s)

def load_image(filename, factor = 1):
    load = Image.open(filename)
    x,y = load.size
    render = ImageTk.PhotoImage(load.resize((int(x*factor),int(y*factor)), Image.ANTIALIAS))
    return render


THEMAN = path("resources/theman.jpg")
RECORDING_0_ICON = path("resources/recording.png")
RECORDING_1_ICON = path("resources/recording1.png")
PLAYING_0_ICON = path("resources/playing.png")
PLAYING_1_ICON = path("resources/playing1.png")
PREPARE_REMAINDER = path('resources/15.wav')
SPEAKING_REMAINDER = path('resources/45.wav')
# the App Class
class TOEFLTimer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("TEOFL Speaking Timer")
        self.geometry("500x500+100+100")
        self.resizable(1, 1)
        self.menubar = tk.Menu(self)
        self.config(menu = self.menubar)
        self.optionMenu = tk.Menu(self.menubar)
        self.startMenu = tk.Menu(self.optionMenu)
        self.optionMenu.add_cascade(label = "Start",menu=self.startMenu)
        self.optionMenu.add_command(label="Exit", command=self.simple_close)
        self.menubar.add_cascade(label="Options", menu=self.optionMenu)
        
        # resources
        self._theman = load_image(THEMAN, 0.75)
        self._recording = load_image(RECORDING_0_ICON, 0.02)
        self._recording1 = load_image(RECORDING_1_ICON, 0.02)
        self._playing = load_image(PLAYING_0_ICON, 0.02)
        self._playing1 = load_image(PLAYING_1_ICON, 0.02)
        self._prepareremainder = get_duration(PREPARE_REMAINDER)
        self._speakingremainder = get_duration(SPEAKING_REMAINDER)
        
        # text
        self._welcome = "Welcome to TOEFL Timer Lite"
        self._prepare = "Begin to prepare your response after the beep!"
        self._speak = "Begin speak after the beep!"
        
        # data
        self._tuple = (15, 45)
        self._remaining, self._rectime = self._tuple
        self._barlen = self._remaining
        self._idletime = 0
        self._p = None
        self._filename = ''
        
        # indicator
        self._status = False
        self._recordingindic = True
        self._playingindic = False
        self._job = None
        self._task = 0
        self._played = 1
        self._recordstart = 1
        
        # set
        self.protocol("WM_DELETE_WINDOW", self.simple_close)
        
        # UI
        self.title("TEOFL Speaking Timer")
        self.geometry("500x500+100+100")
        self.resizable(1, 1)
        
#        s = ttk.Style()
#        s.theme_use('clam')
#        s.configure("pb.Horizontal.TProgressbar",troughcolor = 'grey94', foreground = 'grey94', background='grey94')
        self.progressbar = ttk.Progressbar(self,orient=tk.HORIZONTAL, value = 100,length=100,mode='determinate')
        self.label = tk.Label(self, text = self._welcome, width = 35, font = self.set_font("Times", 12, "bold"))
        self.canvas = tk.Label(self, image = self._theman)       
        self.status = tk.Label(self, image = self._recording1)
        self.timerlabel = tk.Label(self, text = "Question 1 & 2", width = 35, font = self.set_font("Times", 16, "bold"))
        self.button1 = tk.Button(self, text="Start", command = self.clicked0, width = 10, height = 2, font = self.set_font("Times", 10, "bold"))
        self.button2 = tk.Button(self, text="Restart", state="disabled", command = self.clicked1, width = 10, height = 2, font = self.set_font("Times", 10, "bold"))
        
        # menu
        self.menubar = tk.Menu(self)
        self.config(menu = self.menubar)
        self.optionMenu = tk.Menu(self.menubar, tearoff=False)
        self.newMenu = tk.Menu(self.optionMenu, tearoff=False)
        self.newMenu.add_command(label = "Question 1 & 2", command=lambda:self.reset((15,45)))
        self.newMenu.add_command(label = "Question 3 & 4", command=lambda:self.reset((30,60)))
        self.newMenu.add_command(label = "Question 5 & 6", command=lambda:self.reset((20,60)))
        self.optionMenu.add_cascade(label = "New",menu=self.newMenu)
        self.optionMenu.add_command(label="Exit", command=self.simple_close)
        self.helpMenu = tk.Menu(self.menubar, tearoff = False)
        self.helpMenu.add_command(label = "About", command = self.about)
        self.menubar.add_cascade(label="Options", menu=self.optionMenu)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu)
        
        self.pack()
        self.mainloop()
        
    def set_font(self, f, s, w = "normal"):
        return font.Font(family=f, size=s, weight=w)

    
    def pack(self):
        self.label.pack(padx=20, pady=20, fill = tk.BOTH, expand=1)
        self.canvas.pack(padx=10, pady=10, fill = tk.BOTH, expand=1)
        self.timerlabel.pack(fill = tk.BOTH, expand=1)
        self.progressbar.pack(anchor=tk.CENTER,  fill = tk.BOTH, padx = 50, pady = 10, expand=1)
        self.button2.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=50, pady=20, fill = tk.BOTH, expand=1)
        self.status.pack(side=tk.RIGHT,anchor=tk.CENTER, padx=50, pady=20, fill = tk.BOTH, expand=1)
        self.button1.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=50, pady=20, fill = tk.BOTH, expand=1)
        self.pack_propagate(0)
        
    def clicked0(self):
        if self.button1["text"] == "Pause":
            self.countdown(self._remaining, self._job)
            self.button1.config(text = 'Continue')
            self._job = None
        elif self.button1["text"] == "Play":
#                self.button1.config(text = 'Playing')
            self.countdown(self._remaining)
            self.button1.config(state = 'disabled')
            
        else:
            self.countdown(self._remaining, self._job)
            self.button1.config(text = 'Pause')
            self.button2.config(state = 'normal')
                
    def clicked1(self):
        if self.button2['state'] == 'normal':
            self.button2.config(state = 'disabled')
            self.button1.config(state = 'normal', text = 'Start')
            self.reset(self._tuple)
    
    def about(self):
        tk.messagebox.showinfo("About TOEFL Timer", "A Timer and Recorder for TOEFL Speaking Test")

    # in case it need close warning
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            winsound.PlaySound(None, winsound.SND_PURGE)
            
    # blinking the icon while recording or playing
    def blinking(self):
        if self._task == 1:
            if self._status:
                self.status.configure(image = self._recording1)
                self.toggle_status()
            else:
                self.status.configure(image = self._recording)
                self.toggle_status()
        if self._task == 2:
            if self._status:
                self.status.configure(image = self._playing)
                self.toggle_status()
            else:
                self.status.configure(image = self._playing1)
                self.toggle_status()
            
    def simple_close(self):
        self.destroy()
        winsound.PlaySound(None, winsound.SND_PURGE)
        
    def set_remaining(self, n):
        self._remaining = n
        
    def remaining_minusone(self):
        if self._remaining:
            self._remaining -= 1
        
    def set_barlen(self, n):
        self._barlen = n
    
    def set_played(self, b):
        self._played = b
        
    def set_idletime(self, t):
        self._idletime = t
        
    def set_task(self, n):
        self._task = n
        
    def set_rec(self, b):
        self._recordstart = b
    
    def set_tuple(self, t):
        self._tuple = t
        self._remaining, self._rectime = self._tuple
        self._barlen = self._remaining
    
    def toggle_status(self, b = True):
        if b:
            if self._status:
                self._status = False
            else:
                self._status = True
        else:
            self._status = b
    
    def hide_me(event):
        event.widget.pack_forget()

    
    def reset(self, t):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
            self.set_task(0)
        self.status.configure(image = self._recording1)
        self.set_tuple(t)
        self.label.configure(text = self._welcome)
        if self._barlen == 15:
            self.timerlabel.configure(text = "Question 1 & 2")
        elif self._barlen == 30:
            self.timerlabel.configure(text = "Question 3 & 4")
        else:
            self.timerlabel.configure(text = "Question 5 & 6")
        self.set_played(True)
        self.set_rec(True)
        self.set_idletime(0)
        self.button1.config(text = 'Start')
        winsound.PlaySound(None, winsound.SND_PURGE)
        
    def countdown(self, remaining = None, pause = False):
        if remaining is not None:
            self.set_remaining(remaining)

        if self._remaining <= 0 and self._task > 0:
            self.status.configure(image = self._playing1)
            if self._task == 1:
                self.timerlabel.configure(text="Time's up!")
                self.button1.config(text = 'Play')
                self._task = 2
                self.toggle_status(False)
                self.set_remaining(self._rectime)
                self.set_played(True)
                self._idletime += 1
            else:
                self.timerlabel.configure(text="You've completed!")

        elif pause:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self._idletime = 0
            self.timerlabel.configure(text= display(self._remaining))
            self.progressbar.configure(value = (self._remaining)*100//self._barlen)
            if self._job is not None:
                self.after_cancel(self._job)
                self._job = None
            
        else:
            if self._task == 0:
                self.label.configure(text = self._prepare)
                if self._played:
                    winsound.PlaySound(PREPARE_REMAINDER, winsound.SND_ASYNC)
                    self.set_played(False)
                    self._idletime = self._prepareremainder*100 + 1
            elif self._task == 1:
                self.label.configure(text = self._speak)
                if self._played:
                    winsound.PlaySound(SPEAKING_REMAINDER, winsound.SND_ASYNC)
                    self.set_played(False)
                    self._idletime = self._speakingremainder*100 + 1
                if self._recordstart and not self._idletime:
                    self._filename = filename_generator()
                    si = subprocess.STARTUPINFO()
                    si.dwFlags|= subprocess.STARTF_USESHOWWINDOW
                    # self._p = subprocess.Popen([sys.executable, path('resources/recorder.py'), str(self._rectime), self._filename], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,startupinfo=si)
                    self._p = subprocess.Popen([path('resources/recorder.exe'), str(self._rectime), self._filename], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,startupinfo=si)
#                    cmd = [sys.executable, '-c', "import recorder; recorder.record(45, '111.wav')"]
#                    subprocess.Popen(cmd,stdin=child1.stdout,stdout=subprocess.PIPE)
                    self.set_rec(False)
            else:
                if self._played:
                    self.label.configure(text = "Review your recording...")
                    winsound.PlaySound(self._filename, winsound.SND_ASYNC)
                    self.set_played(False)

            if not self._idletime:
                self.blinking()
                self.remaining_minusone()
            else:
                self._idletime -= 1
                
            self.timerlabel.configure(text=display(self._remaining))
            self.progressbar.configure(value = (self._remaining)*100//self._barlen)


            if self._remaining <= 0 and self._task == 0:
                self.timerlabel.configure(text = display(self._remaining))
                self._remaining = self._rectime
                self.set_barlen(self._rectime)
                self._task += 1
                self.set_played(True)
            self._job = self.after(1000, self.countdown)  
            
        
def main():
  
    root = tk.Tk()
#    root.geometry("250x150+300+300")
    app = TOEFLTimer()
    root.mainloop()  
    
    
if __name__ == "__main__":
    app = TOEFLTimer()
