# my greatest achievement of a gui app with things this is too good
import tkinter as tk
from tkinter import filedialog, messagebox
"""
This program takes a folder of videos, pick a random spot, and then just combine it into a video and done
"""

class tkWin:
    def __init__(self, window=None):
        super().__init__()
        global folder_selected, status
        self.window = tk.Tk()
        self.window.geometry("+50+60")
        self.window.resizable(False, False)  # don't resize because it doesn't change the grid
        self.window.title("Random cut and concat")

        # variables
        vidQ = ['2160p (4K)', '1440p (2K)', '1080p (Full HD)', '720p (HD)', '480p (SD)', '360p', '240p', '144p']
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
        self.preset = tk.OptionMenu(self.window, self.varPreset, "ultrafast", "superfast", "veryfast", "faster", "fast",
                                    "medium", "slow", "slower", "veryslow", "placebo")

        self.qualityLbl = tk.Label(self.window, text="Video quality preset:")
        self.quality = tk.OptionMenu(self.window, self.varQuality, '2160p (4K)', '1440p (2K)', '1080p (Full HD)',
                                     '720p (HD)', '480p (SD)', '360p', '240p', '144p')

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

        self.installBtn = tk.Button(self.window,text="Install required libraries",padx=10,command=self.installLibraries)

        self.stopBtn = tk.Button(self.window, text="Stop and Close", padx=10, command=self.on_closing)

        # Grid
        self.presetLbl.grid(row=0, column=0, pady=5, sticky="e")
        self.preset.grid(row=0, column=1, pady=5, sticky="nesw")

        self.qualityLbl.grid(row=1, column=0, pady=5, sticky="e")
        self.quality.grid(row=1, column=1, pady=5, sticky="nesw")

        self.xdimLbl.grid(row=2, column=0, pady=5, sticky="e")
        self.xdim.grid(row=2, column=1, pady=5,sticky="nesw")

        self.ydimLbl.grid(row=3, column=0, pady=5, sticky="e")
        self.ydim.grid(row=3, column=1, pady=5,sticky="nesw")

        self.minLenLbl.grid(row=4, column=0, pady=5, sticky="e")
        self.minLen.grid(row=4, column=1, pady=5,sticky="nesw")

        self.maxLenLbl.grid(row=5, column=0, pady=5, sticky="e")
        self.maxLen.grid(row=5, column=1, pady=5,sticky="nesw")

        self.repeatsLbl.grid(row=6, column=0, pady=5, sticky="e")
        self.repeats.grid(row=6, column=1, pady=5,sticky="nesw")

        self.status.grid(row=7, column=0, columnspan=2, pady=5)

        self.chsFldBtn.grid(row=8, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        self.installBtn.grid(row=9,column=0,pady=5,padx=5,columnspan=2,sticky="nesw")

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
        self.varStatus.set(statusText)

    def selectFolder(self):
        global t
        import threading
        try:  # Validation
            if self.folder_selected == '' or not self.folder_selected:
                pass
            else:
                return False
        except AttributeError:
            pass
        self.folder_selected = filedialog.askdirectory(title="Directory of the videos")
        if self.folder_selected == '':
            return False
        print(self.folder_selected + "/")
        self.statusUpdate("Processing... If this does not change, there might be an error.")

        self.window.update()

        t = threading.Thread(target=self.processing, args=(
            self.folder_selected + "/", self.xdim.get(), self.ydim.get(), self.minLen.get(), self.maxLen.get(),
            self.repeats.get(), self.varPreset.get()), daemon=True)
        t.setDaemon(True)
        t.start()
        # t.join() # don't join, or the window will freeze
        # main(self.folder_selected + "/", self.xdim.get(), self.ydim.get(), self.minLen.get(), self.maxLen.get(),
        #      self.repeats.get(),self.varPreset.get())

    def installLibraries(self):
        from subprocess import run
        try:
            run("pip install moviepy", shell=True, check=True)
        except:
            run("pip3 install moviepy", shell=True, check=True)
        finally:
            run("pip3 install moviepy", shell=True, check=True)
        self.installBtn.destroy()

    def changeButtons(self, ED):
        self.quality.config(state=ED)
        self.xdim.config(state=ED)
        self.ydim.config(state=ED)
        self.minLen.config(state=ED)
        self.maxLen.config(state=ED)
        self.repeats.config(state=ED)
        self.chsFldBtn.config(state=ED)
        self.quality.config(state=ED)
        self.preset.config(state=ED)

    def on_closing(self):
        global t
        self.window.lift()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.quit()
            if t.is_alive():
                print("\nThread still running, some files may not be properly finished using.")
            else:
                print("\nThread not running.")

    def qualityChange(self, i, d, k):
        var = self.varQuality.get()
        if var == "2160p (4K)":
            self.varXdim.set(3840)
            self.varYdim.set(2160)
            return
        elif var == "1440p (2K)":
            self.varXdim.set(2560)
            self.varYdim.set(1440)
            return
        elif var == "1080p (Full HD)":
            self.varXdim.set(1920)
            self.varYdim.set(1080)
            return
        elif var == "720p (HD)":
            self.varXdim.set(1280)
            self.varYdim.set(720)
            return
        elif var == "480p (SD)":
            self.varXdim.set(854)
            self.varYdim.set(480)
            return
        elif var == "360p":
            self.varXdim.set(640)
            self.varYdim.set(360)
            return
        elif var == "240p":
            self.varXdim.set(426)
            self.varYdim.set(240)
            return
        elif var == "144p":
            self.varXdim.set(256)
            self.varYdim.set(144)
            return
        else:
            print("That's weird :/ option not found")

    def processing(self, directory, xdim, ydim, minLength, maxLength, repeats, ffmpeg_preset):  # Where the real magic
        # happens
        self.changeButtons("disabled")
        print("Importing...")
        self.statusUpdate("Importing...")
        from multiprocessing import cpu_count
        import random, os, moviepy.editor, moviepy

        outputs = []
        print("Thread count of export process: {0}".format(str(cpu_count() * 2)))
        self.statusUpdate("Thread count of export process: {0}".format(str(cpu_count() * 2)))
        # compile list of videos
        # inputs = [os.path.join(directory, f) for f in os.listdir(directory) if
        #           os.path.isfile(os.path.join(directory, f)) and fnmatch.fnmatch(f, ext)]

        inputs = []

        for f in os.listdir(directory):
            a = os.path.join(directory, f)
            if a.endswith(
                    ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b')):
                inputs.append(a)

        for q in range(int(repeats)):
            self.installBtn.destroy()
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

                # bye
                clip.close()

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
            raise
        print("Done")
        self.statusUpdate("Done")
        collage.close()
        self.changeButtons("normal")
        self.folder_selected = ""
        # Calls function that plays audio that it is done
        return outputs


if __name__ == '__main__':
    windows = tkWin()
else:
    print("the random cut and concat gui version will not open the gui. you are welcome")
