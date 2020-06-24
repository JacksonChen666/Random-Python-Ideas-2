from os import walk, name
from re import search
from sys import argv, stderr
from time import time

if __name__ == '__main__':
    if len(argv) <= 1:
        stderr.writelines("Missing argument: Directory\n")
        dirChoice, notAllowed = None, None
        exit(1)
    else:
        dirChoice, intervals, notAllowed = argv[1], float(argv[2]) if len(
            argv) >= 3 else 0.01, f".*({'|'.join(argv[3:])}).*" if len(argv) >= 4 else ".*(\\\\.git|\\\\.gradle).*"

    dirs = []
    for root, firs, files in walk(dirChoice):
        if not search(notAllowed, root): dirs.append(root)
        if time() % 0.5 <= intervals: print(f"Current amount of directories: {len(dirs)}", end="\r", flush=True)

    print(f"Current amount of directories: {len(dirs)}\nGetting deepest directory...")
    dir_sep = "/" if name != "nt" else "\\"
    deepest_dir = max(dirs, key=lambda s: s.count(dir_sep))
    shortest_dir = min(dirs, key=lambda s: s.count(dir_sep))
    print("The deepest dir is " + deepest_dir)
    print("The shortest dir is " + shortest_dir)
    print(f"The deepest dir is {deepest_dir.count(dir_sep)} dir long")
    print(f"The shortest dir is {shortest_dir.count(dir_sep)} dir long")
