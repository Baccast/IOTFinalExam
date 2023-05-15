import tkinter as tk
import tkinter.font as tkFont
import RPi.GPIO as GPIO
import time
import glob
import os

# Set up GPIO pins


class App:
    def __init__(self, root):
        # setting title
        root.title("IOT Final Exam")
        # setting window size
        width = 250
        height = 100
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_770 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_770["font"] = ft
        GLabel_770["fg"] = "#333333"
        GLabel_770["justify"] = "center"
        GLabel_770["text"] = "Temperature"
        GLabel_770.place(x=0, y=20, width=70, height=25)

        GLineEdit_667 = tk.Entry(root)
        GLineEdit_667["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_667["font"] = ft
        GLineEdit_667["fg"] = "#333333"
        GLineEdit_667["justify"] = "center"
        GLineEdit_667["text"] = ""
        GLineEdit_667.place(x=70, y=20, width=70, height=25)

        GButton_899 = tk.Button(root)
        GButton_899["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_899["font"] = ft
        GButton_899["fg"] = "#000000"
        GButton_899["justify"] = "center"
        GButton_899["text"] = "SET"
        GButton_899.place(x=150, y=20, width=70, height=25)
        GButton_899["command"] = self.GButton_899_command

        GLabel_321 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_321["font"] = ft
        GLabel_321["fg"] = "#333333"
        GLabel_321["justify"] = "center"
        GLabel_321["text"] = "FAN"
        GLabel_321.place(x=0, y=70, width=70, height=25)

        GButton_464 = tk.Button(root)
        GButton_464["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_464["font"] = ft
        GButton_464["fg"] = "#000000"
        GButton_464["justify"] = "center"
        GButton_464["text"] = "ON"
        GButton_464.place(x=70, y=70, width=70, height=25)
        GButton_464["command"] = self.GButton_464_command

        GButton_152 = tk.Button(root)
        GButton_152["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_152["font"] = ft
        GButton_152["fg"] = "#000000"
        GButton_152["justify"] = "center"
        GButton_152["text"] = "OFF"
        GButton_152.place(x=150, y=70, width=70, height=25)
        GButton_152["command"] = self.GButton_152_command

    def GButton_899_command(self):
        print("command")

    def GButton_464_command(self):
        print("command")

    def GButton_152_command(self):
        print("command")


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


if __name__ == "__main__":
    while True:
        print("Temperature: %.2f °C" % read_temp())
        time.sleep(1)
    # root = tk.Tk()
    # app = App(root)
    # root.mainloop()
