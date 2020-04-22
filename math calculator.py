"""
Math except the software does it and not you
"""
# TODO: Reduce size of the if statement at function line 375 (Calculate)
import math
import statistics
import tkinter as tk


class Math:
    """
    Where math happens
    """

    @staticmethod
    def addition(num, num2):
        """
        Addition
        :param num: Number to add to number
        :param num2: Number to add to other number
        :return: Number added together
        """
        return float(num) + float(num2)

    @staticmethod
    def subtraction(num, num2):
        """
        Subtraction
        :param num: Number subtracted by number 2
        :param num2: Number 2
        :return: Number
        """
        return float(num) - float(num2)

    @staticmethod
    def multiplication(num, num2):
        """
        Multiplication
        :param num: Number multiplied by Number 2
        :param num2: Number 2
        :return: Number
        """
        return float(num) * float(num2)

    @staticmethod
    def division(num, num2):
        """
        Divide
        :param num: Number Divided by Number 2
        :param num2: Number 2
        :return: Number
        """
        return float(num) / float(num2)

    @staticmethod
    def remainder(num, num2):
        """
        Remainder from division
        :param num:
        :param num2:
        :return: Number
        """
        return math.remainder(float(num), float(num2))

    @staticmethod
    def mean(numList):
        """
        Add all and divide by length of list
        :param numList: Number List
        :return: Number
        """
        return float(statistics.mean(numList))

    def MAD(self, numList):
        """
        MAD
        :param numList: Number list
        :return: Number
        """
        tempMean = float(self.mean(numList))  # get mean of list
        tempList = []
        for num in numList:
            if num > tempMean:  # subtract the mean and then number or the other way if its bigger
                tempList.append(float(num - tempMean))
            elif num < tempMean:
                tempList.append(float(tempMean - num))
        tempList.sort()
        return self.mean(tempList)  # get the mean

    @staticmethod
    def power(num, power):
        """
        To the power of
        :param num: Number to the power of number power
        :param power: Number power
        :return: Number
        """
        return math.pow(float(num), float(power))

    @staticmethod
    def square_root(num):
        """
        Square Root
        :param num: Number to square root
        :return: Number
        """
        return math.sqrt(float(num))

    @staticmethod
    def cosine(num):
        """
        Cosine
        :param num: Number to cosine
        :return: Number
        """
        return math.cos(float(num))

    @staticmethod
    def sine(num):
        """
        Sine
        :param num: Number to sine
        :return: Number
        """
        return math.sin(float(num))

    @staticmethod
    def tangent(num):
        """
        Tangent
        :param num: Number
        :return: Number
        """
        return math.tan(float(num))

    @staticmethod
    def median(numList):
        """
        Median
        :param numList: Number List
        :return: Number
        """
        return float(statistics.median(numList))

    def IQR(self, numList):
        """
        IQR (originated from Khan Academy, could be inaccurate in some places)
        :param numList: Number List
        :return: Number
        """
        # main idea:
        # get the lower and higher part of the list of the median
        # change the numbers into a median
        # append everything that's below and above the in between, and do the normal median on both lower and higher
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
            if i < lowerListChoice:
                lowerList.append(numList[i])
            elif i > higherListChoice:
                higherList.append(numList[i])
            elif i == lowerListChoice or i == higherListChoice:
                pass
        lowerList.sort()
        higherList.sort()
        lowerMedian = self.median(lowerList)
        higherMedian = self.median(higherList)
        if lowerMedian > higherMedian:
            return lowerMedian - higherMedian
        elif higherMedian > lowerMedian:
            return higherMedian - lowerMedian

    @staticmethod
    def rounding(num, upDown):
        if upDown.lower() == "up":
            return math.ceil(num)
        elif upDown.lower() == "down":
            return math.floor(num)


class GUI:
    def __init__(self):
        """
        The GUI mainly for people who doesn't know how to
        """
        global numListSaved, allowSave, onTop
        super().__init__()
        numListSaved = []
        allowSave = True
        onTop = False
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
        self.numList = tk.Label(self.window, textvariable=self.varNumList, wraplength=180, justify="center")
        # self.numList = tk.Entry(self.window, textvariable=self.varNumList)
        # self.numList.config(state="disable")

        self.finalLbl = tk.Label(self.window, text="Final answer:")
        self.finalEnt = tk.Label(self.window, textvariable=self.answer, wraplength=180, justify="center")
        # self.finalEnt = tk.Entry(self.window, textvariable=self.answer)
        # self.finalEnt.config(state="disable")

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

        self.calcs.entryconfig(2, state="disabled")
        self.calcs.entryconfig(3, state="disabled")

        self.menubar.add_cascade(label="Math", menu=self.calcs)

        self.window.config(menu=self.menubar)

        # start
        self.window.mainloop()

    def floatingWin(self):
        global onTop
        if onTop:
            self.window.lift()
            self.window.attributes('-topmost', False)
            self.window.update()
            onTop = False
        elif not onTop:
            self.window.lift()
            self.window.attributes('-topmost', True)
            self.window.update()
            onTop = True

    def key_release(self, event):
        """
        When you release a key
        :param event: To detect which key
        :return:
        """
        global allowSave
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
        """
        Change list on GUI
        :return:
        """
        global numListSaved
        self.varNumList.set(numListSaved)

    def clearList(self):
        """
        Clear list on GUI
        :return:
        """
        global numListSaved
        if allowSave:
            numListSaved.clear()
            self.varNumList.set(numListSaved)

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
        numListSaved.clear()
        self.setList()
        self.answer.set("")

        if choice == "Mean" or choice == "MAD" or choice == "Median" or choice == "IQR":
            self.extraNumsState(choice, True, False)
        elif choice == "Power" or choice == "Addition" or choice == "Subtraction" or choice == "Multiplication" or \
                choice == "Division" or choice == "Remainder":
            self.extraNumsState(choice, False, True)
        elif choice == "Square Root" or choice == "Cosine" or choice == "Sine" or choice == "Tangent":
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
            self.numEnt2.config(state="disabled")
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
        """
        Gets sent off to be calculated
        :param numList:
        :return:
        """
        self.setList()
        if numList is None:
            numList = numListSaved
        choice = self.choice.get()
        if choice == "Mean" or choice == "MAD" or choice == "Median" or choice == "IQR":
            if self.numEnt.get() != "" or self.numEnt.get() != "0" or self.numEnt.get() != 0:
                self.saveNum()
        if choice == "Mean":  # i need to somehow reduce this if statement
            self.answer.set(str(Math().mean(numList)))
        elif choice == "MAD":
            self.answer.set(str(Math().MAD(numList)))
        elif choice == "Median":
            self.answer.set(str(Math().median(numList)))
        elif choice == "IQR":
            self.answer.set(str(Math().IQR(numList)))
        elif choice == "Power":
            self.answer.set(str(Math().power(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Square Root":
            self.answer.set(str(Math().square_root(self.numEnt.get())))
        elif choice == "Sine":
            self.answer.set(str(Math().sine(self.numEnt.get())))
        elif choice == "Cosine":
            self.answer.set(str(Math().cosine(self.numEnt.get())))
        elif choice == "Tangent":
            self.answer.set(str(Math().tangent(self.numEnt.get())))
        elif choice == "Addition":
            self.answer.set(str(Math().addition(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Subtraction":
            self.answer.set(str(Math().subtraction(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Multiplication":
            self.answer.set(str(Math().multiplication(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Division":
            self.answer.set(str(Math().division(self.numEnt.get(), self.numEnt2.get())))
        elif choice == "Remainder":
            self.answer.set(str(Math().remainder(self.numEnt.get(), self.numEnt2.get())))
        numListSaved.clear()


if __name__ == '__main__':
    tkWin = GUI()
