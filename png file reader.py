import os
from sys import argv


class PNG:
    def __init__(self, filename):
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            exit(1)
        self._filename = filename
        if not self._checkValidPNG():
            print("The file you provided is not a PNG file.")
            exit(1)
        self._getIHDRChunk()

    def _checkValidPNG(self):
        with open(self._filename, "rb") as f:
            return f.read(8) == b"\x89PNG\x0D\x0A\x1A\x0A"

    def _getIHDRChunk(self):
        with open(self._filename, "rb") as f:
            f.seek(8)
            self.IHDRChunkLength = int(f.read(4).hex(), 16)
            self.IHDRChunkType = f.read(4)
            self.IHDRChunkData = f.read(self.IHDRChunkLength)
            self.IHDRChunkCRCValue = int(f.read(4).hex(), 16)


if __name__ == '__main__':
    if len(argv) - 1 < 1:
        print("Not enough arguments")
        exit(1)
    else:
        photo = PNG(argv[1])
