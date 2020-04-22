# refer to random cut and concat GUI version for perfect example
import os

directory = str(input("Directory:\n"))
videos = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.join(directory, f).endswith(
    ('.mp4', '.mkv', '.webm', '.mov', '.flv', '.avi', '.m4a', '.m4v', '.f4v', '.f4a', '.m4b')) and
          os.path.isfile(os.path.join(directory, f)) and f != "FINAL.MP4"]

print(videos)
