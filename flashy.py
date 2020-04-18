import tkinter as tk


class flash:
    def __init__(self):
        super().__init__()
        self.window = tk.Tk()
        self.window.geometry("+50+60")
        self.flashy = tk.Button(self.window, text="I am flash", command=self.flashing)
        self.flashy.pack()
        self.window.mainloop()

    def flashing(self):
        self.flashy.flash()


if __name__ == '__main__':
    winFlash = flash()
