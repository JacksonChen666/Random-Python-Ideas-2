import tkinter as tk


class tkWin:
    def __init__(self):
        super().__init__()
        self.window = tk.Tk()
        self.window.title("Check your tray!")
        self.window.iconify()
        self.window.mainloop()


if __name__ == '__main__':
    main = tkWin()
