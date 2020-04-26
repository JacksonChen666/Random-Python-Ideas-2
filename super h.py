import atexit


def writeH():
    with open("H.txt", "a") as h:
        while True:
            h.write(
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
                "hhhhhhhhhh"
            )
            logging.debug("written 100 h")


@atexit.register
def delH():
    from os import remove
    remove("H.txt")
    logging.info("Deleted file")
    exit()


if __name__ == '__main__':
    from multiprocessing import cpu_count
    import threading
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] {%(threadName)s}: %(msg)s"
    )
    t = []
    cpuAmount = cpu_count()
    for i in range(cpuAmount * 2):
        t.append(threading.Thread(target=writeH))
        logging.info("Starting thread {}".format(i))
        t[i].start()
        logging.info("Started thread {}".format(i))
