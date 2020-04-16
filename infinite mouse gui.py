import tkinter as tk
from tkinter import messagebox

from pynput import keyboard, mouse
from pynput.keyboard import Key


class tkWin:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Infinite Mouse")
        self.window.geometry("+50+60")

        # vars
        self.currentStatus = tk.Variable(self.window, value="Off")
        self.preset = tk.Variable(self.window, value="Auto")
        self.xDim = tk.Variable(self.window, value="idk")
        self.yDim = tk.Variable(self.window, value="idk")
        self.onOff = tk.Variable(self.window, value=0)
        self.sW = tk.Variable(self.window, value=self.window.winfo_screenwidth())
        self.sH = tk.Variable(self.window, value=self.window.winfo_screenheight())
        self.sHN = tk.Variable(self.window, value=self.sH.get() * -1)
        self.sWN = tk.Variable(self.window, value=self.sW.get() * -1)

        # stuff
        self.presetLbl = tk.Label(self.window, text="Preset:")
        self.presetBox = tk.OptionMenu(self.window, self.preset, "Auto", "Manual")

        self.xDimLbl = tk.Label(self.window, text="Width:")
        self.xDimE = tk.Entry(self.window, textvariable=self.xDim)

        self.yDimLbl = tk.Label(self.window, text="Height:")
        self.yDimE = tk.Entry(self.window, textvariable=self.yDim)

        self.statusLbl = tk.Label(self.window, textvariable=self.currentStatus)

        self.startBtn = tk.Button(self.window, text="Start", command=self.start)

        # grid setup
        self.presetLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.presetBox.grid(row=0, column=1, pady=5, sticky="nesw")

        self.xDimLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.xDimE.grid(row=1, column=1, pady=5, sticky="nesw")

        self.yDimLbl.grid(row=2, column=0, pady=5, sticky="e")
        self.yDimE.grid(row=2, column=1, pady=5, sticky="nesw")

        self.statusLbl.grid(row=3, column=0, columnspan=2, sticky="nesw")

        self.startBtn.grid(row=4, column=0, columnspan=2, sticky="nesw")

        # don't quit yet
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # detect choice change
        self.preset.trace("w", self.presetChange)

        # set buttons
        self.xDimE.config(state="disabled")
        self.yDimE.config(state="disabled")
        self.presetBox.config(state="disabled")

        self.autoDetect()

        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.update()

        self.window.mainloop()

    def autoDetect(self):
        global screen_width, screen_height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        print(screen_width, screen_height)
        if self.preset.get() == "Auto":
            self.xDimE.config(state="disable")
            self.yDimE.config(state="disable")
            self.xDim.set(screen_width)
            self.yDim.set(screen_height)
        elif self.preset.get() == "Manual":
            self.xDimE.config(state="normal")
            self.yDimE.config(state="normal")
        else:
            print("UHH")

    def presetChange(self, i, d, c):
        if self.preset.get() == "Auto":
            self.autoDetect()
        elif self.preset.get() == "Manual":
            self.xDimE.config(state="normal")
            self.yDimE.config(state="normal")
        else:
            print("UHH")

    def start(self):  # start it on another thread instead and disable preset changing
        global kListener, mListener
        self.presetBox.config(state="disabled")
        self.startBtn.config(state="disabled")
        kListener = keyboard.Listener(on_press=self.on_press)
        mListener = mouse.Listener(on_move=self.on_move)
        kListener.start()
        mListener.start()
        # Listener that checks if the mouse if on the edge of the screen and move it to the other side,
        # and change the status text to position, pynput, also disable the start button after start and enable stop
        # button

    def stop(self):
        global kListener, mListener
        self.presetBox.config(state="normal")
        self.startBtn.config(state="normal")
        # stop listener, start button allowed, stop button disallowed, escape allows stop

    def on_press(self, key):
        if key == Key.esc:
            self.window.quit()

    def on_move(self, x, y):
        self.currentStatus.set("{0} {1}\n{2} {3}".format(x, y, self.sW.get(), self.sH.get()))
        if x <= 0.5:
            mouse.Controller().move(10000, 0)
        elif self.sW.get() - 1 <= x < self.sW.get():
            mouse.Controller().move(-10000, 0)
        elif y <= 0.5:
            mouse.Controller().move(0, 10000)
        elif self.sH.get() > y >= self.sH.get() - 1:
            mouse.Controller().move(0, -10000)

    def on_closing(self):
        self.window.lift()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop()
            self.window.quit()


if __name__ == "__main__":
    main = tkWin()
else:
    print("no")
