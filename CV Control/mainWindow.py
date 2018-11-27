import sys
from kivy.app import App
from kivy.uix.widget import Widget



class Game(Widget):
        pass
        
class mainWindow(App):
    def build(self):
        return Game()
