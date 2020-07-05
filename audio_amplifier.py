import logging
import multiprocessing as mp
import os

from pydub import AudioSegment

log = logging.getLogger("pydub.converter")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def amplify(fileName, fileNameOut=None, ampLevel=10000, ampToOriginal=False, start=None, end=None, export=False):
    if export and not fileNameOut and type(fileName) == str:
        fileNameOut = f"{fileName.rpartition('.')[0]}-2.{fileName.rpartition('.')[2]}"
    original = AudioSegment.from_file(fileName) if type(fileName) == str else fileName

    def timeToMS(timeIn):
        """how it works:
        take the hours, turn it into minutes and add the minutes
        take the minutes, turn it into seconds and add the seconds
        take the seconds, turn it into milliseconds"""
        # format: (Hours, Minutes, Seconds, Milliseconds) (its a tuple, or a list)
        if timeIn is not None and len(timeIn) == 4: return int(
            ((timeIn[0] * 60 + timeIn[1]) * 60 + timeIn[2]) * 1000 + timeIn[3])
        return

    def cutAudio(inAudio, starting=None, ending=None):
        # cutting audio: https://gist.github.com/gchavez2/53148cdf7490ad62699385791816b1ea
        starting = timeToMS(starting)
        ending = timeToMS(ending)
        return inAudio[starting:ending], starting, ending

    def ampUp(inAudio, ampLevels, starting=None, ending=None):
        if starting is not None: return partlyAmpUp(inAudio, ampLevels, starting, ending)
        while True:
            try:
                return inAudio.apply_gain(ampLevels), ampLevels
            except OverflowError:
                ampLevels -= 1
                if ampLevels <= -1: raise ValueError(
                    f"Audio level has reached -1 or below, making it impossible to amplify. Level: {ampLevel}")

    def partlyAmpUp(inAudio, ampLevels, starting=None, ending=None):
        cut, starting, ending = cutAudio(inAudio, starting, ending)
        cut, ampLevels = ampUp(cut, ampLevels)
        if ending is None: return inAudio[:starting] + cut, ampLevels  # without ending
        return inAudio[:starting] + cut + inAudio[ending:], ampLevels  # with ending

    def ampDown(inAudio, oAudio):
        return inAudio if not ampToOriginal else inAudio.apply_gain(oAudio.dBFS - inAudio.dBFS)

    final, ampLevel = ampUp(original, ampLevel, start, end)
    final = ampDown(final, original)
    if export: final.export(fileNameOut)
    return {
        "original": original,
        "final": final,
        "amp level": ampLevel
    }


def _from_prompt(directory, fileFormat, audioLevel=10000, ampDownOriginal=False):
    os.chdir(directory)
    files = [os.path.join(root, i) for root, subs, file in os.walk("./") for i in file if i.endswith("." + fileFormat)]
    print(files)
    with mp.Pool(processes=mp.cpu_count() * 2) as pool:
        multiple_results = [
            pool.apply_async(amplify, (i, i, audioLevel, ampDownOriginal, None, None, True)) for i in files
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
    _from_prompt(uDir, fFormat, aLvl, aBTOL)


"""
aa.amplify(aa.amplify(aa.amplify("ltt.mkv", start=(0, 1, 45.5, 0), end=(0, 1, 45.5 + 30, 0))["final"], start=(0, 2,
30.5, 0), end=(0, 2, 30.5 + 30, 0))["final"], start=(0, 4, 0.5, 0), end=(0, 4, 0.5 + 30, 0))["final"].export("L.mkv")
"""
