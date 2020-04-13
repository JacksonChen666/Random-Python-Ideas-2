import tkinter as tk
from tkinter import filedialog


def main(directory, xdim, ydim, minLength, maxLength, repeats):
    print("Importing...")
    from multiprocessing import cpu_count
    import random, os, moviepy.editor

    outputs = []
    print("Thread count of export process: {0}".format(str(cpu_count() * 2)))
    # compile list of videos
    # inputs = [os.path.join(directory, f) for f in os.listdir(directory) if
    #           os.path.isfile(os.path.join(directory, f)) and fnmatch.fnmatch(f, ext)]

    inputs = []

    for f in os.listdir(directory):
        a = os.path.join(directory, f)
        if a.endswith(('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b')):
            inputs.append(a)

    # print(inputs)

    for q in range(int(repeats)):
        print("\rRepeated {0}/{1}".format(q + 1, int(repeats)), end="")
        random.shuffle(inputs)
        for i in inputs:
            print("\rCutting {0}".format(i), end="")

            length = round(random.uniform(float(minLength), float(maxLength)), 2)

            # import to moviepy
            clip = moviepy.editor.VideoFileClip(i).resize((int(xdim), int(ydim)))

            # select a random time point
            start = round(random.uniform(0, clip.duration - length), 2)

            # cut a subclip
            out_clip = clip.subclip(start, start + length)

            outputs.append(out_clip)

    # combine clips from different videos
    print("\nConcatenating...")
    collage = moviepy.editor.concatenate_videoclips(outputs)
    print('Writing... Thread count: {0}'.format(str(cpu_count() * 2)))
    collage.write_videofile(directory + '/FINAL.MP4', verbose=False, logger=None, threads=cpu_count() * 2)
    print("Done")


class tkWin:
    def __init__(self, window=None):
        super().__init__()
        global folder_selected, status
        self.window = tk.Tk()
        self.window.geometry("+50+60")
        self.window.resizable(False, False)  # don't resize because it doesn't change the grid
        self.window.title("Random cut and concat")

        # variables
        self.varXdim = tk.StringVar(self.window, value=1920)
        self.varYdim = tk.StringVar(self.window, value=1080)
        self.varMinLen = tk.StringVar(self.window, value=0.25)
        self.varMaxLen = tk.StringVar(self.window, value=5)
        self.varRepeats = tk.StringVar(self.window, value=5)
        self.varStatus = tk.StringVar(self.window, value="Waiting for folder to be selected...")

        # Stuff
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
        self.stopBtn = tk.Button(self.window, text="Stop and Close", padx=10, command=exit)

        # Grid
        self.xdimLbl.grid(row=0, column=0, pady=5)
        self.xdim.grid(row=0, column=1, pady=5)

        self.ydimLbl.grid(row=1, column=0, pady=5)
        self.ydim.grid(row=1, column=1, pady=5)

        self.minLenLbl.grid(row=2, column=0, pady=5)
        self.minLen.grid(row=2, column=1, pady=5)

        self.maxLenLbl.grid(row=3, column=0, pady=5)
        self.maxLen.grid(row=3, column=1, pady=5)

        self.repeatsLbl.grid(row=4, column=0, pady=5)
        self.repeats.grid(row=4, column=1, pady=5)

        self.status.grid(row=5, column=0, columnspan=2)

        self.chsFldBtn.grid(row=6, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        self.stopBtn.grid(row=7, column=0, pady=5, padx=5, columnspan=2, sticky="nesw")

        # Labels that updates
        # self.text.set("Hello World!")

        # Be on top of everything
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.update()

        # Start the window
        self.window.mainloop()

    def statusUpdate(self, statusText):
        self.varStatus.set(statusText)

    def selectFolder(self):
        self.folder_selected = filedialog.askdirectory(title="Directory of the videos")
        print(self.folder_selected + "/")
        self.statusUpdate("Processing...")
        main(self.folder_selected + "/", self.xdim.get(), self.ydim.get(), self.minLen.get(), self.maxLen.get(),
             self.repeats.get())
        self.statusUpdate("Finished")


if __name__ == '__main__':
    windows = tkWin()
else:
    print("the random cut and concat gui version does not work as modules. thanks")