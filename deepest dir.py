import os
from time import time
from sys import argv

if not len(argv) >= 2:
    print("Directory pls")
    exit(513)
everything, dirChoice = [], argv[1]
sTime = time()
for root, dirs, files in os.walk(dirChoice):
    everything.append(root)
    if (time() - sTime) % 0.5 <= 0.0088: print(f"Current amount of directories: {len(everything)}", end="\r", flush=True)
print(f"Getting deepest directory of {len(everything)} directories...")
deepest = max(everything, key=lambda txt: txt.count(os.path.sep))
print(f'Out of {len(everything)} directories, the deepest directory is {"the chosen one" if deepest == dirChoice else f"{deepest}"}')
