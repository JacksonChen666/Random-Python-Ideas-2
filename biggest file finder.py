from os import path, walk
from sys import argv


def get_files(dirChoice):
    temp = {path.realpath(path.join(root, f)): path.getsize(path.join(root, f)) for root, dirs, _files in
            walk(dirChoice) for f in _files if ".DS_Store" not in f or "desktop.ini" not in f}
    # https://stackoverflow.com/a/613218/13104233
    temp2 = {k: v for k, v in sorted(temp.items(), key=lambda item: -item[1])}
    return temp2


# https://stackoverflow.com/a/52684562/13104233
def format_size(_path, unit="MB"):
    bit_shift = {"B": 0, "kb": 7, "KB": 10, "mb": 17, "MB": 20, "gb": 27, "GB": 30, "TB": 40}
    return int("{:,.0f}".format(path.getsize(_path) / float(1 << bit_shift[unit])))


if __name__ == '__main__':
    sizes = None
    if len(argv) == 1:
        print("Must provide a dir.")
        exit(1)
    elif not len(argv) >= 3:
        print("Must provide size.")
        exit(1)
    files = get_files(argv[1])
    size = int(argv[2])
    # use python 3.8 because https://stackoverflow.com/a/55881984/13104233
    # noinspection PyCompatibility
    print("\n".join([f"{i} is {fSize} MB" for i in files if (fSize := format_size(i)) >= size]))
