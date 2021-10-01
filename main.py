from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem

import cv2
from pyzbar import pyzbar
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class ScreenManagement(ScreenManager):
    pass

class MainScreen(MDScreen):
    pass

class QRScreen(MDScreen):
    pass




class CameraView(Image):
    def __init__(self, **kwargs):
        super(CameraView, self).__init__(**kwargs)

        # connect to the 0th camera
        self.record = cv2.VideoCapture(0)

        # set the drawing interval
        Clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        # load frame
        ret, self.frame = self.record.read()
        # convert to kivy texture
        buf = cv2.flip(self.frame, 0).tobytes()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt='ubyte')

        # change the texture of the instance
        self.texture = texture
        self.get_video(self.frame)

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_info = barcode.data.decode('utf-8')
            self.parent.parent.ids['qrcode'].text = barcode_info
            self.get_code_data(barcode_info)
            with open("barcode_result.txt", mode ='w') as file:
                file.write("Recognized Barcode:" + barcode_info)

    def get_video(self,frame):
        self.read_barcodes(frame)

    def get_code_data(self, data_item):
        '''Get the qr code data, create list item and add it to the main window'''
        if data_item not in [i.text for i in self.parent.parent.parent.screens[0].ids.qrlist.children]:
            list_item = OneLineListItem(text=data_item)
            self.parent.parent.parent.screens[0].ids.qrlist.add_widget(list_item)
            
        


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

    def get_qrcode(self):
        self.root.current = 'qrscreen'

    def return_to_main(self):
        self.root.current = 'mainscreen'

    


if __name__ == '__main__':
    app = MainApp()
    app.run()