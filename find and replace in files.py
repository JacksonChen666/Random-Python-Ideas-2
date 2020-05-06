#!/usr/bin/python3
# this is used for my website, actually, because i have to constantly do the same thing over and over again (change nav
# menu icons or copy and paste)
import os, shutil as st
from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring
from platform import system
Tk().withdraw()
replaceThe, fileExtension, directory = False, False, False
while not directory: directory = str(filedialog.askdirectory())
while not fileExtension: fileExtension = askstring("File extension", "What file extension are you looking for")
while not replaceThe: replaceThe = askstring("Replace", "What would you want to replace?")
replaceWith = askstring("Replace With", "What would you want to replace with?")
if system() == "Darwin" or system() == "Linux": directory += "/"
elif system() == "Windows": directory += "\\"
files = [i for i in os.listdir(directory) if i.endswith(fileExtension)]
try: os.mkdir(directory + "BACKUP")
except FileExistsError:
    st.rmtree(directory + "BACKUP")
    os.mkdir(directory + "BACKUP")
for i in files:
    st.copyfile(directory + i, directory + "BACKUP/" + i)
    with open(directory + i) as w: text = w.read().replace(replaceThe, replaceWith)
    with open(directory + i, "w") as q: q.write(text)
