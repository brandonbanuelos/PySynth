import numpy as np
import pyaudio
import tkinter

import matplotlib.style
import matplotlib
matplotlib.use("TkAgg")
matplotlib.style.use('dark_background')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter.ttk import *

import random 

import wavio

p = pyaudio.PyAudio()

#class to handle the creation of different sound waves
class Oscillator1(object):
    def __init__(self):
        #Volume
        self.waveform = 'Sine Wave'
        self.volume = 0.5
        #Samples per second
        self.sps = 44100
        #Frequency of the note C5 at default
        self.freq = 500
        #Seconds played
        self.duration = 1
        self.everySample = None
        self.wave = None

    #make sure the wave is created when frequency is updated
    def makeWave(self):
        self.everySample = np.arange(self.duration*self.sps)
        #Create sine wave
        if self.waveform == 'Sine Wave':
            self.wave =np.sin(2*np.pi*self.everySample
            *self.freq/self.sps).astype(np.float32)
        elif self.waveform == 'Square Wave':
            wave = np.sin(2*np.pi*self.everySample*
            self.freq/self.sps).astype(np.float32)
            #np.sign() floors the values of the sin wave to 1 if it is above 0
            #and -1 it is below 0 like a square wave
            self.wave = np.sign(wave)
        elif self.waveform == 'Sawtooth Wave':
            #np.modf() creates a tuple of values in the array. The first is all
            #the values that are fractional components of numbers and the second
            #is all of the whole numbers. I index the first part of the tuple
            #to create the sawtooth where all the decimals lie
            #adapted from https://stackoverflow.com/questions/51452675/why-does-playing-a-triangle-wave-via-pyaudio-destroy-my-earbuds
            self.wave = (np.modf(np.arange(self.sps*self.duration)
            *self.freq/self.sps)[0]).astype(np.float32)
        
    #callable function to update the volume in the model
    def newVolume(self,volume):
        self.volume = volume

#second oscillator to combine waveforms with the first for unique sound combinations
class Oscillator2(object):
    def __init__(self):
        #Volume
        self.waveform = 'Sine Wave'
        self.volume = 0.5
        #Samples per second
        self.sps = 44100
        #Frequency of the note C5 at default
        self.freq = 500
        #Seconds played
        self.duration = 1
        self.everySample = None
        self.wave = None

    #make sure the wave is created when frequency is updated
    def makeWave(self):
        self.everySample = np.arange(self.duration*self.sps)
        #Create sine wave
        if self.waveform == 'Sine Wave':
            self.wave = np.sin(2*np.pi*self.everySample
            *self.freq/self.sps).astype(np.float32)
        elif self.waveform == 'Square Wave':
            wave = np.sin(2*np.pi*self.everySample*
            self.freq/self.sps).astype(np.float32)
            #np.sign() floors the values of the sin wave to 1 if it is above 0
            #and -1 it is below 0 like a square wave
            self.wave = np.sign(wave)
        elif self.waveform == 'Sawtooth Wave':
            #adapted from https://stackoverflow.com/questions/51452675/why-does-playing-a-triangle-wave-via-pyaudio-destroy-my-earbuds
            self.wave = (np.modf(np.arange(self.sps*self.duration)
            *self.freq/self.sps)[0]).astype(np.float32)
        
    #callable function to update the volume in the model
    def newVolume(self,volume):
        self.volume = volume

class Display(object):
    def __init__(self):
        self.oscillator1 = Oscillator1()
        self.oscillator2 = Oscillator2()
        self.root = tkinter.Tk()
        self.root.geometry("1000x800")
        self.root.configure(bg="black")
        self.root.configure(highlightbackground = 'black')
        self.root.configure(borderwidth = 0)
        self.root.configure(highlightcolor = 'black')
        #image from https://media.giphy.com/media/148QEiAVkOBwbu/giphy.gif
        self.image = tkinter.PhotoImage(file = 'SynthBackground.gif')
        self.background = tkinter.Label(self.root, image = self.image,
        borderwidth = 0,highlightthickness = 0)
        self.background.place(x=0,y=0)
        self.root.title("PySynth")
        self.title = tkinter.Label(self.root,
        text = "PySynth",font = ('Times',50),bg = 'black',
        fg = 'white',borderwidth = 0,highlightthickness = 0)
        self.title.grid(column =5, row = 0)
        ########################################################################
        #Oscillator 1 Stuff
        ########################################################################
        self.scale = tkinter.Scale(self.root, from_=0, to=10,label = "Volume 1",
        bg = 'black',fg = 'white',highlightthickness = 2,highlightcolor='white')
        self.scale.set(5)
        self.scale.grid(column = 1, row = 4)
        self.button = tkinter.Button(self.root,text =
         f'{self.oscillator1.waveform}',bg ='black',command=self.changeWaveform)
        self.button.grid(column = 1, row = 3)
        self.oscillator1Label = tkinter.Label(self.root,text =
         "Oscillator 1",font = ('Times',30),bg = 'black',fg = 'white',
         borderwidth = 0,highlightthickness = 0)
        self.oscillator1Label.grid(column = 1,row = 2,sticky = E)
        self.note = ""
        self.noteLabel = tkinter.Label(self.root, text =
         f'Note played: {self.note}',bg= 'black',fg = 'white')
        self.noteLabel.grid(column = 1, row = 1)
        ########################################################################
        #Oscillator 2 Stuff
        ########################################################################
        self.oscillator2Label = tkinter.Label(self.root,text
         = "Oscillator 2",font = ('Times',30),bg = 'black',fg = 'white',)
        self.oscillator2Label.grid(column = 2, row = 2)
        self.scale2 = tkinter.Scale(self.root, from_=0, to=10,label
         = "Volume 2",bg = 'black',fg = 'white',
         highlightthickness = 2,highlightcolor='white')
        self.scale2.set(5)
        self.scale2.grid(column = 2, row =4)
        self.button2 = tkinter.Button(self.root,text =
         f'{self.oscillator2.waveform}',bg ='blue',command=self.changeWaveform2)
        self.button2.grid(column = 2,row = 3)
        ########################################################################
        #General Stuff
        ########################################################################
        self.pitch = tkinter.Scale(self.root,from_=250, to=-250,label =
         "Pitch Bender",bg = 'black',fg = 'white',highlightthickness = 2,
         highlightcolor='white')
        self.pitch.set(0)
        self.pitch.grid(column = 1, row = 5)
        self.filter = tkinter.Scale(self.root,from_=100, to = 0, label =
         "Wave Shaper",bg = 'black',fg = 'white',highlightthickness = 2,
         highlightcolor='white')
        self.filter.set(100)
        self.filter.grid(column = 1, row = 6)
        self.helpButton = tkinter.Button(self.root,text = "Help",
         command = self.displayHelp)
        self.helpButton.grid(column = 4, row = 2)
        self.randomButton = tkinter.Button(self.root, 
        text = "Random Settings", command = self.random)
        self.randomButton.grid(column = 6, row = 2)
        self.root.bind('<Key>',self.playNote)
        self.delay = 100
        self.pitchLevel = 0
        self.pitchBend()
        self.filterLevel = 0
        self.filterChange()
        self.sliderVolume()
        self.slider2Volume()
        self.drawGraph()
        #dictionary of frequencies for each note
        self.noteFreq = {'C5':523.25,'q':523.25,
                'D5':587.33, 'w':587.33,
                'E5':659.25, 'e':659.25,
                'F5':698.46, 'r':698.46,
                'G5':783.99, 't':783.99,
                'A5':880.00, 'y':880.00,
                'B5':987.77, 'u':987.77,
                'C4':261.63, 'z':261.63,
                'D4':293.66, 'x':293.66,
                'E4':329.63, 'c':329.63,
                'F4':349.23, 'v':349.23,
                'G4':392.00, 'b':392.00,
                'A4':440.00, 'n':440.00,
                'B4':493.88, 'm':493.88,
                'C5#':554.37, '2':554.37,
                'D5#':622.25, '3':622.25,
                'F5#':739.99, '5':739.99,
                'G5#':830.61, '6':830.61,
                'A5#':932.33, '7':932.33,
                'C6':1046.50, 'i':1046.50,
                'D6':1174.66, 'o':1174.66,
                'E6':1318.51, 'p':1318.51,
                'F6':1396.91, '[':1369.91,
                'G6':1567.98, ']':1567.98,
                'C4#':277.18, 's':277.18,
                'D4#':311.13, 'd':311.13,
                'F4#':369.99, 'g':369.99,
                'G4#':415.30, 'h':415.30,
                'A4#':466.16, 'j':466.16
                }
        ########################################################################
        #Record/Play Stuff
        ########################################################################
        self.recordButton = tkinter.Button(self.root,text = 'Record',
        command =self.record)
        self.recordButton.grid(column = 2, row = 5)
        self.recording = False
        #preload Ode to Joy
        self.record = ['E5','E5','F5','G5','G5','F5','E5','D5','C5',
        'C5','D5','E5','E5','D5','D5']
        self.playButton = tkinter.Button(self.root,text = 'Play',
        command = self.playRecorded)
        self.playButton.grid(column = 2, row = 6)
        self.saveSoundButton = tkinter.Button(self.root, text =
         'Save Sound',command = self.saveSound)
        self.saveSoundButton.grid(column = 5, row = 2)
        self.currentSound = 0
        self.loadPreset = tkinter.Button(self.root,text = 
        "Load Preset",command = self.openPreset)
        self.loadPreset.grid(column = 6, row =3)
        self.savePreset = tkinter.Button(self.root,text =
        "Save Preset",command = self.savePreset)
        self.savePreset.grid(column = 6, row = 4)
        ########################################################################
        #Piano Keyboard Stuff
        ########################################################################
        #plots each button to a note
        self.C5Button = Button(self.root, text = "C5", width = 4,
         command = lambda: self.playFromRecording('C5'))
        self.C5Button.grid(column = 1, row = 8)
        self.C5SButton = Button(self.root, text = "C5#", width = 4,
         command = lambda: self.playFromRecording('C5#'))
        self.C5SButton.grid(column = 2, row = 7)
        self.D5Button = Button(self.root, text = "D5", width = 4,
         command = lambda: self.playFromRecording('D5'))
        self.D5Button.grid(column = 2, row = 8)
        self.D5SButton = Button(self.root, text = "D5#", width = 4,
         command = lambda: self.playFromRecording('D5#'))
        self.D5SButton.grid(column = 3, row = 7)
        self.E5Button = Button(self.root, text = "E5", width = 4,
         command = lambda: self.playFromRecording('E5'))
        self.E5Button.grid(column = 3, row = 8)
        self.F5Button = Button(self.root, text = "F5", width = 4,
         command = lambda: self.playFromRecording('F5'))
        self.F5Button.grid(column = 4, row = 8)
        self.F5SButton = Button(self.root, text = "F5#", width = 4,
         command = lambda: self.playFromRecording('F5#'))
        self.F5SButton.grid(column = 4, row = 7)
        self.G5Button = Button(self.root, text = "G5", width = 4,
         command = lambda: self.playFromRecording('G5'))
        self.G5Button.grid(column = 5, row = 8)
        self.G5SButton = Button(self.root, text = "G5#", width = 4,
         command = lambda: self.playFromRecording('G5#'))
        self.G5SButton.grid(column = 5, row = 7)
        self.A5Button = Button(self.root, text = "A5", width = 4,
         command = lambda: self.playFromRecording('A5'))
        self.A5Button.grid(column = 6, row = 8)
        self.A5SButton = Button(self.root, text = "A5#", width = 4,
         command = lambda: self.playFromRecording('A5#'))
        self.A5SButton.grid(column = 6, row = 7)
        self.B5Button = Button(self.root, text = "B5", width = 4,
         command = lambda: self.playFromRecording('B5'))
        self.B5Button.grid(column = 7, row = 8)

    #play note based on keyboard press
    def playNote(self,event):
        
        if event.char == 'q':
            self.oscillator1.freq = self.noteFreq['C5'] + self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C5"
        elif event.char == 'w':
            self.oscillator1.freq = self.noteFreq['D5'] + self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D5"
        elif event.char == 'e':
            self.oscillator1.freq = self.noteFreq['E5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['E5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: E5"
        elif event.char == 'r':
            self.oscillator1.freq = self.noteFreq['F5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['F5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: F5"
        elif event.char == 't':
            self.oscillator1.freq = self.noteFreq['G5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['G5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: G5"
        elif event.char == 'y':
            self.oscillator1.freq = self.noteFreq['A5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['A5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: A5"
        elif event.char == 'u':
            self.oscillator1.freq = self.noteFreq['B5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['B5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: B5"
        elif event.char == 'i':
            self.oscillator1.freq = self.noteFreq['C6']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C6'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C6"
        elif event.char == 'o':
            self.oscillator1.freq = self.noteFreq['D6']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D6'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D6"
        elif event.char == 'p':
            self.oscillator1.freq = self.noteFreq['E6']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['E6'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: E6"
        elif event.char == '[':
            self.oscillator1.freq = self.noteFreq['F6']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['F6'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: F6"
        elif event.char == ']':
            self.oscillator1.freq = self.noteFreq['G6']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['G6'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: G6"
        elif event.char == '2':
            self.oscillator1.freq = self.noteFreq['C5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C5#"
        elif event.char == '3':
            self.oscillator1.freq = self.noteFreq['D5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D5#"
        elif event.char == '5':
            self.oscillator1.freq = self.noteFreq['F5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['F5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: F5#"
        elif event.char == '6':
            self.oscillator1.freq = self.noteFreq['G5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['G5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: G5#"
        elif event.char == '7':
            self.oscillator1.freq = self.noteFreq['A5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['A5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: A5#"
        elif event.char == 'z':
            self.oscillator1.freq = self.noteFreq['C4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C4"
        elif event.char == 'x':
            self.oscillator1.freq = self.noteFreq['D4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D4"
        elif event.char == 'c':
            self.oscillator1.freq = self.noteFreq['E4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['E4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: E4"
        elif event.char == 'v':
            self.oscillator1.freq = self.noteFreq['F4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['F4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: F4"
        elif event.char == 'b':
            self.oscillator1.freq = self.noteFreq['G4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['G4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: G4"
        elif event.char == 'n':
            self.oscillator1.freq = self.noteFreq['A4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['A4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: A4"
        elif event.char == 'm':
            self.oscillator1.freq = self.noteFreq['B4']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['B4'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: B4"
        elif event.char == ',':
            self.oscillator1.freq = self.noteFreq['C5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C5"
        elif event.char == '.':
            self.oscillator1.freq = self.noteFreq['D5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D5"
        elif event.char == '/':
            self.oscillator1.freq = self.noteFreq['E5']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['E5'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: E5"
        elif event.char == 's':
            self.oscillator1.freq = self.noteFreq['C4#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C4#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C4#"
        elif event.char == 'd':
            self.oscillator1.freq = self.noteFreq['D4#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D4#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D4#"
        elif event.char == 'g':
            self.oscillator1.freq = self.noteFreq['F4#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['F4#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: F4#"
        elif event.char == 'h':
            self.oscillator1.freq = self.noteFreq['G4#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['G4#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: G4#"
        elif event.char == 'j':
            self.oscillator1.freq = self.noteFreq['A4#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['A4#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: A4#"
        elif event.char == 'l':
            self.oscillator1.freq = self.noteFreq['C5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['C5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: C5#"
        elif event.char == ';':
            self.oscillator1.freq = self.noteFreq['D5#']+ self.pitchLevel
            self.oscillator2.freq = self.noteFreq['D5#'] + self.pitchLevel
            self.noteLabel['text'] = "Note played: D5#"
        #make the extra keypresses play no sound except designated ones
        else:
            self.oscillator1.freq = 0
            self.oscillator2.freq = 0
        #alter frequency and update it in the wave
        self.oscillator1.makeWave()
        self.oscillator2.makeWave()
        #play the sound after altering frequency
        self.playSound()
        if self.recording == True:
            self.record.append(event.char)

    #get value from bitch bend slider and apply to frequency
    def pitchBend(self):
        self.root.after(self.delay,self.pitchBend)
        self.pitchLevel = self.pitch.get()

    #always check the slider volume to update the oscillator1 volume
    def sliderVolume(self):
        self.root.after(self.delay,self.sliderVolume)
        volume = self.scale.get()
        self.oscillator1.newVolume(volume/10)
    
    #always check the slider volume to update the oscillator2 volume
    def slider2Volume(self):
        self.root.after(self.delay,self.slider2Volume)
        volume = self.scale2.get()
        self.oscillator2.newVolume(volume/10)

    #change oscillator 1 waveform
    def changeWaveform(self):
        if self.oscillator1.waveform == 'Sine Wave':
            self.oscillator1.waveform = 'Square Wave'
        elif self.oscillator1.waveform == 'Square Wave':
            self.oscillator1.waveform = 'Sawtooth Wave'
        elif self.oscillator1.waveform == 'Sawtooth Wave':
            self.oscillator1.waveform = 'Sine Wave'
        self.button['text'] = self.oscillator1.waveform

    #change oscillator 2 waveform
    def changeWaveform2(self):
        if self.oscillator2.waveform == 'Sine Wave':
            self.oscillator2.waveform = 'Square Wave'
        elif self.oscillator2.waveform == 'Square Wave':
            self.oscillator2.waveform = 'Sawtooth Wave'
        elif self.oscillator2.waveform == 'Sawtooth Wave':
            self.oscillator2.waveform = 'Sine Wave'
        self.button2['text'] = self.oscillator2.waveform

    #takes the information from the slider to update the value
    def filterChange(self):
        self.root.after(self.delay,self.filterChange)
        self.filterLevel = self.filter.get()
        
    #np.add combines the values in each array to create the combined wave
    def combineWaveforms(self):
        wave1 = self.oscillator1.volume * self.oscillator1.wave
        wave2 = self.oscillator2.volume * self.oscillator2.wave
        return np.add(wave1,wave2)

    #play the combined wave
    def playSound(self):
        wave = self.combineWaveforms()
        #limits the maxium value by the filter level applied by the slider
        wave = np.clip(wave, -10,self.filterLevel/100)
        #loads the soundsave with the current wave
        self.currentSound = wave
        #clear the graph before the next note
        self.plot.clear()
        self.plot.set_title('Waveform')
        #plot part of the current wave each time sound is played
        self.plot.plot(wave[:500],color = 'green',label = 'Current Waveform')
        self.figure.draw()
        #open stream and begin playback
        stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=self.oscillator1.sps,
                output=True)
        stream.write(wave)
    
    #draws the graph of the waveform
    def drawGraph(self):
        #self.fig = Figure(figsize=(3, 2), dpi=100)
        self.fig = Figure(figsize=(3, 3))
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.set_title('Waveform')
        self.figure = FigureCanvasTkAgg(self.fig, master = self.root)
        self.figure.draw()
        self.figure.get_tk_widget().grid(column = 5, row = 4)
    
    #resets the list of notes and changes text if it is capturing notes
    def record(self):
        if self.recording == False:
            self.record = []
            self.recording = True
            self.recordButton['text'] = 'Recording'
            self.recordButton.configure(foreground = 'red')
            self.recordButton.configure(bg = 'red')
        elif self.recording == True:
            self.recording = False
            self.recordButton.configure(foreground = 'black')
            self.recordButton['text'] = 'Record'

    #plays each note in the recorded one at a time
    def playRecorded(self):
        for char in self.record:
            self.playFromRecording(char)

    #similar to playSound it updates the wave and takes in an input to find the
    #frequency within the dictionary
    def playFromRecording(self,char):
        freq = self.noteFreq[char]
        self.oscillator1.freq = freq + self.pitchLevel
        self.oscillator2.freq = freq + self.pitchLevel
        self.oscillator1.makeWave()
        self.oscillator2.makeWave()
        self.playSound()

    #sets the values of the sliders to random values as well as set the oscillators
    #to random wave forms separate of each other
    def random(self):
        self.scale.set(random.randint(1,10))
        self.scale2.set(random.randint(1,10))
        self.pitch.set(random.randint(1,250))
        self.filter.set(random.randint(1,100))
        waveform1 = ['Sine Wave','Square Wave','Sawtooth Wave'][random.randint(0,2)]
        self.oscillator1.waveform = waveform1
        self.button['text'] = self.oscillator1.waveform
        waveform2 = ['Sine Wave','Square Wave','Sawtooth Wave'][random.randint(0,2)]
        self.oscillator2.waveform = waveform2
        self.button2['text'] = self.oscillator2.waveform

    #creates a popup to get text entry
    def saveSound(self):
        self.popup = Toplevel(self.root)
        self.popup.geometry('200x100')
        self.popup.title("Enter a filename")
        self.popup.configure(bg = 'black')
        self.filename = tkinter.Entry(self.popup)
        self.filename.grid(column = 0,row = 1)
        self.submit = tkinter.Button(self.popup,text = "Save",command = self.saveFile,bg = 'black')
        self.submit.grid(column = 0, row = 0)

    #takes the entered filename and saves the wave file under it
    def saveFile(self):
        filename = str(self.filename.get())
        wavio.write(filename+'.wav',self.currentSound,self.oscillator1.sps,sampwidth = 1)
        self.popup.destroy()    

    #open search box to open custom preset
    def openPreset(self):
        #open file from dialog box
        currentFile = filedialog.askopenfilename(parent = self.root)
        self.settings = dict()
        contents = open(currentFile,'r')
        #iterate over every item in the file
        for item in contents:
            #each item is on a different line split based on spaces so 
            #key and value can be assigned based on the space difference
            key,value = item.split()
            try:
                self.settings[key]=int(value)
            except:
                self.settings[key]=str(value)
        #call change settings to apply the change
        self.changeSettings()
    
    #trys to change all the settings by reading the dictionary that it is given
    def changeSettings(self):
        try:
            self.oscillator1.newVolume(self.settings['oscillator1.volume'])
            self.scale.set(self.oscillator1.volume)
            self.oscillator2.newVolume(self.settings['oscillator2.volume'])
            self.scale2.set(self.oscillator2.volume)
            self.pitch.set(self.settings['pitch'])
            self.filter.set(self.settings['filter'])
            self.oscillator1.waveform = (self.settings['oscillator1.waveform']+' '+'Wave')
            self.button['text'] = self.oscillator1.waveform
            self.oscillator2.waveform = (self.settings['oscillator2.waveform']+' '+'Wave')
            self.button2['text']=self.oscillator2.waveform
        except:
            pass

    #saves to a txt file the settings on the synth in the
    # necessary format to be loaded for later
    def savePreset(self):
        currentFile = filedialog.asksaveasfilename(parent = self.root,defaultextension='.txt')
        f = open(currentFile,'w')
        oscillator1wave,wave = self.oscillator1.waveform.split()
        oscillator2wave,wave = self.oscillator2.waveform.split()
        f.write(f'''oscillator1.volume {self.scale.get()}\
        \noscillator2.volume {self.scale2.get()}\
        \npitch {self.pitch.get()}\
        \nfilter {self.filter.get()}\
        \noscillator1.waveform {oscillator1wave}\
        \noscillator2.waveform {oscillator2wave}''')

    #creates a new window that displays instructions and general information
    def displayHelp(self): 
        self.help = Toplevel(self.root)
        self.help.geometry('1000x800')
        self.help.configure(bg = 'black')
        self.helpLabel = tkinter.Label(self.help, text = 'Help Screen', font = ('Times',50), bg = 'black',fg = 'white')
        self.helpLabel.grid(column = 1, row = 1) 
        self.text = tkinter.Label(self.help, text = '',bg = 'black',fg = 'white')
        self.text.configure(text =
        '''Welcome to PySynth!
        
        Synthesis:
        This virutal analog monophonic synthesizer relies on some basic knowledge
        of synthesis.
        To begin, there are two oscillators with the option for sine,square, and
        sawtooth waveforms. The volume for each can be controlled because it affects
        how much of each wave is added to the output wave sound.
        The pitch bend increases frequency of the waveform to create more interesting
        sounds.
        The wave shaper trims down on the top of the waveform to allow more of the low
        end to play and can help create new types of waves.

        Recording and Playback:
        The record feature takes the keyboard input and stores it when the "record"
        button is pressed. To stop recording, press the button when it says "recording"
        in red.
        The play button takes the recording and plays it until it is over.

        Saving Sounds:
        When you create a sound you like, you can press the "save sound" button
        to create wave file with the waveform that you have created in the last
        key you played. It will ask you to enter a name to save the file as.

        Presets:
        There is a button to save the preset of your choice as a txt file
        for later access. Additionally, there is a load preset option to access
        that file and load the values that were saved onto it.

        Generating Waves:
        The most important feature is the laptop keyboard piano keys. The mappings
        for this are displayed below.

            '2' - C5#  '3' - D5#    '5' - F5# '6' - G5# '7' - A5#
        'q' - C5 'w' - D5 'e' - E5 'r' - F5 't' - G5 'y' - A5 'u' - B5 'i' - C6 'o' - D6 'p' - E6 '[' - F6 ']' - G6

            's' - C4#  'd' - D4#    'g' - F4# 'h' - G4# 'j' - A4#             'l' - C5# ';' - D5#
        'z' - C4 'x' - D4 'c' - E4 'v' - F4 'b' - G4 'n' - A4 'm' - B4 ',' - C5 '.' - D5 '/' - E5
        
        With each button press, a sound will be played,
        and the waveform will be graphed in real time.

        Additionally, an octave of keys are placed on screen as buttons.
        ''')
        self.text.grid(column = 1, row = 2) 

    def start(self):
        self.root.mainloop()

Display().start()