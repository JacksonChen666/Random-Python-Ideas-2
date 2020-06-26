#!/usr/bin/env python3
import hashlib
import logging
import os
from re import IGNORECASE, search
from sys import argv, stderr, stdout

logging.basicConfig(level=logging.INFO, stream=stdout)
files = logging.getLogger("duplicates.files")
sizes = logging.getLogger("duplicates.sizes")
hashing = logging.getLogger("duplicates.hash")
non_dupe = logging.getLogger("duplicates.non_duplicates")
allow_delete = True

if os.name == 'nt':
    import msvcrt


    def g():
        return msvcrt.g().decode()
else:
    import sys, tty, termios

    fd = sys.stdin.fileno()
    try:
        old_settings = termios.tcgetattr(fd)
    except termios.error:
        allow_delete = False


    def g():
        try:
            tty.setraw(sys.stdin.fileno()); ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        s = ch
        return s


def find_files(cDir):
    temp = []
    for root, dirs, filez in os.walk(cDir):
        for f in filez:
            path = os.path.realpath(os.path.join(root, f))
            if not search(r".*(\.git|\.DS_Store|desktop\.ini|\.idea).*", path, IGNORECASE):
                temp.append(path)
                files.debug(f"File found: {path}")
            else:
                files.debug("Excluded file/folder found in path/file, excluding")
    return temp


def get_file_sizes(filez):
    fileSizeE = {}
    for file in filez:
        try:
            fileSizeE[file] = os.path.getsize(file)
            sizes.debug(f"File size of {file} is {fileSizeE[file]} bytes")
        except OSError:
            filez.remove(file)  # no this isn't delete file
            sizes.error("No permission, or file not found")
            continue
    return fileSizeE


def remove_non_duplicates(inp):
    non_dupe.info("Removing non-duplicates...")
    list1 = list(inp.keys())  # {"this": "not this"}
    list2 = list(inp.values())  # {"not this": "this"}
    for item in list2:
        ind = list2.index(item)
        if ind == 1:
            non_dupe.debug(f"{list1[ind]} is not a duplicate")
            del list1[ind], list2[ind]
    return dict(zip(list1, list2))  # to tuples then back to dict


def get_hash(fileName, size=1024):
    with open(fileName, "rb") as f: text = f.read(size) if size > 0 else f.read()
    hashes = hashlib.sha1(text).hexdigest()
    hashing.debug(f"Hash for {fileName} is {hashes}")
    return hashes


def get_file_hashes(filesList, size=1024):
    fileHashesTemp = {}
    for f in filesList: fileHashesTemp[f] = get_hash(f, size)
    return fileHashesTemp


def duplicate_finalizing(fileHash: dict):
    tDict = {}
    for i in list(fileHash.items()):
        try:
            tDict[i[1]] += (i[0],)
        except KeyError:
            tDict[i[1]] = (i[0],)
    for i in list(tDict.items()):  # delete all with no duplicates
        if len(i[1]) == 1: del tDict[i[0]]
    return tDict


def print_dupes(dicts: dict):
    for key in dicts: yield f"{dicts[key][0]} is a duplicate of {dicts[key][-1]}" if len(dicts[key]) == 2 else " ".join(
        [dicts[key][0], "is a duplicate of", ", ".join(dicts[key][1:-1]), "and", dicts[key][-1]]), dicts[key][0]
    print(f"{str(len(dicts)) if len(dicts) != 0 else 'No'} duplicates found.")


def delete_files(filesList):
    if allow_delete:
        asking = True
        for i in filesList:
            if asking:
                print(f"Would you like to remove {i[1:]}? Original: {i[0]} [y/N]")
                choice = g()
            else:
                choice = "Y"
            if choice == "y":
                for f in i[1:]: os.remove(f)
            elif choice == "Y":
                asking = False
                for f in i[1:]: os.remove(f)
            elif choice == "N" or ord(choice) == 3:
                break


def main():
    sDir = ""
    if argv[1:]:
        sDir = argv[1]
    else:
        stderr.writelines("You need to specify a directory!")
        exit(1)

    logging.info("Finding files...")
    filez: list = find_files(sDir)
    logging.info(f"There are {len(filez)} files")

    logging.info("Getting all file sizes...")
    fileSizes = get_file_sizes(filez)
    fileSizes = remove_non_duplicates(fileSizes)
    filez = list(fileSizes.keys())
    logging.info(f"There are {len(filez)} files left")

    logging.info("Getting part-file hashes...")
    fileHashes = get_file_hashes(filez)  # get partly hash
    fileHashes = remove_non_duplicates(fileHashes)
    filez = list(fileHashes.keys())
    logging.info(f"There are {len(filez)} files left")

    logging.info("Getting full-file hashes...")
    fileHashes = get_file_hashes(filez, -1)  # get entire hash
    fileHashes = remove_non_duplicates(fileHashes)
    filez = list(fileHashes.keys())
    logging.info(f"There are {len(filez)} files left")

    logging.info("Finalizing...")
    duplicates = duplicate_finalizing(fileHashes)
    filez.clear()
    for f in print_dupes(duplicates):
        print(f[0])
        filez.extend(f[1])
    delete_files(filez)


if __name__ == '__main__':
    main()
