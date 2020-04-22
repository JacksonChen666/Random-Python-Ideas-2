"""
This program takes a folder of videos, pick a random spot, and then just combine it into a video and done
"""
# TODO: Open folder from system to show the final mp4 file
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

        # variables
        vidQ = ['2160p (4K)', '1440p (2K)', '1080p (Full HD)',
                '720p (HD)', '480p (SD)', '360p', '240p', '144p']
        ffmpegPreset = ["ultrafast", "superfast", "veryfast", "faster", "fast",
                        "medium", "slow", "slower", "veryslow", "placebo"]
        self.varQuality = tk.StringVar(self.window, value=vidQ[2])
        self.varXdim = tk.StringVar(self.window, value=1920)
        self.varYdim = tk.StringVar(self.window, value=1080)
        self.varMinLen = tk.StringVar(self.window, value=0.25)
        self.varMaxLen = tk.StringVar(self.window, value=3)
        self.varRepeats = tk.StringVar(self.window, value=5)
        self.varStatus = tk.StringVar(self.window, value="Waiting for folder to be selected...")
        self.varPreset = tk.StringVar(self.window, value="medium")

        # Stuff
        self.presetLbl = tk.Label(self.window, text="FFmpeg compression preset:")
        self.preset = tk.OptionMenu(self.window, self.varPreset, *ffmpegPreset)

        self.qualityLbl = tk.Label(self.window, text="Video quality preset:")
        self.quality = tk.OptionMenu(self.window, self.varQuality, *vidQ)

        self.xdimLbl = tk.Label(self.window, text="Video Width:")
        self.xdim = tk.Entry(self.window, textvariable=self.varXdim)

        self.ydimLbl = tk.Label(self.window, text="Video Height:")
        self.ydim = tk.Entry(self.window, textvariable=self.varYdim)

        self.minLenLbl = tk.Label(self.window, text="Min Clip Length:")
        self.minLen = tk.Entry(self.window, textvariable=self.varMinLen)

        self.maxLenLbl = tk.Label(self.window, text="Max Clip Length:")
        self.maxLen = tk.Entry(self.window, textvariable=self.varMaxLen)

        self.repeatsLbl = tk.Label(self.window, text="Repeat thru list times:")
        self.repeats = tk.Entry(self.window, textvariable=self.varRepeats)

        self.status = tk.Label(self.window, textvariable=self.varStatus)

        self.chsFldBtn = tk.Button(self.window, text="Choose folder", padx=10, command=self.selectFolder)

        self.installBtn = tk.Button(self.window, text="Install required libraries", padx=10,
                                    command=self.installLibraries)

        self.stopBtn = tk.Button(self.window, text="Stop and Close", padx=10, command=self.on_closing)

        # Grid
        self.presetLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.preset.grid(row=0, column=1, pady=5, sticky="nesw")

        self.qualityLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.quality.grid(row=1, column=1, pady=5, sticky="nesw")

        self.xdimLbl.grid(row=2, column=0, pady=5, sticky="e")
        self.xdim.grid(row=2, column=1, pady=5, sticky="nesw")

        self.ydimLbl.grid(row=3, column=0, pady=5, sticky="e")
        self.ydim.grid(row=3, column=1, pady=5, sticky="nesw")

        self.minLenLbl.grid(row=4, column=0, pady=5, sticky="e")
        self.minLen.grid(row=4, column=1, pady=5, sticky="nesw")

        self.maxLenLbl.grid(row=5, column=0, pady=5, sticky="e")
        self.maxLen.grid(row=5, column=1, pady=5, sticky="nesw")

        self.repeatsLbl.grid(row=6, column=0, pady=5, sticky="e")
        self.repeats.grid(row=6, column=1, pady=5, sticky="nesw")

        self.status.grid(row=7, column=0, columnspan=2, pady=5)

        self.chsFldBtn.grid(row=8, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        self.installBtn.grid(row=9, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        self.stopBtn.grid(row=10, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        # Be on top of everything
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.update()

        # don't quit yet
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # detect choice change
        self.varQuality.trace("w", self.qualityChange)
        # Start the window
        self.window.mainloop()

    def statusUpdate(self, statusText):
        """
        Changes the status text.
        :param statusText: What text to change to.
        :return: Nothing
        """
        self.varStatus.set(statusText)
        return

    def selectFolder(self):
        """
        Asks user what folder to concat videos from, then starts making it.
        :return: A video.
        """
        global t
        import threading
        try:  # Validation
            if t.is_alive():
                return
        except NameError:
            pass
        self.folder_selected = filedialog.askdirectory(title="Directory of the videos")
        if self.folder_selected == '':
            return False
        print(self.folder_selected + "/")
        self.statusUpdate("Processing... If this does not change, there might be an error.")

        self.window.update()

        t = threading.Thread(target=self.processing, args=(
            self.folder_selected, self.xdim.get(), self.ydim.get(), self.minLen.get(), self.maxLen.get(),
            self.repeats.get(), self.varPreset.get()), daemon=True)
        t.setDaemon(True)
        t.start()
        # t.join() # don't join, or the window will freeze

    def installLibraries(self):
        """
        Install the library assuming you don't have it.
        :return: A Library.
        """
        from subprocess import run
        try:
            run("pip install moviepy", shell=True, check=True)
            run("pip install moviepy --upgrade", shell=True, check=True)
        except CalledProcessError:
            run("pip3 install moviepy", shell=True, check=True)
            run("pip3 install moviepy --upgrade", shell=True, check=True)
        self.installBtn.destroy()

    def changeButtons(self, ED):
        """
        Change State of common entries and buttons.
        :param ED: normal Or disable.
        :return:
        """
        self.quality.config(state=ED)
        self.xdim.config(state=ED)
        self.ydim.config(state=ED)
        self.minLen.config(state=ED)
        self.maxLen.config(state=ED)
        self.repeats.config(state=ED)
        self.chsFldBtn.config(state=ED)
        self.quality.config(state=ED)
        self.preset.config(state=ED)
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

    def qualityChange(self, i, d, c):
        """
        Sets resolution for qualities.
        :param i: I
        :param d: DON'T
        :param c: CARE
        :return: numbers
        """
        global vidQ
        var = self.varQuality.get()
        if var == vidQ[0]:
            self.varXdim.set(3840)
            self.varYdim.set(2160)
        elif var == vidQ[1]:
            self.varXdim.set(2560)
            self.varYdim.set(1440)
        elif var == vidQ[2]:
            self.varXdim.set(1920)
            self.varYdim.set(1080)
        elif var == vidQ[3]:
            self.varXdim.set(1280)
            self.varYdim.set(720)
        elif var == vidQ[4]:
            self.varXdim.set(854)
            self.varYdim.set(480)
        elif var == vidQ[5]:
            self.varXdim.set(640)
            self.varYdim.set(360)
        elif var == vidQ[6]:
            self.varXdim.set(426)
            self.varYdim.set(240)
        elif var == vidQ[7]:
            self.varXdim.set(256)
            self.varYdim.set(144)
        else:
            print("That's weird :/ option not found")
        return

    def processing(self, directory, xdim, ydim, minLength, maxLength, repeats, ffmpeg_preset):
        """
        Where the real magic happens.
        :param directory: Directory of videos.
        :param xdim: Width of output video.
        :param ydim: Height of output video.
        :param minLength: Shortest clip possible.
        :param maxLength: Longest clip possible.
        :param repeats: How many more times to reuse all the clips.
        :param ffmpeg_preset: FFmpeg compression preset (Refer to FFmpeg).
        :return: A Video.
        """
        global collages
        self.installBtn.destroy()  # i've warned you, that you have installed it!!
        self.changeButtons("disabled")
        print("Importing...")
        self.statusUpdate("Importing...")
        from multiprocessing import cpu_count
        import random, os, moviepy.editor, moviepy

        outputs = []
        print("Thread count of export process: {0}".format(str(cpu_count() * 2)))
        self.statusUpdate("Thread count of export process: {0}".format(str(cpu_count() * 2)))
        # compile list of videos
        videos = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.join(directory, f).endswith(
            ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b')) and
                  os.path.isfile(os.path.join(directory, f)) and f != "FINAL.mp4"]

        for q in range(int(repeats)):
            inputs = [q for q in videos if random.randint(0, 1) == 0]  # randomly selects from original full list
            random.shuffle(inputs)
            self.statusUpdate("Repeating {0}/{1} times and Cutting...".format(q + 1, int(repeats)))
            for i in inputs:
                print("\rRepeating {0}/{1} times and Cutting {2}".format(q + 1, int(repeats), i), end="", flush=True)

                # import to moviepy
                clip = moviepy.editor.VideoFileClip(i).resize((int(xdim), int(ydim)))

                # timing
                length = round(random.uniform(float(minLength), float(maxLength)), 2)
                start = round(random.uniform(0, clip.duration - length), 2)

                # cut a subclip and store it later
                outputs.append(clip.subclip(start, start + length))
        # combine clips from different videos
        print("\nConcatenating...")
        self.statusUpdate("Concatenating...")
        print('Writing... Thread count: {0}'.format(str(cpu_count() * 2)))
        self.statusUpdate("Writing... Thread count: {0}.\nKilling the GUI may not stop the writing process".format(str(
            cpu_count() * 2)))
        collage = moviepy.editor.concatenate_videoclips(outputs)
        try:
            collage.write_videofile(directory + '/FINAL.MP4', threads=cpu_count() * 2, preset=ffmpeg_preset)
        except AttributeError:
            self.changeButtons("normal")
            self.statusUpdate("An error occurred")
            collage.close()
            clips.close()
            del video_file_clip.make_frame
            raise
        print("Done")
        self.statusUpdate("Done\nClose and open the app to continue without memory overflow problems")
        self.changeButtons("normal")
        self.folder_selected = ""
        collage.close()  # clean up
        # Calls function that plays audio that it is done
        return outputs


if __name__ == '__main__':
    windows = tkWin()
else:
    print("the random cut and concat gui version will not open the gui. you are welcome")
