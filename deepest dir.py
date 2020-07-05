import os
from time import time

everything, dirChoice = [], "/Users/Jackson/Desktop"
sTime = time()
for root, dirs, files in os.walk(dirChoice):
    everything.append(root)
    if (time() - sTime) % 0.5 <= 0.0088: print(f"Current amount of directories: {len(everything)}", end="\r", flush=True)
print(f"Getting deepest directory of {len(everything)} directories...")
deepest = max(everything, key=lambda txt: txt.count("/"))
if deepest == dirChoice:
    print(f"Out of {len(everything)} directories, the deepest directory is the chosen one")
else:
    print(f"Out of {len(everything)} directories, the deepest directory is \n{deepest}")
