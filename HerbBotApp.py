# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:07:23 2021

@author: Emily
"""
import subprocess
import json
import requests
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.button import Button, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem

# Information for communicating with Raspberry Pi
rip = "192.168.69.67"
rfile_path = "Documents/Update.py"

Window.size = (300, 500)

Home = """
Screen:
    
    
    BoxLayout:
        orientation: 'vertical'
        
        MDToolbar:
            title: 'Herb-Bot'
            left_action_items: [["water", lambda x: app.popup_event()]]
            right_action_items: [["camera", lambda x: app.pop1()]]
            type: "top"
        

        
        MDCard:
                
            size_hint: None, None
            size: "280dp", "140dp"
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 6
            
            Image:
                source:"pngegg.png"
                size_hint: 0.5, 0.5
                pos_hint: {"center_y": .5}
            
            MDLabel:
                text: "Temperature"
            MDLabel:
                text: app.UpdateT 
                halign: "right"
                valign: "middle"
                
                
            MDIconButton:    
                icon: "refresh"
                pos_hint: {"right_x": .5, "right_y": .5}
                on_press:app.getTemperature()
                    
            
        MDCard:
                
            size_hint: None, None
            size: "280dp", "140dp"
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 6
            
            Image:
                source:"humidity.png"
                size_hint: 0.5, 0.5
                pos_hint: {"center_y": .5}
            
            MDLabel:
                text: "Humidity"
                
            MDLabel:
                text: app.UpdateH 
                halign: "right"
                valign: "middle"
                
            MDIconButton:    
                icon: "refresh"
                pos_hint: {"right_x": .5, "right_y": .5}
                on_press:app.getHumidity()

        
        MDCard:
                
            size_hint: None, None
            size: "280dp", "140dp"
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 6
            
            Image:
                source:"soil.png"
                size_hint: 0.5, 0.5
                pos_hint: {"center_y": .5}
            
            MDLabel:
                text: "Soil Moisture"
                pos_hint: {"centre_x": 2, "centre_y": 2}
                
            MDLabel:
                text: app.UpdateS
                halign: "right"
                valign: "middle"
                
            MDIconButton:    
                icon: "refresh"
                pos_hint: {"right_x": .5, "right_y": .5}
                on_press:app.getSoilMoisture()
       
"""


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class HerbBotApp(MDApp):
    url = 'https://herb-bot-1ce6a-default-rtdb.firebaseio.com/.json'
    imageurl = 'gs://herb-bot-1ce6a.appspot.com/.json'

    UpdateT = StringProperty('  ----')
    UpdateH = StringProperty('  ----')
    UpdateS = StringProperty('  ----')

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_hue = "300"
        #subprocess.run("ssh pi@{} python {}".format(rip, rfile_path), shell=True, check=True)
        self.root = Builder.load_string(Home)

    def patch(self, JSON):
        to_database = json.loads(JSON)
        requests.patch(url=self.url, json=to_database)

    def getTemperature(self):
        request = requests.get(self.url)
        weather = request.json()
        y = json.dumps(weather['Weather']['Temperature'])
        Y = (y + "'C")
        self.UpdateT = Y

    def getHumidity(self):
        request = requests.get(self.url)
        weather = request.json()
        p = json.dumps(weather['Weather']['Humidity'])
        P = (p + "%")
        self.UpdateH = P

    def getSoilMoisture(self):
        request = requests.get(self.url)
        weather = request.json()
        s = json.dumps(weather['Weather']['Soil Moisture'])
        S = (s + "%")
        self.UpdateS = S
        print(weather)

    def navigation_draw(self):
        print("Navigation")

    def display(self):
        self.dialog = MDDialog(title='User Garden',
                               type="simple",
                               size_hint=(0.8, 1),
                               buttons=[Button(text='Close', on_release=self.close_dialog),
                                        Button(source="soil.png")])
        self.dialog.open()
        print("popup open")

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def pop1(self):
        # Content for pop up window
        image = Image(source="light1.jpg", size=(250, 250))
        button = MDFlatButton(text='Close', text_color=(1, 1, 1, 1), size_hint=(0.8, 0.2))
        icon = MDIconButton(icon="download", md_bg_color=(1, 1, 1, 1))

        # Set up the popup window
        layout = GridLayout(rows=3, padding=0)
        layout.add_widget(image)
        layout.add_widget(button)
        # layout.add_widget(icon)
        pop1 = Popup(title='User Garden', content=layout, size_hint=(None, None), size=(300, 300))
        pop1.open()  # Open the pop up

        # ON button press close the popup
        button.bind(on_press=pop1.dismiss)

    def pop2(self):
        button1 = MDFlatButton(text='Close', text_color=(1, 1, 1, 1), size_hint=(1, 1))
        pop2 = Popup(title='         Water Level Low! : Please Refill ', content=button1, size_hint=(None, None),
                     size=(300, 100))
        pop2.open()  # Open the pop up

        # ON button press close the popup
        button1.bind(on_press=pop2.dismiss)

    def popup_event(self):
        water_level = 0

        if water_level == 1:
            self.pop2()
        if water_level == 0:
            self.pop2()


if __name__ == '__main__':
    HerbBotApp().run()
