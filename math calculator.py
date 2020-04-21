import math
import statistics
import tkinter as tk


class Calculations:
    @staticmethod
    def addition(num, num2):
        return float(num) + float(num2)

    @staticmethod
    def subtraction(num, num2):
        return float(num) - float(num2)

    @staticmethod
    def multiplication(num, num2):
        return float(num) * float(num2)

    @staticmethod
    def division(num, num2):
        return float(num) / float(num2)

    @staticmethod
    def remainder(num, num2):
        return math.remainder(float(num), float(num2))

    @staticmethod
    def mean(numList):
        return float(statistics.mean(numList))

    def MAD(self, numList):
        tempMean = float(self.mean(numList.sort))  # get mean of list
        tempList = []
        for num in numList:
            if num > tempMean:  # subtract the mean and then number or the other way if its bigger
                tempList.append(float(num - tempMean))
            else:
                tempList.append(float(tempMean - num))
        return self.mean(tempList.sort())  # get the mean

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

    @staticmethod
    def median(numList):
        return float(statistics.median(numList))

    def IQR(self, numList):
        mainMedian = float(self.median(numList))  # get the median of whole list
        lowerList = []  # save the lower and higher part of the list into a new lower and higher part of a list
        # separately
        higherList = []
        for i in numList:
            if i < mainMedian:
                lowerList.append(i)
            elif i > mainMedian:
                higherList.append(i)

        lowerMedian = float(self.median(lowerList))  # get the median both the lower and higher part
        higherMedian = float(self.median(higherList))
        if lowerMedian > higherMedian:  # subtract q1 to q3 or q3 to q1 (one must be higher than the other)
            return lowerMedian - higherMedian
        elif lowerMedian < higherMedian:
            return higherMedian - lowerMedian

    @staticmethod
    def rounding(num, mode):
        if mode.lower() == "up":
            return math.ceil(num)
        elif mode.lower() == "down":
            return math.floor(num)


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
        choices = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Remainder', 'Cosine', 'IQR', 'MAD',
                   'Mean', 'Median', 'Power', 'Sine', 'Square Root', 'Tangent']
        choices.sort()
        print(*choices)
        self.calcTypeLbl = tk.Label(self.window, text="Type of calculation:")
        self.calcType = tk.OptionMenu(self.window, self.choice, *choices)

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

        self.clearBtn = tk.Button(self.window, text="Clear List", command=self.clearList)

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

        self.clearBtn.grid(row=6, column=0, padx=5, pady=5, sticky="nesw", columnspan=2)

        # checks and stuff
        self.choice.trace("w", self.choiceCheck)
        self.choiceCheck()
        self.numEnt.bind("<KeyRelease>", self.key_release)

        # menu bar wth
        self.menubar = tk.Menu(self.window)

        self.calcs = tk.Menu(self.menubar, tearoff=0)
        self.calcs.add_command(label="Calculate", command=self.calculate)
        self.calcs.add_separator()

        self.calcs.add_command(label="Save Number", command=self.saveNum)
        self.calcs.add_command(label="Clear List", command=self.clearList)

        self.calcs.entryconfig(2, state="disabled")
        self.calcs.entryconfig(3, state="disabled")

        self.menubar.add_cascade(label="Math", menu=self.calcs)

        self.window.config(menu=self.menubar)

        # start
        self.window.mainloop()

    def key_release(self, event):
        global allowSave
        # print("Key: {0}".format(event.char))
        if event.char == "\n" or event.char == "\r":
            print("\n", end="")
            self.calculate()
        elif event.char == "":
            self.clearList()
        if allowSave:
            if event.char == " ":
                self.saveNum()
        print("{0}".format(event.char), end="")

    def setList(self):
        global numListSaved
        self.varNumList.set(numListSaved)

    def clearList(self):
        global numListSaved
        if allowSave:
            numListSaved.clear()
            self.varNumList.set(numListSaved)

    def choiceCheck(self, i=None, d=None, c=None):
        global numListSaved, allowSave
        choice = self.choice.get()
        numListSaved.clear()
        self.setList()

        if choice == "Mean" or choice == "MAD" or choice == "Median" or choice == "IQR":
            self.extraNumsState(choice, True, False)
        elif choice == "Power" or choice == "Addition" or choice == "Subtraction" or choice == "Multiplication" or \
                choice == "Division" or choice == "Remainder":
            self.extraNumsState(choice, False, True)
        elif choice == "Square Root" or choice == "Cosine" or choice == "Sine" or choice == "Tangent":
            self.extraNumsState(choice, False, False)

    def extraNumsState(self, answerType, saveState, extraNums, num2Lbl="Number 2"):
        global allowSave
        if extraNums:
            self.numEnt2.config(state="normal")
            self.numLbl2.config(text="{0}:".format(num2Lbl))
            self.finalLbl.config(text="Answer ({0}):".format(answerType))
            self.changeSaveState(saveState)
        elif not extraNums:
            self.numEnt2.config(state="disabled")
            self.numLbl2.config(text="No extra nums")
            self.finalLbl.config(text="Answer ({0}):".format(answerType))
            self.numVar2.set("")
            self.changeSaveState(saveState)

    def changeSaveState(self, allowSaving):
        global allowSave
        if allowSaving:
            self.saveNumBtn.config(state="normal")
            allowSave = True
        elif not allowSaving:
            self.saveNumBtn.config(state="disable")
            self.clearList()
            allowSave = False

    def saveNum(self):
        global numListSaved
        if allowSave:
            try:
                numListSaved.append(float(self.numEnt.get()))
            except ValueError:
                self.numVar.set("")
                return False
            self.numVar.set("")
            self.setList()
            return True
        else:
            return False

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
        elif choice == "Median":
            if self.numEnt.get() != "":
                self.saveNum()
            self.answer.set(str(Calculations().median(numList)))
        elif choice == "IQR":
            if self.numEnt.get() != "":
                self.saveNum()
            self.answer.set(str(Calculations().IQR(numList)))
        elif choice == "Addition":
            self.answer.set(str(Calculations().addition(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Subtraction":
            self.answer.set(str(Calculations().subtraction(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Multiplication":
            self.answer.set(str(Calculations().multiplication(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Division":
            self.answer.set(str(Calculations().division(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Remainder":
            self.answer.set(str(Calculations().remainder(self.numEnt.get(), self.numEnt2.get())))
        numListSaved.clear()


if __name__ == '__main__':
    tkWin = GUI()
