#!/usr/bin/env python3
import os
from tkinter import Button, IntVar, Label, Radiobutton, Text, Tk, filedialog, simpledialog

Tk().withdraw()


def ask_multiple_choice_question(prompt, options):
    root = Tk()
    if prompt: Label(root, text=prompt).pack()
    v = IntVar()
    for i, option in enumerate(options): Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
    Button(text="Submit", command=root.destroy).pack()
    root.mainloop()
    if v.get() == 0: return None
    return options[v.get()]


def displaytext(text, copyToClipboard=False):
    root = Tk()
    if copyToClipboard:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        Label(root, text="(Copied to Clipboard)\nBrainfuck code:").pack()
    else: Label(root, text="Brainfuck code:").pack()
    textbox = Text(root, wrap="word", width=50, height=10)
    textbox.insert("end", str(text))
    textbox.bind("<Key>", lambda e: "break")
    textbox.pack()
    Button(root, text="Exit", command=root.quit).pack()
    root.mainloop()
    return text


def stringprompt(title, prompt):
    answer = simpledialog.askstring(title, prompt)
    return answer


def fileprompt(title):
    file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                      title=title,
                                      filetypes=[
                                          ('text files', '.txt'),
                                          ('all files', '.*')
                                      ])
    return file


def plusMinusOnly(text):
    ASCIILetters, minimizedASCIILetters, cNum, code = convertToASCII(text), convertToMinimisedASCII(text), 0, ""
    for i in ASCIILetters:
        if cNum < i:
            e = i - cNum
            cNum += e
            for r in range(e): code += "+"
        elif cNum > i:
            e = cNum - i
            cNum -= e
            for r in range(e): code += "-"
        code += "."
    code += "[-]"
    print("ASCII:\n{}\nASCII modified: {}\nBrainfuck code:\nSTART-OF-FILE\n{}\nEND-OF-FILE".format(ASCIILetters,
                                                                                                   minimizedASCIILetters,
                                                                                                   code))
    return code


def withLoops(text):
    asciiLetters, minimizedASCIILetters, cNum, listNums, listNums2, code = convertToASCII(text), convertToMinimisedASCII(
        text), 0, [], [], ''
    print(asciiLetters)
    for i in asciiLetters:
        # yes use loops, but make sure to emulate the way it's done, and round up or down to 10ths and make a normal and doing it list
        if cNum < i: pass
        elif cNum > i: pass
        code += "."
    print("ASCII:\n{}\nASCII modified: {}\nBrainfuck code:\nSTART-OF-FILE\n{}\nEND-OF-FILE".format(ASCIILetters,
                                                                                                   minimizedASCIILetters,
                                                                                                   code))
    print("Debug:\n{}\n{}".format(listNums, listNums2))
    return code


def convertToASCII(text):
    return list(bytes(text, encoding='utf8'))


def convertToMinimisedASCII(text):
    return sorted(list(dict.fromkeys(bytes(text, encoding="utf8"))))


if __name__ == '__main__':
    inputs = stringprompt("Convert to Brainfuck", "What would you like to convert to Brainfuck?")
    # result = ask_multiple_choice_question(
    #     "How would you like to convert?",
    #     ["Using + and - only"]
    # )
    output = plusMinusOnly(inputs)
    displaytext(output, True)
