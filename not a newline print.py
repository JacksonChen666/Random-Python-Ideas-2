from time import sleep

for i in range(10):
    print("\r{0}".format(i), end="", flush=True)
    sleep(0.5)
