import traceback as tb

def writeH():
    with open("/Volumes/Jackson/H.txt", "a+") as h:
        hs = "H"
        for i in range(30):
            hs += hs
        print("Starting point: {}".format(len(hs)))
        while True:
            try:
                h.write(hs)
                print("Written {} Hs".format(len(hs)))
                hs = hs + hs[:int(len(hs) / 8)] if 4000000000 >= len(hs) >= 0 else "HHHHHHHH"
            except:
                print("Before: {}".format(len(hs)), end=" ")
                hs = hs[:int(len(hs) / 2)] if len(hs) > 0 else hs
                print("After: {}".format(len(hs)))
                tb.print_exc()
                pass


if __name__ == '__main__':
    writeH()
