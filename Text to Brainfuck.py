#!/usr/bin/python3
import os
from tkinter import Button, IntVar, Label, Radiobutton, Text, Tk, filedialog, simpledialog
import time

Tk().withdraw()


def ask_multiple_choice_question(prompt, options):
    root = Tk()
    if prompt:
        Label(root, text=prompt).pack()
    v = IntVar()
    for i, option in enumerate(options):
        Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
    Button(text="Submit", command=root.destroy).pack()
    root.mainloop()
    if v.get() == 0: return None
    return options[v.get()]


def displaytext(text):
    root = Tk()
    Label(root, text="Brainfuck code:").pack()
    textbox = Text(root, wrap="word", width=30, height=20)
    textbox.insert(str(text), "1.0", "1.0")
    textbox.pack()
    root.mainloop()
    return text


def stringprompt(title, prompt):
    answer = simpledialog.askstring(title, prompt)
    return answer


def fileprompt(title):
    file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                      title=title,
                                      filetypes=[('text files', '.txt'), ('all files', '.*')])
    return file


def plusMinusOnly(text):
    asciiLetters = convertToASCII(text)
    cNum = 0
    code = ""
    for i in asciiLetters:
        if cNum < i:
            e = i - cNum
            cNum += e
            for r in range(e):
                code += "+"
        elif cNum > i:
            e = cNum - i
            cNum -= e
            for r in range(e):
                code += "-"
        code += "."
    print("ASCII:\n{}\nBrainfuck code:\nSTART-OF-FILE\n{}\nEND-OF-FILE".format(asciiLetters, code))
    return code


def withLoops(text):
    asciiLetters = convertToASCII(text)
    cNum = 0
    code = ''
    for i in range(10):
        pass
    return code


def convertToASCII(text):
    return list(bytes(text, encoding='utf8'))


if __name__ == '__main__':
    inputs = stringprompt("Convert to Brainfuck", "What would you like to convert to Brainfuck?")
    # result = ask_multiple_choice_question(
    #     "How would you like to convert?",
    #     ["Using + and - only"]
    # )
    output2 = plusMinusOnly(inputs)
    # displaytext(output)
