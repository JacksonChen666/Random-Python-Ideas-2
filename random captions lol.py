#!/usr/bin/env python3
import random
import re

n = "\n"
startTime = "0:00:00.000"
endTime = "0:00:30.000"
with open("caption.sbv", "w") as f:
    toWrite = f"{startTime},{endTime}\n"
    for line in range(1000):
        for letter in range(1000):
            while True:
                temp = random.randint(0, 0x110000 - 1)
                if not re.search(r"[\uD800-\uDFFF]", chr(temp)): break  # surrogate check
            toWrite += chr(temp)
        toWrite += "\n"
    f.write(toWrite)
