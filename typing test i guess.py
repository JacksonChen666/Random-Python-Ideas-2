from tkinter import *


class Typing:
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing test")
        self.successes = 0
        self.failures = 0
        window_size = (700, 400)
        screen_size = (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.geometry("{}x{}+{}+{}".format(window_size[0], window_size[1], screen_size[0] // 2 - window_size[0]
                                                  // 2, screen_size[1] // 2 - window_size[1] // 2))
        self.texts = Text(self.window)
        self.texts.bind("<ButtonPress>", lambda e: "break")
        self.texts.pack(fill=BOTH, expand=True)

        self.input_box = Entry(self.window)
        self.input_box.bind("<Key>", self.verify)
        self.input_box.bind("<Return>", self.new_typing)
        self.input_box.pack(fill=X)

        self.set_text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lectus at arcu sagittis consectetur"
            " eu et augue. Etiam efficitur hendrerit nisi, sollicitudin hendrerit enim."
        )
        self.window.mainloop()

    def verify(self, e):
        trueText = self.texts.get("1.0", END).rstrip("\n")
        userInput = self.input_box.get() + e.char if e.keycode != 8 else self.input_box.get()[:-1]
        print(e)
        if userInput == trueText:
            self.texts.config({"background": "green3"})
            self.new_typing()
        elif trueText.startswith(userInput):
            self.texts.config({"background": "white"})
        else:
            self.texts.config({"background": "red"})
        return userInput == trueText

    def new_typing(self, e=None, text=None):
        # TODO: use the text parameter to take input, or get a random quote from a book online
        # TODO: merge set text or not
        trueText = self.texts.get("1.0", END).rstrip("\n")
        userInput = self.input_box.get()
        if userInput == trueText:
            self.successes += 1
        else:
            self.failures += 1
        self.set_text(text)
        self.texts.config({"background": "white"})

    def set_text(self, text):
        self.input_box.delete(0, END)
        self.texts.config(state=NORMAL)
        self.texts.delete("1.0", END)
        self.texts.insert("end", text)
        self.texts.config(state=DISABLED)


if __name__ == '__main__':
    tkWin = Typing()
