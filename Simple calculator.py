#!/usr/bin/env python3
from tkinter import *

def safe_eval(expression):
    safe_expressions = {
        "sum": sum,
        "round": round,
        "max": max,
        "min": min,
        "sorted": sorted,
    }
    complied = compile(expression, "<string>", "eval")
    for name in complied.co_names:
        if name not in safe_expressions:
            raise NameError(f"A unsafe expression '{name}' has been found during evaluation")
    return eval(complied, {"__builtins__": {}}, safe_expressions)


class GUI:
    # get caller:
    # print sys._getframe().f_back.f_code.co_name
    # print('caller name:' + stack()[1][3])
    def __init__(self):
        if sys._getframe().f_back.f_code.co_name != "<module>": return
        self.window = Tk()
        self.window.resizable(0, 0)
        self.window.title("Math Calculator")

        self.numLbl = Label(self.window, text="Math:")
        self.numEnt = Entry(self.window)
        self.finalLbl = Label(self.window, text="Answer:")
        self.finalEnt = Label(self.window, wraplength=180, justify="center")
        self.calcBtn = Button(self.window, text="Calculate", command=self.calculate)

        self.numLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.numEnt.grid(row=0, column=1, pady=5)
        self.finalLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.finalEnt.grid(row=1, column=1, pady=5)
        self.calcBtn.grid(row=2, column=0, sticky="nesw", columnspan=2)

        self.numEnt.bind("<Return>", self.calculate)
        self.window.mainloop()

    def calculate(self, e):
        if self.numEnt.get():
            ans = safe_eval(self.numEnt.get())
            self.finalEnt.config(text=ans)


if __name__ == '__main__': tkWin = GUI()
