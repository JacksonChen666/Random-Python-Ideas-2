#!/usr/bin/env python3
import hashlib
import logging
import os
from collections import Counter
from re import IGNORECASE, search
from sys import argv, stderr, stdout

logging.basicConfig(level=logging.INFO, stream=stdout)
files = logging.getLogger("duplicates.files")
sizes = logging.getLogger("duplicates.sizes")
hashing = logging.getLogger("duplicates.hash")
non_dupe = logging.getLogger("duplicates.non duplicates")
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
            tty.setraw(sys.stdin.fileno());
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        s = ch
        return s


def find_files(cDir):
    temp = []
    for root, dirs, _files in os.walk(cDir):
        for f in _files:
            path = os.path.realpath(os.path.join(root, f))
            if not search(r".*(\.git|\.DS_Store|desktop\.ini|\.idea).*", path, IGNORECASE):
                temp.append(path)
                files.debug(f"File found: {path}")
                continue
            files.debug("Excluded file/folder found in path/file, excluding")
    return temp


def get_file_sizes(_files):
    fileSizeE = {}
    for file in _files:
        try:
            fileSizeE[file] = os.path.getsize(file)
            sizes.debug(f"File size of {file} is {fileSizeE[file]} bytes")
        except OSError:
            _files.remove(file)  # no this isn't delete file
            sizes.error("No permission, or file not found")
    return fileSizeE


def remove_non_duplicates(inp):
    non_dupe.info("Removing non-duplicates...")
    list1, list2 = list(inp.keys()), list(inp.values())
    counted = Counter(list2)
    temp1 = [i for i in list2 if counted[i] == 1]
    for i in temp1:
        i = list2.index(i)
        non_dupe.debug(f"{list1[i]} is not a duplicate")
        del list1[i], list2[i]
    return dict(zip(list1, list2))


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
    print(f"{len(dicts) if len(dicts) != 0 else 'No'} duplicates found.")


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
    def get_files_left(_files):
        if len(_files) > 0:
            get_files_left(_files)
        else:
            logging.info("There are no files left. Stopping.")
            exit(0)

    sDir = ""
    if argv[1:]:
        sDir = argv[1]
    else:
        stderr.writelines("You need to specify a directory!")
        exit(1)

    logging.info("Finding files...")
    _files: list = find_files(sDir)
    logging.info(f"There are {len(_files)} files")

    logging.info("Getting all file sizes...")
    fileSizes = get_file_sizes(_files)
    fileSizes = remove_non_duplicates(fileSizes)
    _files = list(fileSizes.keys())
    get_files_left(_files)

    logging.info("Getting part-file hashes...")
    fileHashes = get_file_hashes(_files)  # get partly hash
    fileHashes = remove_non_duplicates(fileHashes)
    _files = list(fileHashes.keys())
    get_files_left(_files)

    logging.info("Getting full-file hashes...")
    fileHashes = get_file_hashes(_files, -1)  # get entire hash
    fileHashes = remove_non_duplicates(fileHashes)
    _files = list(fileHashes.keys())
    get_files_left(_files)

    logging.info("Finalizing...")
    duplicates = duplicate_finalizing(fileHashes)
    _files.clear()
    for f in print_dupes(duplicates):
        print(f[0])
        _files.extend(f[1])
    delete_files(_files)


if __name__ == '__main__':
    main()
