#!/usr/bin/env python3
n = "\n"
time = "0:00:00.000,0:00:30.000" + n
with open("caption.sbv", "w") as f:
    f.write(time + ((" " * 10000 + n) * 10000) + n)
