"""
This program takes a folder of videos, pick a random spot, and then just combine it into a videosEnt and done
"""
import logging
import tkinter as tk
from tkinter import filedialog, messagebox


class tkWin:
    def __init__(self):
        """
        Main GUI for the whole thing to ease things out for people who have no idea how to use it
        """
        super().__init__()
        global folder_selected, status, vidQ
        self.window = tk.Tk()
        self.window.geometry("+50+60")
        self.window.resizable(False, False)  # don't resize because it doesn't change the grid
        self.window.title("Random cut and concat")
        self.folder_selected = ""

        # variables
        vidQ = ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']
        ffmpegPreset = ["ultrafast", "superfast", "veryfast", "faster", "fast",
                        "medium", "slow", "slower", "veryslow", "placebo"]
        self.varQuality = tk.StringVar(self.window, value=vidQ[2])
        self.varXdim = tk.IntVar(self.window, value=1920)
        self.varYdim = tk.IntVar(self.window, value=1080)
        self.varMinLen = tk.IntVar(self.window, value=0.5)
        self.varMaxLen = tk.IntVar(self.window, value=3)
        self.varRepeats = tk.IntVar(self.window, value=5)
        self.varStatus = tk.StringVar(self.window, value="Waiting for folder to be selected...")
        self.varPreset = tk.StringVar(self.window, value="medium")
        self.varDiscard = tk.IntVar(self.window, value=20)
        self.varVideos = tk.IntVar(self.window, value=1)

        # Stuff
        self.presetLbl = tk.Label(self.window, text="FFmpeg compression preset:")
        self.preset = tk.OptionMenu(self.window, self.varPreset, *ffmpegPreset)

        self.qualityLbl = tk.Label(self.window, text="Video quality preset:")
        self.quality = tk.OptionMenu(self.window, self.varQuality, *vidQ)

        self.xDimLbl = tk.Label(self.window, text="Video Width:")
        self.xDimEnt = tk.Entry(self.window, textvariable=self.varXdim)

        self.yDimLbl = tk.Label(self.window, text="Video Height:")
        self.yDimEnt = tk.Entry(self.window, textvariable=self.varYdim)

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
        self.presetLbl.grid(row=0, column=0, pady=3, sticky="e")
        self.preset.grid(row=0, column=1, pady=3, sticky="nesw")

        self.qualityLbl.grid(row=1, column=0, pady=3, sticky="e")
        self.quality.grid(row=1, column=1, pady=3, sticky="nesw")

        self.xDimLbl.grid(row=2, column=0, pady=3, sticky="e")
        self.xDimEnt.grid(row=2, column=1, pady=3, sticky="nesw")

        self.yDimLbl.grid(row=3, column=0, pady=3, sticky="e")
        self.yDimEnt.grid(row=3, column=1, pady=3, sticky="nesw")

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

        # detect choice change
        self.varQuality.trace("w", self.qualityChange)
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
        if allowPrint: print(statusText)
        return

    def selectFolder(self):
        """
        Asks user what folder to concat videos from, then starts making it.
        :return: A videosEnt.
        """
        global t
        import threading
        import os
        if self.folder_selected: return False
        try:  # validate the nums
            int(self.varXdim.get())
            int(self.varYdim.get())
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
        if self.folder_selected == '' and not os.path.isfile(self.folder_selected):
            self.window.update()
            self.window.focus_force()
            return False
        print(self.folder_selected)
        self.statusUpdate("Processing... If this does not change, there might be an error.")

        t = threading.Thread(target=self.processing, args=(
            self.folder_selected, self.xDimEnt.get(), self.yDimEnt.get(), self.minLenEnt.get(), self.maxLenEnt.get(),
            self.repeatsEnt.get(), self.varDiscard.get(), self.varPreset.get(), self.varVideos.get()),
                             daemon=True).start()
        return True

    def changeButtons(self, isDisabled):
        """
        Change State of common entries and buttons.
        :param isDisabled: normal Or disable.
        :return:
        """
        isDisabled = "disabled" if isDisabled else "normal"
        self.quality.config(state=isDisabled)
        self.xDimEnt.config(state=isDisabled)
        self.yDimEnt.config(state=isDisabled)
        self.minLenEnt.config(state=isDisabled)
        self.maxLenEnt.config(state=isDisabled)
        self.repeatsEnt.config(state=isDisabled)
        self.chsFldBtn.config(state=isDisabled)
        self.quality.config(state=isDisabled)
        self.preset.config(state=isDisabled)
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
            try:
                if t.is_alive():
                    print("\nThread still running, some files may not be properly finished using.")
                else:
                    print("\nThread not running.")
            except NameError:
                pass

    def qualityChange(self, i, d, c):
        """
        Sets resolution for qualities.
        :param i: I
        :param d: DON'T
        :param c: CARE
        :return: numbers
        """
        vidQRes = [(3840, 2160), (2560, 1440), (1920, 1080), (1280, 720), (854, 480), (640, 360), (426, 240),
                   (256, 144)]
        i = vidQ.index(self.varQuality.get())
        self.varXdim.set(vidQRes[i][0])
        self.varYdim.set(vidQRes[i][1])
        return

    def processing(self, directory, xDim, yDim, minLength, maxLength, repeats, discardedClipsPercent, ffmpeg_preset,
                   amountOfVideos):
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
        import os, random

        # compile list of videos
        videoFormats = ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a')
        clips = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(videoFormats) and
                 os.path.isfile(os.path.join(directory, f)) and "FINAL-" not in f]
        logging.debug("Clips: {}".format(clips))
        inputs = []
        for i in range(amountOfVideos):
            tempInputs = [q for i in range(int(repeats)) for q in clips if random.randint(0, 100) >= float(
                discardedClipsPercent)]  # randomly selects from original full list
            random.shuffle(tempInputs)
            inputs.append(tempInputs.copy())
        logging.debug("Randomly selected clips: {}".format(inputs))
        aClips = 0
        for i in inputs: aClips += len(i)
        if 500 < aClips < 10000:
            logging.warning("Exceeded normal limit of 500, might be dangerous if it takes over system ram")
            if messagebox.askokcancel("a lotta clips",
                                      "There is a total of {} clips used for concat. "
                                      "Are you sure to continue?".format(aClips)):
                pass
            else:
                self.statusUpdate("Waiting for folder to be selected...")
                return
        elif aClips > 10000:
            logging.warning("Exceeded max limit of 10000, that's too dangerous")
            self.statusUpdate("Waiting for folder to be selected...")
            messagebox.showwarning("WAY too many clips", "{} is too many clips. The hard limit is 10000 clips. "
                                                         "Try lowering repeatsEnt and increasing discards".format(
                aClips))
            return
        self.changeButtons(True)
        self.statusUpdate("Importing...")
        logging.debug("Importing modules required to continue...")
        from multiprocessing import cpu_count
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        import traceback as tc
        logging.debug("Finished importing")

        output, outputs = [], []
        self.statusUpdate("Thread count of export process: {0}".format(str(cpu_count() * 2)), True)
        self.statusUpdate("Cutting...")
        for v in inputs:
            for c in v:
                logging.info("\rCutting {}".format(c))
                clip = VideoFileClip(c).resize((int(xDim), int(yDim)))
                length = round(random.uniform(float(minLength), float(maxLength)), 2)
                start = round(random.uniform(0, clip.duration - length), 2)
                try:
                    output.append(clip.subclip(start, start + length))
                except OSError:
                    self.statusUpdate("oops! error:\n{}\ncontinuing".format(tc.format_exc()))
                    logging.exception("Exception-ed")
            outputs.append(output.copy())
            output.clear()
        self.statusUpdate("Writing {} video(s)... Thread count: {}.".format(str(amountOfVideos), str(cpu_count() * 2)))
        for i in range(len(outputs)):
            try:
                concatenate_videoclips(outputs[i]).write_videofile(
                    os.path.join(directory, 'FINAL-{}.MP4'.format(i + 1)), threads=cpu_count() * 2,
                    preset=ffmpeg_preset)
            except (AttributeError,):
                self.statusUpdate("oops! error:\n{}\nskipping".format(tc.format_exc()))
                logging.exception("Exception-ed")
        self.statusUpdate("Done", True)
        self.changeButtons(False)
        self.folder_selected = ""
        return output


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    windows = tkWin()
