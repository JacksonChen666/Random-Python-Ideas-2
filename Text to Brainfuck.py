#!/usr/bin/env python3
import os
from tkinter import Button, Label, Text, Tk, filedialog, simpledialog

Tk().withdraw()


def displaytext(text):
    root = Tk()

    def updateClipboard(textIn):
        root.clipboard_clear()
        root.clipboard_append(textIn)
        root.update()

    def quitWin(e):
        root.quit()

    updateClipboard(text)
    Label(root, text=f"Brainfuck code (Length: {len(text)}):").pack()
    textbox = Text(root, wrap="word", width=50, height=10)
    textbox.insert("end", str(text))
    textbox.bind("<Key>", lambda e: "break")
    textbox.pack()
    Button(root, text="Exit", command=root.quit).pack()
    root.bind_all("<Return>", quitWin)
    root.mainloop()
    return text


def stringPrompt(title, prompt):
    return simpledialog.askstring(title, prompt)


def filePrompt(title):
    return filedialog.askopenfilename(initialdir=os.getcwd(),
                                      title=title,
                                      filetypes=[('text files', '.txt'), ('all files', '.*')])


def minifiedASCII():
    """
    put all required ascii codes in memory without duplicates
    requires the length of minified ascii codes (no duplicates)
    :return: Generated code
    """
    code = ">"
    for i in minimizedASCIILetters: code += "+" * i + ">"
    code = code[:-1]  # trailing move
    code += "[<]>"
    pointer = 0  # "simulate" pointer
    for i in ASCIILetters:
        indexes = minimizedASCIILetters.index(i)
        code = code + ">" * (indexes - pointer) if indexes > pointer else \
            code + "<" * (pointer - indexes) if indexes < pointer else code
        pointer = indexes
        code += "."
    return code


def plusMinusOnly():
    """
    adds is current number is too small, and the opposite if too big, then print.
    requires only 1 spot of memory
    :return: Generated code
    """
    cNum, code = 0, ""
    for i in ASCIILetters:
        if cNum < i:
            code += "+" * (i - cNum)
        elif cNum > i:
            code += "-" * (cNum - i)
        cNum = i
        code += "."
    return code


def plusMoveOnly():
    """
    get all ascii code in order
    increment until reached the desired ascii code
    repeat for the rest
    go back to start (0) then start printing it all
    requires the length of text of memory
    :return: Generated code
    """
    code = ">"
    for i in ASCIILetters:
        code += "+" * i
        code += ">"
    code = code[:-1]  # trailing move
    code += "[<]>[.>]"
    return code


if __name__ == '__main__':
    inputs = stringPrompt("Convert to Brainfuck", "What would you like to convert to Brainfuck?")
    if not inputs: exit(1)
    ASCIILetters, minimizedASCIILetters = list(bytes(inputs, encoding='utf8')), sorted(
        list(dict.fromkeys(bytes(inputs, encoding="utf8"))))
    modes = [minifiedASCII, plusMoveOnly, plusMinusOnly]
    output = [fun() for fun in modes]
    smallest = 100 ** 100
    output2 = output.copy()
    for p in output2:
        if smallest > len(p):
            smallest = len(p)
            output = p
    print(f"ASCII: {ASCIILetters}\n"
          f"ASCII minified: {minimizedASCIILetters}")
    displaytext(output)
