#GUI imports
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics','multisamples', '0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.properties import OptionProperty
Window.size = (600, 400)

#CNN imports 

from test_model_gui import TestDemo

# Declare screens
class MenuScreen(Screen):

    def closeapp(self):
        return Window.close()

class SettingsScreen(Screen):
    def fullscre(self):
        Window.fullscreen = 'auto'

    def smallscreen(self):
        Window.fullscreen = 0
        Window.size = (600, 400)
    


#ScreenManager
class StateMachine(ScreenManager):
    pass            
        
class RunDemoScreen(Screen):

    network = TestDemo()
    model_l = network.model_load()

    def file_dialog(self):
        Tk().withdraw()
        self.filename = askopenfilename()
        self.imageWid = self.ids['imageWidget']
        self.imageWid.source = self.filename
        if self.imageWid.source == '':
            self.imageWid.source = 'ImgBck.png'
        self.imageWid.opacity = 1 # to make it visible
        print(self.filename)
    
    def test(self):
        try:
            #self.model_l = self.network.model_load() 
            self.result = self.network.test_img(self.filename) 
            self.labell = self.ids['result']
            self.labell.text = str(self.result)
            print(self.result)

        except Exception:   
            pass

    def make_cam(self):
        self.cam_res = self.network.create_cam_model_plt(self.filename, self.model_l)
        return self.cam_res
            
   


class TestApp(App):
    language = OptionProperty('EN', options=('EN', 'BG'))
    use_kivy_settings = False

    def on_stop(self):
        print("App stopped succesfully")

    def build(self):
        self.icon = 'Logo 2.png'
        self.title = 'Pneumonia Detector'
        
    def switch_language(self,*args):
        print('get pressed')
        if self.language == 'EN':
            self.language = 'BG'
            print(self.language)
        elif self.language == 'BG':
            self.language = 'EN'
            print(self.language)
        else:
            pass

if __name__ == '__main__':
    TestApp().run()

