#!/usr/bin/env python3
import logging
import multiprocessing as mp
import os

from pydub import AudioSegment

log = logging.getLogger("pydub.converter")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def amplify(fileName: str, formatIn=None, fileNameOut=None, ampLevel=10000, ampToOriginal=False):
    # filename must contain file format to be precise of the files
    if not formatIn: formatIn = fileName.rpartition(".")[2]
    audio = AudioSegment.from_file(fileName, formatIn)
    if not fileNameOut: fileNameOut = f"{fileName.rpartition('.')[0]}-2.{formatIn}"
    while True:
        try:
            lAudio = audio.apply_gain(ampLevel)
            break
        except OverflowError:
            ampLevel = ampLevel - 1 if ampLevel > 0 else -1
            if ampLevel <= -1: raise ValueError(f"Audio level has reached -1 or below, making it impossible to amplify. {ampLevel}")
    final = lAudio if not ampToOriginal else lAudio.apply_gain(audio.dBFS - lAudio.dBFS)
    final.export(fileNameOut, format=formatIn)
    return {
        "original audio": audio,
        "new audio": final,
        "amp level": ampLevel
    }


def from_prompt(directory, fileFormat, audioLevel=10000, amplifyBackToOriginalLevel=False):
    os.chdir(directory)
    files = [os.path.join(root, i) for root, subs, file in os.walk("./") for i in file if i.endswith("." + fileFormat)]
    print(files)
    with mp.Pool(processes=mp.cpu_count() * 2) as pool:
        multiple_results = [
            pool.apply_async(amplify, (i, fileFormat, i, audioLevel, amplifyBackToOriginalLevel)) for i in files
        ]
        print([res.get() for res in multiple_results])
    print("Done!")


if __name__ == '__main__':
    from tkinter import filedialog, messagebox, Tk, simpledialog

    Tk().withdraw()
    uDir = filedialog.askdirectory(message="Select a folder to process audio on", initialdir=os.getcwd(),
                                   mustexist=True)
    if not uDir: exit(0)
    fFormat = str(simpledialog.askstring("File Format", "What is your main file format?")).strip(".")
    if not fFormat: exit(0)
    aLvl = simpledialog.askinteger("Loudness", "How much louder do you want it to be?")
    if not aLvl: exit(0)
    aBTOL = messagebox.askyesno("Revert back to original level",
                                "Would you like to revert the audio back to original level after amplifying? ("
                                "excludes un-clipping)")
    from_prompt(uDir, fFormat, aLvl, aBTOL)
