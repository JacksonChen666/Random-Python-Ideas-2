#!/usr/bin/python3
# now ineffective because sublime and jetbrain editors have them
import os
import shutil as st
from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring

Tk().withdraw()
replaceThe, fileExtension, directory = None, None, None
while not directory: directory = str(filedialog.askdirectory())
while not fileExtension: fileExtension = askstring("File extension", "What file extension are you looking for")
while not replaceThe: replaceThe = askstring("Replace", "What would you want to replace?")
replaceWith = askstring("Replace With", "What would you want to replace with?")
if replaceWith is None: replaceWith = ""
files = [i for i in os.listdir(directory) if i.endswith(fileExtension)]
if os.path.isdir(os.path.join(directory, "BACKUP")): st.rmtree(os.path.join(directory, "BACKUP"))
os.mkdir(os.path.join(directory, "BACKUP"))
for i in files:
    st.copyfile(os.path.join(directory, i), os.path.join(directory, "BACKUP", i))
    replacedText = open(os.path.join(directory, i)).read().replace(replaceThe, replaceWith)
    open(os.path.join(directory, i), "w").write(replacedText)
