# variables: total time, max clip time, file name, repeat thru list how many times, both dimensions
# modules: random, moviepy, youtube_dl
# maybe also make this into a module
# video length: https://www.reddit.com/r/moviepy/comments/2bsnrq/is_it_possible_to_get_the_length_of_a_video/cj8iqg7
# ?utm_source=share&utm_medium=web2x
# video cut: https://stackoverflow.com/questions/37317140/cutting-out-a-portion-of-video-python
# moviepy doc: https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html
# asks for channel URL
# asks for directory save
# download from youtube_dl: https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
import random, moviepy, youtube_dl

total_time = int
max_clip_time = int
folder = str
repeat = int
fileExtentions = [".mp4", '.mkv', '.webm']


def script():
    global total_time, max_clip_time, folder, repeat
    total_time = int(input("Total Video Time:\n"))
    max_clip_time = int(input("Max time for random clips:\n"))
    folder = input("Directory of clips:\n")
    repeat = int(input("Repeat thru clips times:\n"))
    videos = getFiles(folder, fileExtentions)
    print(videos)


def module():
    pass


def getFiles(directory, extensions):
    import os
    file = []
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            for i in extensions:
                if i in file:
                    file.append(os.path.join(r, file))

    for f in files:
        files.append(file)
    return files


if __name__ == '__main__':
    script()
else:
    module()
