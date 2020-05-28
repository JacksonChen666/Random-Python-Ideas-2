import atexit
import logging
import random
import threading

from PIL import Image, ImageDraw

width = 1920
height = 1080

colors = []
for q in range(10):
    colors.append(random.choice(['white', 'black']))
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
        images[0].save('Random Colors.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)
        logging.info("Saved image")
    except IndexError:
        logging.exception("Failed to save image due to IndexError (Most likely there's no images ever "
                          "generated)")
        exit()
    return images


def startup(widths=width, heights=height, frames=amountOfImages, loggingLevel=logging.INFO):  # do it all
    # at the same time
    setup(widths=widths, heights=heights, frames=frames, loggingLevel=loggingLevel)
    for i in range(amountOfImages):
        threads.append(threading.Thread(target=randomImage))
        threads[i].times()
        logging.info("Started Thread-{}".format(i + 1))
    logging.info("All {} threads started".format(amountOfImages))
    TIA = True
    while TIA:
        for i in threads:
            if i.is_alive():
                TIA = True
                continue
            else:
                TIA = False
        for t in range(len(threads)):
            logging.info('Joining thread-{}'.format(t + 1))
            threads[t].join()
            logging.info("Left thread-{}".format(t + 1))


def startup2(widths=width, heights=height, frames=amountOfImages, loggingLevel=logging.INFO):  # do it
    # individually
    setup(widths=widths, heights=heights, frames=frames, loggingLevel=loggingLevel)
    for i in range(amountOfImages):
        randomImage()


def setup(widths=width, heights=height, frames=amountOfImages, loggingLevel=logging.INFO):
    global threads, width, height, amountOfImages
    logging.basicConfig(
        level=loggingLevel,
        format="%(asctime)s [%(levelname)s] {%(threadName)s}: %(msg)s",
        # filename="random colors.log",
        # filemode="w"
    )
    width = widths
    height = heights
    amountOfImages = frames


if __name__ == '__main__':
    startup(1024, 1024, frames=30)
