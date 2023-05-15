import tkinter as tk
import tkinter.font as tkFont
import os
import time
import threading


class Fan:
    def __init__(self):
        self.fan_running = False

    def turn_on(self):
        self.fan_running = True

    def turn_off(self):
        self.fan_running = False

    def status(self):
        return self.fan_running


class App:
    def __init__(self, root):
        self.fan = Fan()
        # setting title
        root.title("Fan Control")
        # setting window size
        width = 300
        height = 100
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.temperature_entry = tk.Entry(root, borderwidth="1px")
        self.temperature_entry.place(x=70, y=20, width=70, height=25)

        self.set_button = tk.Button(
            root, bg="#f0f0f0", text="SET", command=self.set_temperature)
        self.set_button.place(x=150, y=20, width=70, height=25)

        self.fan_label = tk.Label(root, text="FAN")
        self.fan_label.place(x=0, y=70, width=70, height=25)

        self.fan_on_button = tk.Button(
            root, bg="#f0f0f0", text="ON", command=self.turn_fan_on)
        self.fan_on_button.place(x=70, y=70, width=70, height=25)

        self.fan_off_button = tk.Button(
            root, bg="#f0f0f0", text="OFF", command=self.turn_fan_off)
        self.fan_off_button.place(x=150, y=70, width=70, height=25)

        # Initialize the maximum temperature
        self.max_temperature = None

        # Create a flag to control the loop
        self.running = True

        # Start the loop in a separate thread
        threading.Thread(target=self.loop).start()

    def set_temperature(self):
        # Make sure text box is not empty and only has numbers
        if not self.temperature_entry.get().isdigit():
            print("Invalid temperature")
            return
        temperature = self.temperature_entry.get()
        self.max_temperature = float(temperature)
        print("Set temperature:", self.max_temperature)

    def turn_fan_on(self):
        print("Fan turned ON")
        self.fan.turn_on()

    def turn_fan_off(self):
        print("Fan turned OFF")
        self.fan.turn_off()

    def read_sensor(self, id):
        tfile = open("/sys/bus/w1/devices/" + id + "/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        print(" - Current temperature: %0.3f C" % temperature)

        if self.max_temperature is not None and temperature >= self.max_temperature:
            if not self.fan.status():
                self.turn_fan_on()
        else:
            if self.fan.status():
                self.turn_fan_off()

    def read_sensors(self):
        for file in os.listdir("/sys/bus/w1/devices/"):
            if file.startswith("28-"):
                self.read_sensor(file)

    def loop(self):
        while self.running:
            self.read_sensors()
            time.sleep(1)

    def destroy(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    app.destroy()
