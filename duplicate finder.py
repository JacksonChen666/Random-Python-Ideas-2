import hashlib
import logging
import os
from collections import Counter
from sys import argv, stderr, stdout

logging.basicConfig(level=logging.INFO, stream=stdout)
files = logging.getLogger("duplicates.files")
sizes = logging.getLogger("duplicates.sizes")
hashing = logging.getLogger("duplicates.hash")
non_dupe = logging.getLogger("duplicates.non duplicates")


def find_files(cDir):
    temp = []
    for root, dirs, _files in os.walk(cDir):
        for f in _files:
            path = os.path.realpath(os.path.join(root, f))
            if any([i in path for i in [".git", ".DS_Store", "desktop.ini", ".idea"]]):
                files.debug("Excluded file/folder found in path/file, excluding")
                continue
            temp.append(path)
            files.debug(f"File found: {path}")
    return temp


def get_file_sizes(_files):
    fileSizeE = {}
    for file in _files:
        try:
            fileSizeE[file] = os.path.getsize(file)
            sizes.debug(f"File size of {file} is {fileSizeE[file]} bytes")
        except OSError:
            _files.remove(file)  # no this isn't delete file you idiot
            sizes.error("No permission, or file not found")
    return fileSizeE


def remove_non_duplicates(inp):
    non_dupe.info("Removing non-duplicates...")
    list1, list2 = list(inp.keys()), list(inp.values())
    counted = Counter(list2)
    for i in [i for i in list2 if counted[i] == 1]:
        i = list2.index(i)
        non_dupe.debug(f"{list1.pop(i)} is not a duplicate")
        del list2[i]
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


def main():
    def get_files_left(_files):
        idk = list(_files.keys())
        if len(idk) == 0:
            logging.info("There are no files left. Stopping.")
            exit(0)
        else:
            logging.info(f"There are {len(idk)} files left")
        return _files

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
    _files = get_files_left(remove_non_duplicates(get_file_sizes(_files)))

    logging.info("Getting part-file hashes...")
    _files = get_files_left(remove_non_duplicates(get_file_hashes(_files)))  # get partly hash

    logging.info("Getting full-file hashes...")
    fileHashes = get_files_left(remove_non_duplicates(get_file_hashes(_files, -1)))  # get entire hash

    logging.info("Finalizing...")
    dps = duplicate_finalizing(fileHashes)
    for key in dps:
        print(f"{dps[key][0]} is a duplicate of {dps[key][-1]}" if len(dps[key]) == 2 else " ".join(
            [dps[key][0], "is a duplicate of", ", ".join(dps[key][1:-1]), "and", dps[key][-1]]))
    print(f"{len(dps) if len(dps) != 0 else 'No'} duplicates found.")


if __name__ == '__main__':
    main()
