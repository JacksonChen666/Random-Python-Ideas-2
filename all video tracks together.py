# use ffmpeg to combine all the videos and audios into one video
# this makes the command
import os
import re

vidFormat = "mp4"
output = "output." + vidFormat
os.chdir("/Users/jackson/Desktop/Everything/Pending/bill wurtz music")
vid = [i for i in os.listdir() if i.endswith(vidFormat)]
try: vid.remove(output)
except ValueError: pass
command = ["ffmpeg", "-loglevel", "panic", "-stats", "-hide_banner"]
for i in vid:
    # temp = re.sub(r"([\" '()])", r"\\\1", i)
    temp = re.sub(r"([^\w\d.])", r"\\\1", i)
    command.extend(["-i", f"{temp}"])
for i in range(len(vid)): command.extend(["-map", f"{i}:0", "-map", f"{i}:1"])
command.extend(["-c", "copy", output])
command = " ".join(command)
print(command)
