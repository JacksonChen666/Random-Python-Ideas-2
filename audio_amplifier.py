#!/usr/bin/env python3
import logging
import multiprocessing as mp
import os

from pydub import AudioSegment

l = logging.getLogger("pydub.converter")
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())


def set_loudness(sound, target_dBFS):
    loudness_difference = target_dBFS - sound.dBFS
    return sound.apply_gain(loudness_difference)


def amplify(fileName: str, fileFormat: str = None, fileNameOut: str = None, audioLevel: int = 50,
            amplifyToOriginal: bool = True):
    # filename must contain file format to be precise of the files
    audio = AudioSegment.from_file(fileName, fileFormat)
    if not fileFormat: fileFormat = fileName.rpartition(".")[2]
    if not fileNameOut: fileNameOut = f"{fileName.rpartition('.')[0]}-2.{fileFormat}"
    while True:
        try:
            lAudio = audio + audioLevel
            break
        except OverflowError:
            if audioLevel > 0: audioLevel -= 1
            else: raise ValueError(f"Audio level has reached 0 or below, making it impossible to amplify. {audioLevel}")
    final = lAudio if not amplifyToOriginal else set_loudness(lAudio, audio.dBFS)
    final.export(fileNameOut, format=fileFormat)
    return final

def main(directory, fileFormat, audioLevel=50, amplifyBackToOriginalLevel=True):
    os.chdir(directory)
    files = [os.path.join(root, i) for root, subs, file in os.walk("./") for i in file if i.endswith("." + fileFormat)]
    print(files)
    with mp.Pool(processes=mp.cpu_count() * 2) as pool:
        multiple_results = [pool.apply_async(amplify, (i, fileFormat, i, audioLevel, amplifyBackToOriginalLevel,)) for i in
                            files]
        print([res.get() for res in multiple_results])


if __name__ == '__main__':
    from tkinter import filedialog, messagebox, Tk, simpledialog
    Tk().withdraw()
    uDir = filedialog.askdirectory(message="Select a folder to process audio on", initialdir=os.getcwd(), mustexist=True)
    if not uDir: exit(0)
    fFormat = str(simpledialog.askstring("File Format", "What is your main file format?")).strip(".")
    if not fFormat: exit(0)
    aLvl = simpledialog.askinteger("Loudness", "How much louder do you want it to be?")
    if aLvl is None: exit(0)
    aBTOL = messagebox.askyesno("Revert back to original level", "Would you like to revert the audio back to original level after amplifying? (excludes unclipping)")
    main(uDir, fFormat, aLvl, aBTOL)
