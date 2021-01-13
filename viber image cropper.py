import os

from PIL import Image, UnidentifiedImageError
import time


def process_img(filename: str, new_filename: str):
    try:
        im = Image.open(filename)
    except UnidentifiedImageError:
        print("wtf is that")
        return
    if im.size != (1242, 2208):
        print(f"Not original size")
        return False
    if os.path.exists(new_filename):
        print(f"Already cropped")
        return False
    im = im.crop((0, 194, im.size[0], im.size[1] - 395))
    color = (255,) * 3
    x, y = 166, im.height
    # check x from left to right, all must be black
    while True:
        while sum(color[:-1]) != 0:
            y -= 1
            if y < 1:
                print("Failed to find starting point")
                return
            color = im.getpixel((x, y))
        works = True
        for x2 in range(1, im.width):
            if sum(im.getpixel((x2, y))[:-1]):
                works = False
                break
        if works:
            break
        else:
            y -= 1
            if y < 1:
                print("Failed to find starting point")
                return
    y2 = y
    color = (255,) * 3
    while True:
        while sum(color[:-1]) == 0:
            y2 -= 1
            if y2 < 1:
                print("Failed to find ending point")
                return
            color = im.getpixel((x, y2))
        works = True
        for x2 in range(1, im.width):
            if sum(im.getpixel((x2, y2))[:-1]):
                works = False
                break
        if works:
            break
        else:
            y2 -= 1
            if y2 < 1:
                print("Failed to find starting point")
                return
    y -= int((y - y2) / 2)
    im = im.crop((0, 0, im.width, y))
    im.save(new_filename)
    return im


if not os.path.exists("viber new"):
    os.mkdir("viber new")

start = time.time()
try:
    for i in os.listdir("viber"):
        path = os.path.join("viber", i)
        if os.path.exists(path):
            print(path, end="... ")
            temp = i.rpartition(".")
            new_name = f"viber new{os.path.sep}{temp[0]}-crop.{temp[2]}"
            temp = time.time()
            if process_img(path, new_name):
                temp2 = time.time()
                print(f"Done in {round(temp2 - temp, 2)} seconds")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    end = time.time()
    print(f"Finished in {round(end - start, 2)} seconds")
