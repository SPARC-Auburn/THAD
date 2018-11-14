import sys
from tkinter import Tk, Label

class mainWindow:
    def __init__(self, fullscreen, debug):
        self.fullscreen = fullscreen
        self.debug = debug

    def start(self):
        root = Tk()

        if(self.fullscreen):
            root.attributes('-fullscreen', True)
        test_text = Label(root, text='Hello world!')
        test_text.pack()

        root.mainloop()