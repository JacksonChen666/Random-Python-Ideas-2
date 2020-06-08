"""
Math except the software does it and not you
"""
import math
import re
import statistics
import tkinter as tk

numListSaved = []


class GUIAndMath:
    global numListSaved

    def __init__(self):
        """
        The GUI mainly for people who doesn't know how to
        """
        global numListSaved, allowSave, onTop, choices
        super().__init__()
        allowSave = True
        onTop = False
        self.window = tk.Tk()
        self.window.resizable(0, 0)
        self.window.geometry("+50+60")
        self.window.title("Math Calculator")

        # vars
        self.numVar = tk.Variable(self.window)
        self.numVar2 = tk.Variable(self.window)
        self.answer = tk.Variable(self.window)
        self.varNumList = tk.Variable(self.window)

        # stuff
        choices = ["Addition", "Cosine", "Division", "IQR", "MAD", "Mean", "Median", "Multiplication", "Power",
                   "Remainder", "Sine", "Square Root", "Subtraction", "Tangent"]  # please no change or break
        choices.sort()
        print(*choices)
        print(len(choices))
        self.choice = tk.Variable(self.window, value=choices[0])
        self.calcTypeLbl = tk.Label(self.window, text="Type of calculation:")
        self.calcType = tk.OptionMenu(self.window, self.choice, *choices)

        self.numLbl = tk.Label(self.window, text="Number 1:")
        self.numEnt = tk.Entry(self.window, textvariable=self.numVar)

        self.numLbl2 = tk.Label(self.window, text="Number 2:")
        self.numEnt2 = tk.Entry(self.window, textvariable=self.numVar2)

        self.numListLbl = tk.Label(self.window, text="Nums list:")
        self.numList = tk.Label(self.window, textvariable=self.varNumList, wraplength=180, justify="center")

        self.finalLbl = tk.Label(self.window, text="Final answer:")
        self.finalEnt = tk.Label(self.window, textvariable=self.answer, wraplength=180, justify="center")

        self.saveNumBtn = tk.Button(self.window, text="Save num", command=self.saveNum)
        self.calcBtn = tk.Button(self.window, text="Calculate", command=self.calculate)

        self.clearBtn = tk.Button(self.window, text="Clear List", command=self.clearList)

        self.onTopBtn = tk.Button(self.window, text="Floating window", command=self.floatingWin)

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

        self.onTopBtn.grid(row=6, column=0, padx=5, pady=5, sticky="nesw", columnspan=1)
        self.clearBtn.grid(row=6, column=1, padx=5, pady=5, sticky="nesw", columnspan=1)

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

        self.calcs.entryconfig(2, state="isDisabled")
        self.calcs.entryconfig(3, state="isDisabled")

        self.menubar.add_cascade(label="Math", menu=self.calcs)

        self.window.config(menu=self.menubar)

        # start
        self.window.mainloop()

    def floatingWin(self):
        global onTop
        self.window.lift()
        onTop = not onTop
        self.window.attributes('-topmost', onTop)
        self.window.update()

    def validation(self, text, setting):
        if not re.search("\d+|\d*\.\d+", text):
            setting.set("")
            self.setList()
            return False

    def key_release(self, event):
        """
        When you release a key
        :param event: To detect which key
        :return:
        """
        global allowSave
        self.validation(self.numEnt.get(), self.numVar)
        self.validation(self.numEnt2.get(), self.numVar2)
        if re.search("[\n|\r]", event.char):
            print("\n", end="")
            self.calculate()
        elif event.char == "":
            self.clearList()
        if allowSave:
            if event.char == " ": self.saveNum()
        print("{0}".format(event.char), end="")

    def setList(self):
        """
        Change list on GUI
        :return:
        """
        global numListSaved
        self.varNumList.set(self.numListSaved)

    def clearList(self):
        """
        Clear list on GUI
        :return:
        """
        global numListSaved
        if allowSave:
            self.numListSaved.clear()
            self.varNumList.set(self.numListSaved)

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def choiceCheck(self, i=None, d=None, c=None):
        """
        Check choices and stuff
        :param i: I
        :param d: DON'T
        :param c: CARE
        :return:
        """
        global numListSaved, allowSave
        choice = self.choice.get()
        self.numListSaved.clear()
        self.setList()
        self.answer.set("")

        if re.search("Mean|MAD|Median|IQR", choice):
            self.extraNumsState(choice, True, False)
        elif re.search("Power|Addition|Subtraction|Multiplication|Division|Remainder", choice):
            self.extraNumsState(choice, False, True)
        elif re.search("Square Root|Cosine|Sine|Tangent", choice):
            self.extraNumsState(choice, False, False)

    def extraNumsState(self, answerType, saveState, extraNums, num1Lbl="Number 1", num2Lbl="Number 2"):
        """
        Allow extra numbers. Or not. I don't care.
        :param answerType: What is the answer?
        :param saveState: Is saving allowed in this mode?
        :param extraNums: Is 2 numbers required?
        :param num1Lbl: What should the first number label be called?
        :param num2Lbl: What should the second number label be called?
        :return:
        """
        global allowSave
        if extraNums:
            self.numEnt2.config(state="normal")
            self.numLbl2.config(text="{0}:".format(num2Lbl))
        elif not extraNums:
            self.numEnt2.config(state="isDisabled")
            self.numLbl2.config(text="No extra nums")
            self.numVar2.set("")
        self.numLbl.config(text="{0}:".format(num1Lbl))
        self.finalLbl.config(text="Answer ({0}):".format(answerType))
        self.changeSaveState(saveState)

    def changeSaveState(self, allowSaving):
        """
        If saving is allowed or not
        :param allowSaving: if saving is allowed or not
        :return:
        """
        global allowSave
        if allowSaving:
            self.saveNumBtn.config(state="normal")
            allowSave = True
        elif not allowSaving:
            self.saveNumBtn.config(state="disable")
            self.clearList()
            allowSave = False

    def saveNum(self):
        """
        Save the number into a list
        :return:
        """
        global numListSaved
        if allowSave and self.numEnt != "" and self.numEnt2 != "":
            try:
                self.numListSaved.append(float(self.numEnt.get()))
            except ValueError:
                self.numVar.set("")
                return False
            self.numVar.set("")
            self.setList()
            return True
        else:
            return False

    def calculate(self):
        """
        Gets sent off to be calculated
        :return:
        """
        global choices
        self.setList()
        choice = self.choice.get()
        choicesThing = [self.addition, self.cosine, self.division, self.IQR, self.MAD, self.mean, self.median,
                        self.multiplication, self.power, self.remainder, self.sine, self.square_root,
                        self.subtraction, self.tangent]
        if re.search("Mean|MAD|Median|IQR", choice):
            if self.numEnt.get() != "" or self.numEnt.get() != "0" or self.numEnt.get() != 0: self.saveNum()
        for i in range(len(choices)):
            if choice == choices[i]:
                self.answer.set(choicesThing[i]())
                break
        self.numListSaved.clear()

    # Math from now on

    def addition(self, num=None, num2=None):
        """
        Addition
        :param num: Number to add to number
        :param num2: Number to add to other number
        :return: Number added together
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return float(num) + float(num2)

    def subtraction(self, num=None, num2=None):
        """
        Subtraction
        :param num: Number subtracted by number 2
        :param num2: Number 2
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return float(num) - float(num2)

    def multiplication(self, num=None, num2=None):
        """
        Multiplication
        :param num: Number multiplied by Number 2
        :param num2: Number 2
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return float(num) * float(num2)

    def division(self, num=None, num2=None):
        """
        Divide
        :param num: Number Divided by Number 2
        :param num2: Number 2
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return float(num) / float(num2)

    def remainder(self, num=None, num2=None):
        """
        Remainder from division
        :param num:
        :param num2:
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return math.remainder(float(num), float(num2))

    def mean(self, numList=None):
        """
        Add all and divide by length of list
        :param numList: Number List
        :return: Number
        """
        if numList is None: numList = self.numListSaved
        # return float(statistics.mean(numList))
        return sum(numList) / len(numList)

    def MAD(self, numList=None):
        """
        MAD
        :param numList: Number list
        :return: Number
        """
        if numList is None: numList = self.numListSaved
        tempMean = float(self.mean(numList))  # get mean of list
        tempList = []
        for num in numList:
            # tempList.append(float(num - tempMean) if num > tempMean else float(tempMean - num))
            if num > tempMean:
                tempList.append(float(num - tempMean))  # subtract the mean and then number or the
            # other way if its bigger
            elif num < tempMean:
                tempList.append(float(tempMean - num))
        tempList.sort()
        return self.mean(tempList)  # get the mean

    def power(self, num=None, num2=None):
        """
        To the power of
        :param num: Number to the power of number power
        :param num2: Number power
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        if num2 is None: num2 = self.numEnt2.get()
        return math.pow(float(num), float(num2))

    def square_root(self, num=None):
        """
        Square Root
        :param num: Number to square root
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        return math.sqrt(float(num))

    def cosine(self, num=None):
        """
        Cosine
        :param num: Number to cosine
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        return math.cos(float(num))

    def sine(self, num=None):
        """
        Sine
        :param num: Number to sine
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        return math.sin(float(num))

    def tangent(self, num=None):
        """
        Tangent
        :param num: Number
        :return: Number
        """
        if num is None: num = self.numEnt.get()
        return math.tan(float(num))

    def median(self, numList=None):
        """
        Median
        :param numList: Number List
        :return: Number
        """
        if numList is None: numList = self.numListSaved
        return float(statistics.median(numList))

    def IQR(self, numList=None):
        """
        IQR (originated from Khan Academy, could be inaccurate in some places)
        :param numList: Number List
        :return: Number
        """
        # main idea:
        # get the lower and higher part of the list of the median
        # change the numbers into a median
        # append everything that's below and above the in between, and do the normal median on both lower and higher
        if numList is None: numList = self.numListSaved
        numList.sort()
        if (len(numList) % 2) == 0:
            lowerListChoice = self.rounding(len(numList) / 2 - 1, "down")
            higherListChoice = self.rounding(len(numList) / 2, "up")
        else:
            lowerListChoice = self.rounding(len(numList) / 2, "down")
            higherListChoice = self.rounding(len(numList) / 2 - 1, "up")

        lowerList = []
        higherList = []
        for i in range(len(numList)):
            # cannot ignore middle numbers
            if i <= lowerListChoice:
                lowerList.append(numList[i])
            elif i >= higherListChoice:
                higherList.append(numList[i])
        lowerList.sort()
        higherList.sort()
        lowerMedian = self.median(lowerList)
        higherMedian = self.median(higherList)
        # return lowerMedian - higherMedian if lowerMedian > higherMedian else higherMedian - lowerMedian
        if lowerMedian > higherMedian:
            return lowerMedian - higherMedian
        elif higherMedian > lowerMedian:
            return higherMedian - lowerMedian

    def rounding(self, num=None, upDown=None):
        if num is None: num = self.numEnt.get()
        if upDown.lower() == "up":
            return math.ceil(num)
        elif upDown.lower() == "down":
            return math.floor(num)
        elif upDown is None:
            return round(num)


if __name__ == '__main__':
    tkWin = GUIAndMath()
