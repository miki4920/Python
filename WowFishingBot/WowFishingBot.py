from PIL import ImageGrab
from pynput.mouse import Listener
import pynput.keyboard as keyboard
import tkinter as tk
import pyautogui
import numpy as np
import sounddevice as sd
import time
import psutil
import os


class Bot(object):
    def __init__(self):
        self.process_name = "WoW.exe"
        if not self.check_process():
            os._exit(0)
        pyautogui.PAUSE = 0.01
        self.start_x = -1
        self.start_y = -1
        self.current_x = -1
        self.current_y = -1
        self.end_x = -1
        self.end_y = -1
        self.pixel_location = []
        self.pixel_colour = []
        self.step = 20
        self.caught = False
        self.changed = False

        self.master = tk.Tk()
        self.get_resolution()
        self.configure_window()
        self.place_grid()
        self.coordinate_button()
        self.start_button()
        self.master.mainloop()

    def check_process(self):
        process_list = []
        for proc in psutil.process_iter():
            try:
                process_list.append(proc.name())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        if self.process_name in process_list:
            return True

    def get_resolution(self):
        scale = 0.3
        # Gets size of the screen
        resolution = pyautogui.size()
        resolution = [round(dimension * scale) for dimension in resolution]
        # Converts resolution into the format accepted by the program
        resolution = "%sx%s" % (resolution[0], resolution[1])
        self.master.geometry(resolution)
        # Doesn't allow user to rescale the window
        self.master.resizable(width=False, height=False)

    def configure_window(self):
        self.master.title("The Fishing Master")
        self.master.iconbitmap("icon.ico")
        self.master.configure(background="#A9A9A9")

    def place_grid(self):
        for i in range(0, 101):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def coordinate_button(self):
        button = tk.Button(self.master, text="Set Coordinates", command=self.set_coordinates)
        button.grid(column=50, row=1)

    def set_coordinates(self):
        listener = Listener(on_move=self.do_nothing(), on_click=self.click, on_scroll=self.do_nothing())
        with listener:
            listener.join()

    def click(self, x, y, button, pressed, ):
        if pressed:
            if not self.changed:
                self.start_x = x
                self.start_y = y
                self.changed = True
            elif self.changed:
                self.end_x = x
                self.end_y = y
                self.changed = False
                return False

    def do_nothing(self, *args):
        pass

    def start_button(self):
        button = tk.Button(self.master, text="Start", command=self.pixel_checker)
        button.grid(column=50, row=2)

    def pixel_checker(self):
        self.master.destroy()
        with keyboard.Listener(on_release=self.do_nothing, on_press=self.end_program):
            while True:
                self.current_x = self.start_x
                self.current_y = self.start_y
                pyautogui.keyDown("1")
                time.sleep(0.05)
                pyautogui.keyUp("1")
                self.caught = False
                while True:
                    pyautogui.moveTo(self.current_x, self.current_y, 0.01)
                    pixel = ImageGrab.grab().getpixel((1165, 619))
                    red = pixel[0]
                    green = pixel[1]
                    blue = pixel[2]
                    if 240 < red <= 255 and 170 < green < 220 and blue == 0:
                        self.sound_checker()
                        time.sleep(1)
                        break
                    else:
                        if self.change_coordinates():
                            break

    def change_coordinates(self):
        if self.current_x > self.end_x:
            self.current_x = self.start_x
            self.current_y += self.step * 2
            return False
        else:
            self.current_x += self.step
        if self.current_y > self.end_y:
            return True

    def sound_checker(self):
        duration = 15
        stream = sd.Stream(channels=2, callback=self.detect_sound)
        with stream:
            sd.sleep(duration * 1000)
            stream.close()

    def detect_sound(self, indata, *args):
        volume = int(np.linalg.norm(indata)*10)*10
        if volume > 10 and not self.caught:
            pyautogui.click()
            self.caught = True

    def end_program(self, key):
        if keyboard.Key.f9 == key:
            os._exit(0)
        else:
            pass


bot = Bot()
