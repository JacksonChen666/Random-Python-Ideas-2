from argparse import ArgumentParser
from random import choice, randint
from threading import Thread
from time import sleep, time
from tkinter import BOTH, DISABLED, END, Entry, Label, NORMAL, Text, Tk, WORD, X

from requests import exceptions, get

font = ("Monospace", 16)
bg = "white"
fg = "black"


class Error(Exception):
    pass


class NoWordsSelected(Error):
    def __init__(self, message="Unable to get words from the minimum length of {} and maximum length of {}."):
        super().__init__(message.format(args.min_len, args.max_len))


class Typing:
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing")
        self.window.configure(bg=bg, highlightbackground=bg)
        self.texts = Text(self.window, font=font, height=20, wrap=WORD, fg=fg, bg=bg)
        self.texts.tag_config("correct", foreground="green3")
        self.texts.tag_config("incorrect", background="red")
        self.texts.insert("1.0", "Loading...")
        self.texts.bind("<ButtonPress>", lambda e: "break")
        self.texts.pack(fill=BOTH, expand=True)

        self.input_box = Entry(self.window, font=font, fg=fg, bg=bg)
        self.input_box.bind("<Key>", self.verify)
        self.input_box.pack(fill=X)

        self.info = Label(self.window, text="WPM: 0\tAccuracy: 100%", bg=bg, fg=fg)
        self.info.pack()

        self.window.update_idletasks()
        sizes = ((self.window.winfo_screenwidth(), self.window.winfo_screenheight()),
                 (self.window.winfo_width(), self.window.winfo_height()))
        self.window.minsize(sizes[1][0], sizes[1][1])
        self.window.geometry("+{}+{}".format(sizes[0][0] // 2 - sizes[1][0] // 2, sizes[0][1] // 2 - sizes[1][1] // 2))
        self.window.update_idletasks()
        self.window.update()

        self.words = None
        try:
            self.words = get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text.splitlines()
        except exceptions.ConnectionError:
            print("Offline. Please connect to a working internet connection to download the words.")
            self.window.quit()
            return
        if args.min_len > len(min(self.words)) or args.max_len < len(max(self.words)):
            self.words = [i for i in self.words if args.max_len >= len(i) >= args.min_len]

        self.window.bind("<Return>", self.new_typing)
        self.start_time, self.uncorrected_errors, self.total_errors = None, 0, 0
        self.new_typing()
        Thread(target=self.intervals, daemon=True).start()
        self.window.mainloop()

    def verify(self, e):
        def end():
            self.input_box.insert("end", e.char)
            self.input_box.config(state=DISABLED)

        te = e.keycode
        print(e)
        if not (te == 8 or te == 13 or e.keysym == "BackSpace") and (te < 32):
            return "break"
        if e.keysym == "BackSpace" and e.state == "Mod1":
            self.texts.delete("1.0", END)
        if self.start_time is None:
            self.start_time = time()
        trueText, userInput = self.texts.get("1.0", END).rstrip(
            "\n"), self.input_box.get() + e.char if te != 8 and e.keysym != "BackSpace" else self.input_box.get()[:-1]
        for tag in self.texts.tag_names():
            self.texts.tag_remove(tag, "1.0", END)
        if userInput == trueText:
            self.texts.tag_add("correct", "1.0", END)
            end()
        elif trueText.startswith(userInput):
            self.input_box.config(background=bg)
            self.texts.tag_add("correct", "1.0", f"1.{len(userInput)}")
        else:
            self.input_box.config(background="red")
            ui2 = userInput
            while not trueText.startswith(ui2):
                ui2 = ui2[:-1]
            lUI2, EFT = len(ui2), len(ui2) + len(userInput[len(ui2):])
            userInput, trueText = userInput[lUI2:EFT], trueText[lUI2:EFT]
            self.texts.tag_add("correct", "1.0", f"1.{lUI2}")
            self.uncorrected_errors = EFT - lUI2
            for i in range(EFT - lUI2):
                i2 = i + lUI2
                try:
                    if userInput[i] == trueText[i]:
                        self.texts.tag_add("correct", f"1.{i2}", f"1.{i2 + 1}")
                        self.uncorrected_errors -= 1
                    else:
                        self.texts.tag_add("incorrect", f"1.{i2}", f"1.{i2 + 1}")
                except IndexError:
                    continue
            trueText = self.texts.get("1.0", END).rstrip("\n")
            userInput = self.input_box.get() + e.char if te != 8 and e.keysym != "BackSpace" else self.input_box.get()[
                                                                                                  :-1]
            if len(userInput) == len(trueText):
                end()

    def intervals(self):
        while True:
            try:
                if self.input_box.cget('state') == NORMAL and self.start_time is not None:
                    self.wpm_and_accuracy()
            except TypeError:
                continue
            sleep(0.25)

    def wpm_and_accuracy(self, e=None):
        # wpm and accuracy: https://www.speedtypingonline.com/typing-equations
        userInputLen = len(self.input_box.get()) if e is None else len(self.input_box.get() + e.char)
        time_apart = (time() - self.start_time) / 60
        try:
            accuracy = (userInputLen - self.uncorrected_errors) / userInputLen * 100
            net_wpm = (userInputLen / 5 - self.uncorrected_errors) / time_apart
        except ZeroDivisionError:
            accuracy, net_wpm = 100, 0
        net_wpm = 0 if net_wpm < 0 else net_wpm
        accuracy = 100 if accuracy > 100 else 0 if accuracy < 0 else accuracy
        self.info.config(text=f"WPM: {int(net_wpm) or 0}\tAccuracy: {int(accuracy) or 100}%")

    def new_typing(self, *_args):
        words = [choice(self.words) for _ in range(randint(args.min, args.max))]
        if not len(words) > 0:
            raise NoWordsSelected(
                f"Unable to get words from the minimum length of {args.min_len} and maximum length of "
                f"{args.max_len}")
        text = " ".join(words)
        self.texts.config(state=NORMAL)
        self.texts.delete("1.0", END)
        self.texts.insert("end", text)
        self.texts.config(state=DISABLED)
        self.input_box.config(state=NORMAL)
        self.input_box.delete(0, END)
        self.input_box.focus_set()
        self.input_box.config(bg=bg)
        self.start_time, self.uncorrected_errors, self.total_errors = None, 0, 0
        self.texts.config(bg=bg)


if __name__ == '__main__':
    parser = ArgumentParser(description="Type random words from the dictionary")
    parser.add_argument("-min", metavar="3", help="Minimum amount of words", type=int, default=3)
    parser.add_argument("-max", metavar="50", help="Maximum amount of words", type=int, default=50)
    parser.add_argument("--max-len", dest="max_len", metavar="100", help="Max length for each word", type=int,
                        default=100 ** 100)
    parser.add_argument("--min-len", dest="min_len", metavar="0", help="Min length for each word", type=int, default=0)
    parser.add_argument("--dark-theme", dest="dark_theme", help="Enable dark theme", action="store_true", default=False)
    args = parser.parse_args()
    if args.min_len > args.max_len:
        args.min_len, args.max_len = args.max_len, args.min_len
    if args.min > args.max:
        args.min, args.max = args.max, args.min
    args.min_len, args.max_len, args.max, args.min = \
        abs(args.min_len), abs(args.max_len), abs(args.max), abs(args.min)
    if args.dark_theme:
        bg = "#121212"
        fg = "#9A9A9A"
    tkWin = Typing()
