import cv2
import json
import os
import pyautogui

from termcolor import colored
from tkinter import *

import pytesseract
from deep_translator import (GoogleTranslator, DeeplTranslator)

from rich.tree import Tree
from rich import print

class Translator:
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    """
    get1 = input(colored('''\nPlace cursor at the top left of the region you want to capture, and then press enter \n''', "blue"))
    pos1 = pyautogui.position()

    get2 = input(colored('''Now place your cursor at the bottom right of the region you want to capture, and press enter \n''', "blue"))
    pos2 = pyautogui.position()

    width = pos2[0] - pos1[0]
    height = pos2[1] - pos1[1]
    """
    # Get settings position of the text
    with open("lib/config/config.json") as f:
        position_settings = json.load(f)

    current_folder = os.getcwd()
    path = r'%s\\img\\translate.png' % current_folder

    def __init__(self, box_constant = 416, collect_data = False, mouse_delay = 0.0001, debug = False):
        t = colored('''\n[INFO] PRESS 'F2' TO TRANSLATE\n[INFO] PRESS 'F3' TO QUIT''', "blue")
        print("\n[INFO] PRESS 'F2' TO TRANSLATE\n[INFO] PRESS 'F3' TO QUIT")

    def on_take_screenshot(apiKey=""):
        # region=(SlowMouse.pos1[0], SlowMouse.pos1[1], SlowMouse.width, SlowMouse.height)
        # image = pyautogui.screenshot(region=(SlowMouse.pos1[0], SlowMouse.pos1[1], SlowMouse.width, SlowMouse.height))
        # os.system('cls')
        x = Translator.position_settings["x"]
        y = Translator.position_settings["y"]
        width = Translator.position_settings["width"]
        height = Translator.position_settings["height"]
        image = pyautogui.screenshot(region=(Translator.position_settings["x"], Translator.position_settings["y"], Translator.position_settings["width"], Translator.position_settings["height"]))
        image.save(Translator.path)
        img2 = cv2.imread(Translator.path)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        txt = pytesseract.image_to_string(img2)
        # translated = GoogleTranslator(source='en', target='fr').translate(text=txt)
        translated = DeeplTranslator(api_key=apiKey, source='en', target='fr', use_free_api=True).translate(txt)  # output -> Weiter so, du bist großartig

        tree = Tree("\nTranslation")
        tree.add('\n' + translated)
        tree.add(' ')
        print(tree)

    def start(self):
        
        while True:
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

    def clean_up():
        os._exit(0)

if __name__ == "__main__": print("[red]You are in the wrong directory and are running the wrong file; you must run lunar.py")
