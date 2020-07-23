import logging.handlers
import statistics
from tkinter import *


def safe_eval(expression):
    safe_expressions = {
        "sum": sum,
        "round": round,
        "max": max,
        "min": min,
        "sort": sorted,
        "sorted": sorted,
        "mean": statistics.mean,
        "median": statistics.median,
    }
    try:
        complied = compile(expression, "<string>", "eval")
    except (SyntaxError,) as err:
        logging.exception("Error: {}".format(err))
        return err
    for name in complied.co_names:
        if name not in safe_expressions:
            raise NameError(f"A unsafe expression '{name}' has been found during evaluation")
    try:
        return eval(complied, {"__builtins__": {}}, safe_expressions)
    except (TypeError,) as err:
        logger.exception("Error: {}".format(err))
        return err


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
        self.helpBtn = Button(self.window, text="Help", command=self.help)
        self.calcBtn = Button(self.window, text="Calculate", command=self.calculate)

        self.numLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.numEnt.grid(row=0, column=1, pady=5)
        self.finalLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.finalEnt.grid(row=1, column=1, pady=5)
        self.helpBtn.grid(row=2, column=0, sticky="nesw")
        self.calcBtn.grid(row=2, column=1, sticky="nesw")

        self.numEnt.bind("<Return>", self.calculate)
        self.window.mainloop()

    def calculate(self, e=None):
        if self.numEnt.get():
            ans = safe_eval(self.numEnt.get())
            self.finalEnt.config(text=ans)

    @staticmethod
    def help():
        hw = Tk()
        hw.title("Help")
        hw.resizable(0, 0)
        Label(hw, text="Usage: function_name((data))\n"
                       "Built-in functions:\n"
                       "sum: Add all the provided numbers\n"
                       "round: Round the numbers\n"
                       "max: Get the max number from the data point\n"
                       "min: Get the min number from the data point\n"
                       "sort/sorted: Sort the data\n"
                       "\n"
                       "Functions:\n"
                       "mean: Get the mean of the data point\n"
                       "median: Get the median of the data point").pack()
        Button(hw, text="Close", command=hw.destroy).pack()
        hw.mainloop()


if __name__ == '__main__':
    logger = logging.getLogger("Calculator")
    logger.setLevel(logging.DEBUG)
    tkWin = GUI()
