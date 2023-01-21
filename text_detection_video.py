import cv2
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np
from mss import mss
from PIL import Image
import os
import pyautogui
import time
from pynput import keyboard
from termcolor import colored

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

path = r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\1.png'


# img = cv2.imread(path)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# txt = pytesseract.image_to_string(img)
# translated = DeeplTranslator(api_key="18704e15-6cce-db4f-5b88-6928c8529b1f:fx", source='en', target='fr', use_free_api=True).translate('hello')  # output -> Weiter so, du bist großartig
# translated = GoogleTranslator(source='auto', target='fr').translate(text=txt)
# print(translated)

### Detecting Characters
# hImg, wImg, _ = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
#     cv2.rectangle(img, (x,hImg-y), (w,hImg-h), (0,0,255), 1)

# cv2.imshow('Result', img)
# cv2.waitKey(0)


# directory = r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img'
# Change the current directory 
# to specified directory 
# os.chdir(directory)
# List files and directories  
# in 'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img'  
# print("Before saving image:")  
# print(os.listdir(directory))  
filename = 'savedImage.png'

get1 = input('\nPlace cursor at the top left of the region you want to capture, and then press enter \n')
pos1 = pyautogui.position()

get2 = input('Now place your cursor at the bottom right of the region you want to capture, and press enter \n')
pos2 = pyautogui.position()

width = pos2[0] - pos1[0]
height = pos2[1] - pos1[1]

print('region=('+str(pos1[0])+','+str(pos1[1])+','+str(width)+','+str(height)+') \n')


sct = mss()

# path2 = r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img\\{}'.format(filename)
path2 = r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img\\translate.png'

def on_release(key):
    try:
        if key == keyboard.Key.f2:
            image = pyautogui.screenshot(region=(pos1[0],pos1[1],width,height))
            image.save(r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img\\translate.png')
            img2 = cv2.imread(path2)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            txt = pytesseract.image_to_string(img2)
            translated = GoogleTranslator(source='auto', target='fr').translate(text=txt)
            print(translated)
    except NameError:
        pass

print(colored('''
LIVE TRANSLATOR
''', "yellow"))
listener = keyboard.Listener(on_release=on_release)
listener.start()

bounding_box = {'top': 100, 'left': 300, 'width': 400, 'height': 300}
"""
while True:
    sct_img = sct.grab(bounding_box)
    cv2.imshow('screen', np.array(sct_img))
    # Using cv2.imwrite() method
    # Saving the image
    image = pyautogui.screenshot(region=(pos1[0],pos1[1],width,height))
    image.save(r'C:\\Users\\Sabri\\Desktop\\translate-chat-game\\img\\translate.png')
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)

    
    time.sleep(2)

    
    img2 = cv2.imread(path2)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    
    time.sleep(2)
    txt = pytesseract.image_to_string(img2)
    translated = GoogleTranslator(source='auto', target='fr').translate(text=txt)
    print(translated)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    time.sleep(5)
"""