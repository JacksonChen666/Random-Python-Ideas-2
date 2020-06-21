from tkinter import *


class Typing:
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing test")
        window_size = (700, 400)
        screen_size = (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.geometry("{}x{}+{}+{}".format(window_size[0], window_size[1], screen_size[0] // 2 - window_size[0]
                                                  // 2, screen_size[1] // 2 - window_size[1] // 2))
        self.texts = Text(self.window)
        self.insert_text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lectus at arcu sagittis consectetur"
            " eu et augue. Etiam efficitur hendrerit nisi, sollicitudin hendrerit enim."
        )
        self.texts.bind("<ButtonPress>", lambda e: "break")
        self.texts.pack(fill=BOTH, expand=1)

        self.input_box = Entry(self.window)
        self.input_box.bind("<Key>", self.verify)
        self.input_box.pack(fill=X)
        self.window.mainloop()

    def verify(self, e):
        trueText = self.texts.get("1.0", END).rstrip("\n")
        userInput = self.input_box.get() + e.char if e.keycode != 8 else self.input_box.get()[:-1]
        print(e)
        if userInput == trueText:
            self.texts.config({"background": "green3"})
        elif trueText.startswith(userInput):
            self.texts.config({"background": "white"})
        else:
            self.texts.config({"background": "red"})

    def insert_text(self, text, loc="end"):
        self.texts.config(state=NORMAL)
        self.texts.insert(loc, text)
        self.texts.config(state=DISABLED)


if __name__ == '__main__':
    tkWin = Typing()
