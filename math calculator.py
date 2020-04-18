import math
import tkinter as tk
from tkinter import messagebox


class Calculations:
    @staticmethod
    def mean(numList):
        tempNum = 0.0
        for num in numList:
            tempNum = float(tempNum) + float(num)
        return float(tempNum) / float(len(numList))

    def MAD(self, numList):
        tempMean = float(self.mean(numList))
        tempList = []
        for num in numList:
            if num > tempMean:
                tempList.append(float(num - tempMean))
            else:
                tempList.append(float(tempMean - num))
        return self.mean(tempList)

    @staticmethod
    def power(num, power):
        return math.pow(float(num), float(power))

    @staticmethod
    def square_root(num):
        return math.sqrt(float(num))

    @staticmethod
    def cosine(num):
        return math.cos(float(num))

    @staticmethod
    def sine(num):
        return math.sin(float(num))

    @staticmethod
    def tangent(num):
        return math.tan(float(num))


class GUI:
    def __init__(self):
        global numListSaved, allowSave
        super().__init__()
        numListSaved = []
        allowSave = True
        self.window = tk.Tk()
        self.window.resizable(0, 0)
        self.window.geometry("+50+60")
        self.window.title("Math Calculator")

        # vars
        self.choice = tk.Variable(self.window, value="Mean")
        self.numVar = tk.Variable(self.window)
        self.numVar2 = tk.Variable(self.window)
        self.answer = tk.Variable(self.window)
        self.varNumList = tk.Variable(self.window)

        # stuff
        self.calcTypeLbl = tk.Label(self.window, text="Type of calculation:")
        self.calcType = tk.OptionMenu(self.window, self.choice, "Cosine", "Sine", "Tangent", "Mean", "MAD", "Power",
                                      "Square Root")

        self.numLbl = tk.Label(self.window, text="Number 1:")
        self.numEnt = tk.Entry(self.window, textvariable=self.numVar)

        self.numLbl2 = tk.Label(self.window, text="Number 2:")
        self.numEnt2 = tk.Entry(self.window, textvariable=self.numVar2)

        self.numListLbl = tk.Label(self.window, text="Nums list:")
        self.numList = tk.Label(self.window, textvariable=self.varNumList, wraplength=200, justify="center")
        # self.numList = tk.Entry(self.window, textvariable=self.varNumList)
        # self.numList.config(state="disable")

        self.finalLbl = tk.Label(self.window, text="Final answer:")
        self.finalEnt = tk.Label(self.window, textvariable=self.answer, wraplength=200, justify="center")
        # self.finalEnt = tk.Entry(self.window, textvariable=self.answer)
        # self.finalEnt.config(state="disable")

        self.saveNumBtn = tk.Button(self.window, text="Save num", command=self.saveNum)
        self.calcBtn = tk.Button(self.window, text="Calculate", command=self.calculate)

        # grid
        self.calcTypeLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.calcType.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        self.numLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.numEnt.grid(row=1, column=1, pady=5, sticky="nesw")

        self.numLbl2.grid(row=2, column=0, pady=5, sticky="e")
        self.numEnt2.grid(row=2, column=1, pady=5, sticky="nesw")

        self.numListLbl.grid(row=3, column=0, pady=5, sticky="e")
        self.numList.grid(row=3, column=1, pady=5, sticky="nesw")

        self.finalLbl.grid(row=4, column=0, pady=5, sticky="e")
        self.finalEnt.grid(row=4, column=1, padx=5, pady=5, sticky="nesw")

        self.saveNumBtn.grid(row=5, column=0, padx=5, pady=5, sticky="nesw")
        self.calcBtn.grid(row=5, column=1, padx=5, pady=5, sticky="nesw")

        # checks and stuff
        self.choice.trace("w", self.choiceCheck)
        self.choiceCheck()
        self.numEnt.bind("<KeyRelease>", self.key_release)
        self.window.bind_all("<KeyRelease>", self.confirm_quit)

        # start
        self.window.mainloop()

    def confirm_quit(self, event):
        if event.char == "":
            self.window.lift()
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.window.quit()

    def key_release(self, event):
        global allowSave
        # print("Key: {0}".format(event.char))
        if event.char == "\n" or event.char == "\r":
            self.calculate()
        if allowSave:
            if event.char == " ":
                self.saveNum()
        print("{0}".format(event.char), end="")

    def setList(self):
        global numListSaved
        self.varNumList.set(numListSaved)

    def choiceCheck(self, i=None, d=None, c=None):
        global numListSaved, allowSave
        choice = self.choice.get()
        self.setList()
        if choice == "Mean":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="disable")
            self.numLbl2.config(text="Save instead")
            self.finalLbl.config(text="Answer (Mean):")
            self.saveNumBtn.config(state="normal")
            allowSave = True
            self.numVar2.set("")
        elif choice == "MAD":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="disable")
            self.numLbl2.config(text="Save instead")
            self.finalLbl.config(text="Answer (MAD):")
            self.saveNumBtn.config(state="normal")
            allowSave = True
            self.numVar2.set("")
        elif choice == "Power":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="normal")
            self.numLbl2.config(text="To the power of:")
            self.finalLbl.config(text="Answer (Power):")
            self.saveNumBtn.config(state="disable")
            allowSave = False
            numListSaved.clear()
            self.setList()
        elif choice == "Square Root":
            self.numLbl.config(text="Number 1:")
            self.numEnt2.config(state="disabled")
            self.numLbl2.config(text="No extra nums")
            self.finalLbl.config(text="Answer (Square Root):")
            self.saveNumBtn.config(state="disable")
            allowSave = False
            numListSaved.clear()
            self.setList()
            self.numVar2.set("")
        elif choice == "Cosine":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="disabled")
            self.numLbl2.config(text="No extra nums")
            self.finalLbl.config(text="Answer (Cosine):")
            self.saveNumBtn.config(state="disable")
            allowSave = False
            numListSaved.clear()
            self.setList()
            self.numVar2.set("")
        elif choice == "Sine":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="disabled")
            self.numLbl2.config(text="No extra nums")
            self.finalLbl.config(text="Answer (Sine):")
            self.saveNumBtn.config(state="disable")
            allowSave = False
            numListSaved.clear()
            self.setList()
            self.numVar2.set("")
        elif choice == "Tangent":
            self.numLbl.config(text="Number:")
            self.numEnt2.config(state="disabled")
            self.numLbl2.config(text="No extra nums")
            self.finalLbl.config(text="Answer (Tangent):")
            self.saveNumBtn.config(state="disable")
            allowSave = False
            numListSaved.clear()
            self.setList()
            self.numVar2.set("")

    def saveNum(self):
        global numListSaved
        try:
            numListSaved.append(float(self.numEnt.get()))
        except ValueError:
            self.numVar.set("")
            return False
        self.numVar.set("")
        self.setList()
        return True

    def calculate(self, numList=None):
        self.setList()
        if numList is None:
            numList = numListSaved
        choice = self.choice.get()
        if choice == "Mean":
            if self.numEnt.get() == "":
                pass
            else:
                self.saveNum()
            self.answer.set(str(Calculations().mean(numList)))
        elif choice == "MAD":
            if self.numEnt.get() == "":
                pass
            else:
                self.saveNum()
            self.answer.set(str(Calculations().MAD(numList)))
        elif choice == "Power":
            self.answer.set(str(Calculations().power(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Square Root":
            self.answer.set(str(Calculations().square_root(self.numEnt.get())))
        elif choice == "Sine":
            self.answer.set(str(Calculations().sine(self.numEnt.get())))
        elif choice == "Cosine":
            self.answer.set(str(Calculations().cosine(self.numEnt.get())))
        elif choice == "Tangent":
            self.answer.set(str(Calculations().tangent(self.numEnt.get())))
        numListSaved.clear()


if __name__ == '__main__':
    tkWin = GUI()
