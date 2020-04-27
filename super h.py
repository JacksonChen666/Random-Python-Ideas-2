import logging
import threading
from multiprocessing import cpu_count


def writeH():
    with open("H.txt", "a") as h:
        while True:
            h.write("h")
            logging.debug("written 1 h")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] {%(threadName)s}: %(msg)s"
    )
    t = []
    for i in range(cpu_count() * 2):
        t.append(threading.Thread(target=writeH))
        logging.info("Starting thread {}".format(i + 1))
        t[i].start()
        logging.info("Started thread {}".format(i + 1))
