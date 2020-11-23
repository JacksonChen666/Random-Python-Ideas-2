"""
This program takes a folder of videos, pick a random spot, and then just combine it into a videosEnt and done
"""
import logging
import os
import random
import re
import threading
import tkinter as tk
from collections import Counter
from concurrent import futures
from multiprocessing import cpu_count
from os import listdir, path
from random import randint, shuffle, uniform
from shutil import rmtree
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
        self.varToSeconds = tk.IntVar(self.window, value=0)

        # Stuff
        self.minLenLbl = tk.Label(self.window, text="Min Clip Length:")
        self.minLenEnt = tk.Entry(self.window, textvariable=self.varMinLen)

        self.maxLenLbl = tk.Label(self.window, text="Max Clip Length:")
        self.maxLenEnt = tk.Entry(self.window, textvariable=self.varMaxLen)

        self.discardLbl = tk.Label(self.window, text="% of random clips discarded")
        self.discardEnt = tk.Entry(self.window, textvariable=self.varDiscard)

        self.repeatsLbl = tk.Label(self.window, text="Repeat thru list times:")
        self.repeatsEnt = tk.Entry(self.window, textvariable=self.varRepeats)

        self.toSecondsLbl = tk.Label(self.window, text="Make video seconds long:")
        self.toSecondsEnt = tk.Entry(self.window, textvariable=self.varToSeconds)

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

        self.toSecondsLbl.grid(row=8, column=0, pady=3, sticky="e")
        self.toSecondsEnt.grid(row=8, column=1, pady=3, sticky="nesw")

        self.videosLbl.grid(row=9, column=0, pady=3, sticky="e")
        self.videosEnt.grid(row=9, column=1, pady=3, sticky="nesw")

        self.status.grid(row=10, column=0, columnspan=2, pady=3)

        self.chsFldBtn.grid(row=11, column=0, pady=3, padx=3, columnspan=2, sticky="nesw")

        self.stopBtn.grid(row=12, column=0, pady=3, padx=3, columnspan=2, sticky="nesw")

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
            float(self.varToSeconds.get())
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
            self.varDiscard.get(), self.varVideos.get(), self.varToSeconds.get()), daemon=True)
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
        self.toSecondsEnt.config(state=isDisabled)
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

    def processing(self, directory, minLength, maxLength, repeats, discardedClipsPercent, amountOfVideos, toTime=0):
        """
        Where the real magic happens.
        :param directory: Directory of videos.
        :param minLength: Shortest clip possible.
        :param maxLength: Longest clip possible.
        :param repeats: How many more times to reuse all the clips.
        :param discardedClipsPercent: percentage of how much clips to be discarded every loop.
        :param amountOfVideos: Amount of different videos to make.
        :param toTime: Amount of seconds of video to make
        :return: A Video.
        """

        def cutClip(filename, minLen=minLength, maxLen=maxLength):
            logging.info("\rCutting {}".format(filename))
            duration = float(probes[filename]["format"]["duration"])
            length = round(uniform(float(minLen), float(maxLen)), 2)
            start = round(uniform(0, duration - length), 2)
            return filename, start, start + length

        # compile list of videos
        self.changeButtons(True)
        maxLength, toTime = int(maxLength), float(toTime)
        videoFormats = ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi')
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
            values = list(map(lambda q: f"{q[0]}x{q[1]} ({resolutions[q]} videos)", resolutions.keys()))
            dlg = OptionDialog(self.window, 'Resolutions',
                               "Different resolutions of video detected.\nChoose resolution of the videos to keep.",
                               values)
            width, height = map(lambda q: int(q), dlg.result.partition(" ")[0].split("x"))
            keys = list(probes.keys())
            values = list(probes.values())
            clips = [keys[values.index(probe)] for probe in values for stream in probe["streams"] if
                     stream["codec_type"] == "video" and stream["width"] == width and stream["height"] == height]

        logging.debug("Clips: {}".format(clips))
        output, outputs = [], []
        self.statusUpdate("Cutting...")
        for i in range(amountOfVideos):
            if toTime <= 0:
                for a in range(int(repeats)):
                    for clip in clips:
                        if randint(0, 100) >= float(discardedClipsPercent):
                            outputs.append(cutClip(clip))
            else:
                totalTime = 0
                while toTime > totalTime:
                    clip = random.choice(clips)
                    timeLeft = toTime - totalTime
                    _maxLength = maxLength if timeLeft > maxLength else timeLeft
                    clip, start, startAndLength = cutClip(clip, maxLen=_maxLength)
                    totalTime += startAndLength - start
                    output.append((clip, start, startAndLength))
            shuffle(output)
            outputs.append(output.copy())
            output.clear()
        shuffle(outputs)
        logging.debug(f"Cuts: {outputs}")

        temp_dir = os.path.join(directory, "TEMP")
        for i in range(len(outputs)):
            outPath = os.path.join(directory, f"FINAL-{i}.MP4")
            paths = {}
            try:
                os.mkdir(temp_dir)
            except FileExistsError:
                rmtree(temp_dir)
                os.mkdir(temp_dir)
            os.chdir(temp_dir)
            with futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
                total = 0
                self.statusUpdate(f"Submitting tasks...", allowPrint=True)
                for f in range(len(outputs[i])):
                    temp = {
                        ffmpeg.input(c[0]).video.trim(start=c[1], end=c[2]).setpts('PTS-STARTPTS'):
                            ffmpeg.input(c[0]).audio.filter('atrim', start=c[1], end=c[2]).filter('asetpts',
                                                                                                  'PTS-STARTPTS')
                        for c in outputs[i]
                    }
                    for s in range(len(temp.keys())):
                        videoPath = os.path.join(temp_dir, f"FINAL-TEMP-{i}-{s}-V.MP4")
                        audioPath = os.path.join(temp_dir, f"FINAL-TEMP-{i}-{s}-A.MP3")
                        a = list(temp.keys())[s]
                        paths[ffmpeg.input(videoPath).video] = ffmpeg.input(audioPath).audio
                        executor.submit(
                            a.output(videoPath).overwrite_output().global_args('-loglevel', 'warning').global_args(
                                '-stats').run)
                        executor.submit(
                            temp[a].output(audioPath).overwrite_output().global_args('-loglevel',
                                                                                     'warning').global_args(
                                '-stats').run)
                        total += 2
                self.statusUpdate(f"Processing {total} cuts for video {i}...", allowPrint=True)
                executor.shutdown()  # disallow submit and wait for all to complete
            self.statusUpdate(f"Finishing video {i}...", allowPrint=True)
            videoPath = os.path.join(temp_dir, f"FINAL-TEMP-{i}-V.MP4")
            audioPath = os.path.join(temp_dir, f"FINAL-TEMP-{i}-A.MP3")
            audios = sorted([os.path.abspath(i) for i in os.listdir(temp_dir) if
                             i.startswith("FINAL-TEMP-0") and i.endswith("-A.MP3")])
            with open(os.path.join(temp_dir, "concat.txt"), "w") as f:
                for a in audios:
                    f.write(f'file {re.escape(a)}\n')
            audio = ffmpeg.input(os.path.join(temp_dir, 'concat.txt'), format="concat", safe = "0").output(
                audioPath).overwrite_output().global_args('-loglevel', 'warning').global_args('-stats').run_async()
            ffmpeg.concat(*paths.keys()).output(videoPath).overwrite_output().global_args('-loglevel',
                                                                                          'warning').global_args(
                '-stats').run()
            audio.wait()
            ffmpeg.concat(ffmpeg.input(videoPath).video, ffmpeg.input(audioPath).audio, v=1, a=1).output(
                outPath).overwrite_output().global_args('-loglevel', 'warning').global_args('-stats').run()
            rmtree(temp_dir)
        self.statusUpdate("Done", True)
        self.changeButtons(False)
        self.folder_selected = ""
        return output


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    windows = tkWin()
