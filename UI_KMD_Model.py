# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import Screen
from kivy.graphics import Color, Rectangle
from kivymd.icon_definitions import md_icons
# NLP Model FILE
import numpy as np
from nlp_model import loaded_model, classes, prepare_data, tokenizer

class MyRoot(MDBoxLayout):
    orientation: "vertical"

    def classify_specialty(self):
        self.ids.output_label.text = str("Processing...")
        processed_data = prepare_data(self.ids.transcript_input.text,tokenizer)
        results = loaded_model.predict(processed_data)
        probs = results[0]
        self.ids.output_label.text = str(classes[np.argmax(probs)])
        self.ids.transcript_input.text = ""

class KMDMedicalSpecialtyClassifierApp(MDApp):
    def build(self):
        screen = Screen()
        screen.add_widget(MyRoot())
        screen.canvas.before.add(Color(172/255 ,221/255 ,231/255))  # Light blue color
        screen.canvas.before.add(Rectangle(size=screen.size, pos=screen.pos))
        return screen

if __name__ == '__main__':
    KMDMedicalSpecialtyClassifierApp().run()
