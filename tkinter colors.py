from tkinter import *


class Colors:
    def __init__(self):
        self.window = Tk()
        self.window.title("Colors wow")
        win_size = (200, 100)
        scr_size = (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.geometry(f"{win_size[0]}x{win_size[1]}+{scr_size[0] // 2 - win_size[0] // 2}+{scr_size[1] // 2 - win_size[1] // 2}")
        self.entry = Entry(self.window)
        self.entry.pack(fill=BOTH, expand=1)
        self.entry.bind("<Key>", self.change_color)
        self.window.mainloop()

    def change_color(self, e):
        try:
            self.entry.config({"background": self.entry.get() + e.char})
        except:
            self.entry.config({"background": "white"})


if __name__ == '__main__':
    tkWin = Colors()