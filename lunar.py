import os
import sys

from pynput import keyboard
from termcolor import colored

def on_release(key):
    try:
        if key == keyboard.Key.f2:
            SlowMouse.on_take_screenshot(apiKey="18704e15-6cce-db4f-5b88-6928c8529b1f:fx")
        if key == keyboard.Key.f3:
            SlowMouse.clean_up()
        if key == keyboard.Key.f4:
            os.system('python transitive.py -fs=True')
    except NameError:
        pass

def main():
    global lunar
    lunar = SlowMouse(collect_data = "collect_data" in sys.argv)
    lunar.start()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    print(colored('''
    ___     _______      ________   _______ _____            _   _  _____ _            _______ ____  _____    
    | |    |_   _\ \    / /  ____| |__   __|  __ \     /\   | \ | |/ ____| |        /\|__   __/ __ \|  __ \  
    | |      | |  \ \  / /| |__       | |  | |__) |   /  \  |  \| | (___ | |       /  \  | | | |  | | |__) | 
    | |      | |   \ \/ / |  __|      | |  |  _  /   / /\ \ | . ` |\___ \| |      / /\ \ | | | |  | |  _  /  
    | |____ _| |_   \  /  | |____     | |  | | \ \  / ____ \| |\  |____) | |____ / ____ \| | | |__| | | \ \  
    |______|_____|   \/   |______|    |_|  |_|  \_\/_/    \_\_| \_|_____/|______/_/    \_\_|  \____/|_|  \_\ 
    \n(Neural Network Translate)''', "light_cyan"))

    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")

    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists:
        print(colored('''[WARNING] Launch python setup.py for set the settings position of the text at translate''', "red"))
        os._exit(0)
    
    from lib.slowmouse import SlowMouse
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
