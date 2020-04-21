import tkinter as tk


class Main():
    def __init__(self):
        super().__init__()
        # main stuff
        self.root = tk.Tk()
        self.root.geometry("+50+60")
        self.root.title("a title")
        # vars
        self.something = tk.Variable(self.root, value="enter text")
        self.notTheSame = tk.Variable(self.root, value="enterer text")
        self.buttonText = tk.Variable(self.root, value="button")
        # screen stuff
        self.labels = tk.Label(self.root, text="hi")
        self.entries = tk.Entry(self.root, textvariable=self.something)
        self.moreLabels = tk.Label(self.root, text="some kind of very long text")
        self.moreEntries = tk.Entry(self.root, textvariable=self.notTheSame)
        self.buttons = tk.Button(self.root, textvariable=self.buttonText, command=self.idot)

        self.menuBar = tk.Menu(self.root)
        self.idot = tk.Menu(self.menuBar, tearoff=0)
        self.idot.add_command(label="idot buton", command=self.idot)
        self.menuBar.add_cascade(label="idot", menu=self.idot)
        self.root.config(menu=self.menuBar)
        # setup
        self.labels.grid(row=0, column=0, sticky="e")
        self.entries.grid(row=0, column=1)
        self.moreLabels.grid(row=1, column=0, sticky="e")
        self.moreEntries.grid(row=1, column=1)
        self.buttons.grid(row=2, column=0, columnspan=2, sticky="nesw")
        # Be on top of everything
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.update()

        # start
        self.root.mainloop()

    def idot(self):
        if self.buttonText.get() == "button":
            self.buttonText.set("lmao idot, dis button is stoopid")
        elif self.buttonText.get() == "lmao idot, dis button is stoopid":
            self.buttonText.set("can you stop m8")
        elif self.buttonText.get() == "can you stop m8":
            self.buttonText.set("im warning you, im going to destroy myself if you continue")
        elif self.buttonText.get() == "im warning you, im going to destroy myself if you continue":
            self.buttonText.set("don't tell me i didn't warn you!!!!!!!!!!!!")
        elif self.buttonText.get() == "don't tell me i didn't warn you!!!!!!!!!!!!":
            self.root.destroy()
        else:
            self.buttonText.set("wtf")


if __name__ == '__main__':
    tkWin = Main()
else:
    print("no module thx")
