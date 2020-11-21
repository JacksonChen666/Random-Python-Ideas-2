"""
This program takes a folder of videos, pick a random spot, and then just combine it into a videosEnt and done
"""
import logging
import os
import threading
import tkinter as tk
from collections import Counter
from os import listdir, path
from random import randint, shuffle, uniform
from tkinter import filedialog, messagebox

import ffmpeg


class OptionDialog(tk.Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """

    def __init__(self, parent, title, question, options):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.options = options
        self.result = '_'
        self.createWidgets()
        self.grab_set()
        # wait.window ensures that calling function waits for the window to
        # close before the result is returned.
        self.wait_window()

    def createWidgets(self):
        frmQuestion = tk.Frame(self)
        tk.Label(frmQuestion, text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = tk.Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = tk.Button(frmButtons, text=option, command=lambda x=option: self.setOption(x))
            btn.grid(column=column, row=0)
            column += 1

    def setOption(self, optionSelected):
        self.result = optionSelected
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


class tkWin:
    def __init__(self):
        """
        Main GUI for the whole thing to ease things out for people who have no idea how to use it
        """
        super().__init__()
        global folder_selected, status
        self.window = tk.Tk()
        self.window.geometry("+50+60")
        self.window.resizable(False, False)  # don't resize because it doesn't change the grid
        self.window.title("Random cut and concat")
        self.folder_selected = ""

        # variables
        self.varMinLen = tk.IntVar(self.window, value=0.5)
        self.varMaxLen = tk.IntVar(self.window, value=3)
        self.varRepeats = tk.IntVar(self.window, value=5)
        self.varStatus = tk.StringVar(self.window, value="Waiting for folder to be selected...")
        self.varDiscard = tk.IntVar(self.window, value=20)
        self.varVideos = tk.IntVar(self.window, value=1)

        # Stuff
        self.minLenLbl = tk.Label(self.window, text="Min Clip Length:")
        self.minLenEnt = tk.Entry(self.window, textvariable=self.varMinLen)

        self.maxLenLbl = tk.Label(self.window, text="Max Clip Length:")
        self.maxLenEnt = tk.Entry(self.window, textvariable=self.varMaxLen)

        self.discardLbl = tk.Label(self.window, text="% of random clips discarded")
        self.discardEnt = tk.Entry(self.window, textvariable=self.varDiscard)

        self.repeatsLbl = tk.Label(self.window, text="Repeat thru list times:")
        self.repeatsEnt = tk.Entry(self.window, textvariable=self.varRepeats)

        self.videosLbl = tk.Label(self.window, text="Amount of different videos:")
        self.videosEnt = tk.Entry(self.window, textvariable=self.varVideos)

        self.status = tk.Label(self.window, textvariable=self.varStatus)

        self.chsFldBtn = tk.Button(self.window, text="Choose folder", padx=10, command=self.selectFolder)

        self.stopBtn = tk.Button(self.window, text="Stop and Close", padx=10, command=self.on_closing)

        # Grid
        self.minLenLbl.grid(row=4, column=0, pady=3, sticky="e")
        self.minLenEnt.grid(row=4, column=1, pady=3, sticky="nesw")

        self.maxLenLbl.grid(row=5, column=0, pady=3, sticky="e")
        self.maxLenEnt.grid(row=5, column=1, pady=3, sticky="nesw")

        self.discardLbl.grid(row=6, column=0, pady=3, sticky="e")
        self.discardEnt.grid(row=6, column=1, pady=3, sticky="nesw")

        self.repeatsLbl.grid(row=7, column=0, pady=3, sticky="e")
        self.repeatsEnt.grid(row=7, column=1, pady=3, sticky="nesw")

        self.videosLbl.grid(row=8, column=0, pady=3, sticky="e")
        self.videosEnt.grid(row=8, column=1, pady=3, sticky="nesw")

        self.status.grid(row=9, column=0, columnspan=2, pady=3)

        self.chsFldBtn.grid(row=10, column=0, pady=3, padx=3, columnspan=2, sticky="nesw")

        self.stopBtn.grid(row=11, column=0, pady=3, padx=3, columnspan=2, sticky="nesw")

        # don't quit yet
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the window
        self.window.mainloop()

    def statusUpdate(self, statusText, allowPrint=False):
        """
        Changes the status text.
        :param statusText: What text to change to.
        :param allowPrint: print to console or not
        :return: Nothing
        """
        self.varStatus.set(statusText)
        if allowPrint:
            print(statusText)
        return

    def selectFolder(self):
        """
        Asks user what folder to concat videos from, then starts making it.
        :return: A videosEnt.
        """
        global t
        if self.folder_selected:
            return False
        try:  # validate the nums
            float(self.varMinLen.get())
            float(self.varMaxLen.get())
            int(self.varRepeats.get())
            int(self.varDiscard.get())
            int(self.varVideos.get())
        except ValueError:
            self.statusUpdate("Error:\nCan't convert some inputs. Check your inputs")
            logging.warning("Can't convert some inputs. Check your inputs")
            self.window.update()
            return False
        self.window.update()
        self.folder_selected = filedialog.askdirectory(title="Directory of the videos")
        self.window.update()
        if self.folder_selected == '' and not path.isfile(self.folder_selected):
            self.window.update()
            self.window.focus_force()
            return False
        print(self.folder_selected)
        self.statusUpdate("Processing... If this does not change, there might be an error.")

        t = threading.Thread(target=self.processing, args=(
            self.folder_selected, self.minLenEnt.get(), self.maxLenEnt.get(), self.repeatsEnt.get(),
            self.varDiscard.get(), self.varVideos.get()), daemon=True)
        t.start()
        return True

    def changeButtons(self, isDisabled):
        """
        Change State of common entries and buttons.
        :param isDisabled: normal Or disable.
        :return:
        """
        isDisabled = "disabled" if isDisabled else "normal"
        self.minLenEnt.config(state=isDisabled)
        self.maxLenEnt.config(state=isDisabled)
        self.repeatsEnt.config(state=isDisabled)
        self.chsFldBtn.config(state=isDisabled)
        self.discardEnt.config(state=isDisabled)
        self.videosEnt.config(state=isDisabled)
        return

    def on_closing(self):
        """
        Asks user if they REALLY want to close the window and quit.
        :return:
        """
        global t
        self.window.lift()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.quit()
            if t.is_alive():
                print("\nThread still running, some files may not be properly finished using.")
            else:
                print("\nThread not running.")

    def processing(self, directory, minLength, maxLength, repeats, discardedClipsPercent, amountOfVideos):
        """
        Where the real magic happens.
        :param directory: Directory of videos.
        :param xDim: Width of output videosEnt.
        :param yDim: Height of output videosEnt.
        :param minLength: Shortest clip possible.
        :param maxLength: Longest clip possible.
        :param repeats: How many more times to reuse all the clips.
        :param discardedClipsPercent: percentage of how much clips to be discarded every loop.
        :param ffmpeg_preset: FFmpeg compression preset (Refer to FFmpeg).
        :param amountOfVideos: Amount of different videos to make.
        :return: A Video.
        """
        # compile list of videos
        videoFormats = ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a')
        clips = [path.join(directory, f) for f in listdir(directory) if f.endswith(videoFormats) and
                 path.isfile(path.join(directory, f)) and "FINAL-" not in f]
        probes = {clip: ffmpeg.probe(clip) for clip in clips}
        resolutions = []
        for probe in probes.values():
            for i in probe["streams"]:
                if i["codec_type"] == "video":
                    resolutions.append((i["width"], i["height"]))
                    break
        resolutions = Counter(resolutions)
        if len(resolutions) > 1:
            values = list(map(lambda a: f"{a[0]}x{a[1]} ({resolutions[a]} videos)", resolutions.keys()))
            dlg = OptionDialog(self.window, 'Resolutions',
                               "Different resolutions of video detected.\nChoose resolution of the videos to keep.",
                               values)
            width, height = dlg.result.partition(" ")[0].split("x")
            width, height = int(width), int(height)
            values = list(probes.values())
            keys = list(probes.keys())
            clips = []
            for probe in probes.values():
                for stream in probe["streams"]:
                    if stream["codec_type"] == "video" and stream["width"] == width and stream["height"] == height:
                        clips.append(keys[values.index(probe)])
                        break
        logging.debug("Clips: {}".format(clips))
        inputs = []
        for i in range(amountOfVideos):
            tempInputs = [q for i in range(int(repeats)) for q in clips if randint(0, 100) >= float(
                discardedClipsPercent)]  # randomly selects from original full list
            shuffle(tempInputs)
            inputs.append(tempInputs.copy())
        logging.debug("Randomly selected clips: {}".format(inputs))
        self.changeButtons(True)

        output, outputs = [], []
        self.statusUpdate("Cutting...")
        for v in inputs:
            for c in v:
                logging.info("\rCutting {}".format(c))
                duration = float(ffmpeg.probe(c)["format"]["duration"])

                length = round(uniform(float(minLength), float(maxLength)), 2)
                start = round(uniform(0, duration - length), 2)
                output.append((c, start, start + length))
            outputs.append(output.copy())
            output.clear()
        self.statusUpdate("Writing {} video(s)...".format(str(amountOfVideos)))
        for i in range(len(outputs)):
            outPath = os.path.join(directory, f"FINAL-{i + 1}.MP4")
            videoPath = os.path.join(directory, f"FINAL-{i + 1}-V.MP4")
            audioPath = os.path.join(directory, f"FINAL-{i + 1}-A.MP3")
            temp = [ffmpeg.input(c[0]).trim(start=c[1], end=c[2]).setpts('PTS-STARTPTS') for c in outputs[i]]
            ffmpeg.concat(*temp).output(videoPath).overwrite_output().global_args("-an").global_args("-loglevel",
                                                                                                     "warning").global_args(
                "-stats").run()

            temp2 = [ffmpeg.input(c[0]).filter('atrim', start=c[1], end=c[2]) for c in outputs[i]]
            ffmpeg.concat(*temp2).output(audioPath).overwrite_output().global_args("-vn").run()

            ffmpeg.concat(ffmpeg.input(videoPath), ffmpeg.input(audioPath), v=1, a=1).output(outPath).run()
            # .global_args("-loglevel", "warning").global_args("-stats")
            # os.remove(videoPath)
            # os.remove(audioPath)
        self.statusUpdate("Done", True)
        self.changeButtons(False)
        self.folder_selected = ""
        return output


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    windows = tkWin()
