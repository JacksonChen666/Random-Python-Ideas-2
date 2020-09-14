"""ffmpeg -r 60 -f image2 -i frame%06d.jpg out.mp4"""
import os
import shutil

import numpy as np
from PIL import Image
from progress.bar import IncrementalBar

if os.path.exists("images"):
    shutil.rmtree("images")

os.mkdir("images")
os.chdir("images")

size = (int(input("Width of images: ")), int(input("Height of images: ")))
imagesAmount = int(input("Amount of frames to create: "))

with IncrementalBar("Creating images...", max=imagesAmount,
                    suffix="%(index)d/%(max)d images (%(elapsed_td)s/%(eta_td)s | avg %(avg)f item/second)") as bar:
    for i in range(imagesAmount):
        # bruh this (https://stackoverflow.com/a/59056944/13104233) is much better than acutally making the random module do it
        arr = np.random.randint(low=0, high=255, size=(size[0], size[1], 3))
        im = Image.fromarray(arr.astype('uint8'))
        im.save(f"frame{str(i).zfill(6)}.jpg")
        bar.next()
