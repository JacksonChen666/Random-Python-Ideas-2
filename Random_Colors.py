import atexit
import logging
import random
import threading
from math import pow

from PIL import Image, ImageDraw

width = 1920
height = 1080
fps = 30
colors = ["white", "black"]
images = []
amountOfImages = 10
threads = []


def randomImage():
    global images, colors
    logging.debug("Setting random seed...")
    random.seed(random.randint(0, 999999999))
    logging.debug("Set random seed")
    logging.debug("Creating new image")
    with Image.new("RGB", (width, height), "black") as img:
        logging.debug("Created new image")
        draw = ImageDraw.Draw(img)
        for y in range(height):
            for x in range(width):
                color = random.choice(colors)
                draw.point((x, y), color)
                logging.debug("{} x {}\tis {}".format(x + 1, y + 1, color))
    logging.debug("Adding image to list...")
    images.append(img)
    logging.debug("Added image to list")
    logging.info("Finished")
    return img


@atexit.register
def saveGif():
    logging.info("All {} threads finished".format(amountOfImages))
    try:
        logging.info("Saving image...")
        images[0].save('Random Colors.gif', save_all=True, append_images=images[1:], optimize=False, fps=fps, loop=0)
        logging.info("Saved image")
    except IndexError:
        logging.exception("Failed to save image due to IndexError (Most likely there's no images ever "
                          "generated)")
        exit()
    if __name__ == '__main__':
        readLog()
    return images


def startup(widths=width, heights=height, frames=amountOfImages, fpsz=fps, loggingLevel=logging.INFO):  # do it all
    # at the same time
    setup(widths=widths, heights=heights, frames=frames, fpsz=fpsz, loggingLevel=loggingLevel)
    for i in range(amountOfImages):
        threads.append(threading.Thread(target=randomImage))
        threads[i].start()
        logging.info("Started Thread-{}".format(i + 1))
    logging.info("All {} threads started".format(amountOfImages))


def startup2(widths=width, heights=height, frames=amountOfImages, fpsz=fps, loggingLevel=logging.INFO):  # do it
    # individually
    setup(widths=widths, heights=heights, frames=frames, fpsz=fpsz, loggingLevel=loggingLevel)
    for i in range(amountOfImages):
        randomImage()


def setup(widths=width, heights=height, frames=amountOfImages, fpsz=fps, loggingLevel=logging.INFO):
    global threads, width, height, amountOfImages, fps
    logging.basicConfig(
        level=loggingLevel,
        format="%(asctime)s [%(levelname)s] {%(threadName)s}: %(msg)s",
        filename="random colors.log",
        filemode="w"
    )
    width = widths
    height = heights
    amountOfImages = frames
    fps = fpsz


def readLog():
    with open("random colors.log") as f:
        print(
            "Log format: `Year-Month-Day Hour:Min:Sec,MS [Level] Thread name: Message`\nLog:\n{}".format(f.read()))
    return


if __name__ == '__main__':
    startup(frames=10, fpsz=1, loggingLevel=logging.DEBUG)
