import atexit
import logging
import random
import threading

from PIL import Image, ImageDraw

width = 1920
height = 1080
colors = ["white", "black"]
images = []
amountOfImages = 5
t = []


def randomImage(threadNum):
    global images, colors
    random.seed(random.randint(0, 999999999))
    logging.debug("Thread {}:Set random seed".format(threadNum))
    with Image.new("RGB", (width, height), "black") as img:
        draw = ImageDraw.Draw(img)
        logging.debug("Thread {}:Created new image".format(threadNum))
        for y in range(height):
            for x in range(width):
                logging.debug("Thread {}:Drawing at pixel {}x{}".format(threadNum, x, y))
                color = random.choice(colors)
                draw.point((x, y), color)
    images.append(img)
    logging.info("Thread {}:Finished".format(threadNum))


@atexit.register
def save():
    global images
    logging.info("Thread 0:All thread finished")
    try:
        images[0].save('Random Colors.gif', save_all=True, append_images=images[1:], optimize=False,
                       duration=amountOfImages / 2, loop=0)
    except IndexError:
        logging.exception("Main: Failed to save image due to IndexError (Most likely there's no images ever generated)")
        exit()
    logging.info("Thread 0:Saved image")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='random images.log', filemode="w")
    for i in range(amountOfImages):
        t.append(threading.Thread(target=randomImage, args=str(i + 1)))
        t[i].start()
        logging.info("Thread 0:Started Thread {}".format(i + 1))
