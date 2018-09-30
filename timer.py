# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 20:08:31 2018

@author: ray
"""
import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
import winsound
import math
import wave
import contextlib
#from recorder import record as rec
import subprocess
#from multiprocessing import Process, Queue
import sys
import re
import datetime
import os

def path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_filename():
    time_startrecord = re.sub('[^A-Za-z0-9]+', '', str(datetime.datetime.now()))
    return time_startrecord[:14] + ".wav"

def get_time(filename):
    pf = filename
    with contextlib.closing(wave.open(pf,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return math.ceil(round(frames / float(rate), 3))
    
def display(time):
    s, cs = divmod(time, 100)
    m, s = divmod(s, 60)
#    h, m = divmod(m, 60)
#    return "%d:%02d:%02d:%02d" % (h, m, s, cs)
    return "%02d:%02d:%02d" % (m, s, cs)

def load_image(filename, factor = 1):
    load = Image.open(filename)
    x,y = load.size
    render = ImageTk.PhotoImage(load.resize((int(x*factor),int(y*factor)), Image.ANTIALIAS))
    return render

class TOEFLTimer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
#        self.pack(padx=20, pady=20)
        self.title("TEOFL Speaking Timer")
        
        self.geometry("500x450")
        self.resizable(0, 0)
        
        self._welcome = "Welcome to TOEFL Timer Lite"
        self.label = tk.Label(self, text = self._welcome, width=35, font = "Helvetica 12 bold")
        
        # adding "the man" image
        self._theman = load_image(path("resources/theman.jpg"), 0.75)
        self.canvas = tk.Label(self, image=self._theman)
#        self.canvas.image = self._theman
        self.canvas.place(x=0, y=0)
        
        self._recording = load_image(path("resources/recording.png"), 0.02)
        self._recording1 = load_image(path("resources/recording1.png"), 0.02)
        self._playing = load_image(path("resources/playing.png"), 0.02)
        self._playing1 = load_image(path("resources/playing1.png"), 0.02)
        self._recordingindic = True
        self._playingindic = False
        self.recording = tk.Label(self, image=None)
#        self.recording.image = self._recording
        self.recording.place(x=0, y=0)
        
        self.label_timer = tk.Label(self, text="", width=35, font = "Helvetica 16 bold")
        self.bar = tk.Label(self, width=100, font = "Helvetica 5")
#        self.geometry("360x120")
        self.label.pack(padx=20, pady=20)
        self.canvas.pack(padx=10, pady=10)
        self.label_timer.pack()
        self.bar.pack(anchor="w", padx=50, pady=10)
        
#        self.label.grid(column=0, row=1)
#        self.label_timer.grid(column=0, row=2)
        self._job = None
        self._task = 0
        self._prepare = "Begin to prepare your response after the beep!"
        self._speak = "Begin speak after the beep!"
        self._remaining = 1500
        self._barlen = 15
        self._played = 1
        self._recordstart = 1
        self._play = None
        self._idletime = 0
        self.protocol("WM_DELETE_WINDOW", self.simple_close)
        self._filename = ''
        
        def clicked0():
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
                
        def clicked1():
            if self.button2['state'] == 'normal':
                self.button2.config(state = 'disabled')
                self.button1.config(state = 'normal', text = 'Start')
                self.reset()
#        self.button0 = tk.Button(self)
        self.button1 = tk.Button(self, text="Start", command = clicked0, font = "Helvetica 12 bold")
        self.button2 = tk.Button(self, text="Restart", state="disabled", command = clicked1, font = "Helvetica 12 bold")
        
#        self.button0.pack(side=tk.LEFT,anchor=tk.CENTER, padx=60, pady=20)
        self.button2.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=65, pady=20)
        self.recording.pack(side=tk.RIGHT,anchor=tk.CENTER, padx=55)
        self.button1.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=55, pady=20)
#        self.button1.grid(column=0, row=3)
#        self.button2.grid(column=0, row=4)
        self.mainloop()
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            winsound.PlaySound(None, winsound.SND_PURGE)
            
    def blinking(self):
        if self._task == 1:
            if self._recordingindic:
                self.recording.configure(image = self._recording1)
                self._recordingindic = False
            else:
                self.recording.configure(image = self._recording)
                self._recordingindic = True
        if self._task == 2:
            if self._playingindic:
                self.recording.configure(image = self._playing)
                self._playingindic = False
            else:
                self.recording.configure(image = self._playing1)
                self._playingindic = True
            
    def simple_close(self):
        self.destroy()
        winsound.PlaySound(None, winsound.SND_PURGE)
        
    def reset(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
            self._task = 0
        self.label.configure(text = self._welcome)
        self.label_timer.configure(text = "")
        self.bar.configure(background = "grey94")
        self._remaining = 1500
        self._played = 1
        self._recordstart = 1
        self._play = None
        self._idletime = 0
        self._barlen = 15
        self._recordingindic = True
        winsound.PlaySound(None, winsound.SND_PURGE)
        
    def countdown(self, remaining = None, pause = False):
        
        self.bar.configure(background = "gainsboro")
        if remaining is not None:
            self._remaining = remaining


        if self._remaining <= 0 and self._task > 0:

#            self.label_timer.configure(text=self._remaining)
            self.bar.configure(background = "grey94")
            self.recording.configure(image = self._playing)
            if self._task == 1:
                self.label_timer.configure(text="Time's up!")
                self.button1.config(text = 'Play')
                self._playingindic = True
                self._task = 2
                self._remaining = 4500
                self._played = 1
            else:
                self.label_timer.configure(text="You've completed!")
#            if self._playingindic == True:
#                winsound.PlaySound(self._filename, winsound.SND_ASYNC)
#                self.blinking()
#        elif self._remaining < 0 and self._task == 0:
            
            
        
        elif pause:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self._idletime = 0
            self.label_timer.configure(text= display(self._remaining))
            self.bar.configure(width = (self._remaining//self._barlen), anchor="w")
            if self._job is not None:
                self.after_cancel(self._job)
                self._job = None
            
        else:
            if self._task == 0:
                self.label.configure(text = self._prepare)
                if self._played:
                    winsound.PlaySound(path('resources/15.wav'), winsound.SND_ASYNC)
                    self._played -= 1
                    self._idletime = get_time(path('resources/15.wav'))*100
            elif self._task == 1:
                self.label.configure(text = self._speak)
                if self._played:
                    winsound.PlaySound(path('resources/45.wav'), winsound.SND_ASYNC)
                    self._played -= 1
                    self._idletime = get_time(path('resources/45.wav'))*100
                if self._recordstart and not self._idletime:
                    self._filename = get_filename()
                    si = subprocess.STARTUPINFO()
                    si.dwFlags|= subprocess.STARTF_USESHOWWINDOW
                    #subprocess.Popen([sys.executable, path('resources/recorder.py'), self._filename], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,startupinfo=si)
                    subprocess.Popen([path('resources/recorder.exe'), self._filename], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,startupinfo=si)
#                    cmd = [sys.executable, '-c', "import recorder; recorder.record(45, '111.wav')"]
#                    subprocess.Popen(cmd,stdin=child1.stdout,stdout=subprocess.PIPE)
                    self._recordstart -= 1
            else:
                if self._played:
                    self.label.configure(text = "Review your recording...")
                    winsound.PlaySound(self._filename, winsound.SND_ASYNC)
#                    self._idletime = get_time(self._filename)*100
                    self._played -= 1

#                    self.reset()
            
            if self._remaining < 0 and self._task == 0:
                self._remaining = 4501   
                self._barlen = 45
                self._task += 1
                self._played = 1
                
                
            self.label_timer.configure(text=display(self._remaining))
            self.bar.configure(width = (self._remaining//self._barlen), anchor="w")
            if not self._idletime:
                self._remaining -= 1
                if self._remaining%100 == 0:
                    self.blinking()

            else:
                self._idletime -= 1
            self._job = self.after(10, self.countdown)  
            
        
if __name__ == "__main__":
    app = TOEFLTimer()
