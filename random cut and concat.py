# videosEnt cut: https://stackoverflow.com/questions/37317140/cutting-out-a-portion-of-video-python
# download from youtube_dl: https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
# /users/jackson/desktop/everything/pending/random cut and concat attempts/videos/
directory = '/path/to/macos/ or C:\\path\\to\\windows\\'  # double backslash because in programming it means something
xdim = 1920
ydim = 1080
minLength = 0.05
maxLength = 5
repeats = 3

ext = "*"


def inputting():
    global directory, xdim, ydim, minLength, maxLength, repeats
    directory = input("Directory of the videos:\n")
    repeats = int(input("Repeat thru list how many times:\n"))
    xdim = int(input("Width of final videosEnt:\n"))
    ydim = int(input("Height of videosEnt:\n"))
    minLength = float(input("Min length of clips:\n"))
    maxLength = float(input("Max length of clips:\n"))
    main()


def main():
    global directory, xdim, ydim, ext, minLength, maxLength, repeats
    print("Importing...")
    from multiprocessing import cpu_count
    import moviepy.editor, os, random, fnmatch

    outputs = []
    print("Thread count of export process: {0}".format(str(cpu_count() * 2)), end="\n\n")
    # compile list of videos
    inputs = [os.path.join(directory, f) for f in os.listdir(directory) if
              os.path.isfile(os.path.join(directory, f)) and fnmatch.fnmatch(f, ext)]
    try:
        inputs.remove(directory + ".DS_Store")
        inputs.remove(directory + "[Tt]humb.db")
    except ValueError:
        pass
    for q in range(repeats):
        print("\rRepeating {0}/{1}".format(q + 1, repeats))
        random.shuffle(inputs)
        for i in inputs:
            print("\rCutting {0}".format(i), end="", flush=True)

            length = round(random.uniform(minLength, maxLength), 2)

            # import to moviepy
            clip = moviepy.editor.VideoFileClip(i).resize((xdim, ydim))

            # select a random time point
            start = round(random.uniform(0, clip.duration - length), 2)

            # cut a subclip
            out_clip = clip.subclip(start, start + length)

            outputs.append(out_clip)

    # combine clips from different videos
    print("\nConcatenating...")
    collage = moviepy.editor.concatenate_videoclips(outputs)
    print('Writing...\nThread count: ' + str(cpu_count() * 2))
    collage.write_videofile(directory + 'FINAL.MP4', verbose=False, logger=None, threads=cpu_count() * 2)
    print("\nDone")


if __name__ == '__main__':
    inputting()
