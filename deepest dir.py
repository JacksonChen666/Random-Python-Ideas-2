#!/usr/bin/env python3
import os
from time import time

everything = []
i = 0
sTime = time()
dirChoice = "/"
for root, dirs, files in os.walk(dirChoice):
    everything.append(root)
    i += 1
    if (time() - sTime) % 0.5 <= 0.0088: print(f"Current amount of directories: {str(i)}", end="\r", flush=True)
print(f"Getting deepest directory of {str(i)} directories...")
deepest = max(everything, key=lambda txt: txt.count("/"))
if deepest == dirChoice:
    print(f"Out of {len(everything)} directories, the deepest directory is the chosen one")
else:
    print(f"Out of {len(everything)} directories, the deepest directory is \n{deepest}")
