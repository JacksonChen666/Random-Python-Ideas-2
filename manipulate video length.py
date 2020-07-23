"""This python program can manipulate video length by directly modifying the metadata of the video. Inspired by
FlyTech's video (https://youtu.be/UxHQ7dW6M2s)

Supported formats:
mp4
"""
from platform import system

from cv2 import CAP_PROP_FPS, VideoCapture

SUPPORTED_FORMATS = ["mp4"]

# mp4: find this thing, then go 4 bytes (mvhd), 16 bytes ahead and read 4 bytes. those 4 bytes are the duration.
# webm: find the TimestampScale property, and then find the duration and read 4 bytes. this is FlyTech's method.
keywords = {"mp4": [b"mvhd"]}


class Exceptions(Exception):
    pass


class UnsupportedFormat(Exceptions):
    """I don't know how this format works"""
    def __init__(self, message=None, format=None):
        super().__init__(message or "Unsupported format. Please check if you have chosen the format correctly", format)


class NotFound(Exceptions):
    def __init__(self, message=None):
        """Check your source video file. Can you see a preview? Can you play it not via VLC?"""
        super().__init__(message or "Information not found in video. Try setting a higher limit or 0.")


class InputTooShort(Exceptions):
    def __init__(self, message=None):
        """Check your inputs. This is a protection against video corruption."""
        super().__init__(message or "Please check your inputs.")


class Video:
    def __init__(self, fileName, format=None, limit=1024):
        """Initializations. Should've already read the durations."""
        self.fileName = fileName
        self.format = format or fileName.rpartition(".")[2].lower()
        self.format = self.format.lower()
        if not any([f in self.format for f in SUPPORTED_FORMATS]):
            raise UnsupportedFormat(format=self.format)
        self.second = VideoCapture(self.fileName).get(CAP_PROP_FPS) * 1000
        self.duration, self.durLocation = None, None
        self.time_scale, self.tsLoc = None, None
        self.read_duration(force=True, limit=limit)
        self.read_time_scale(force=True, limit=limit)

    def read_duration(self, limit=1024, force=False):
        """Reads the duration of the video file directly. 1 second is 1000 * Video FPS"""
        if not force and self.duration is not None:
            return self.duration

        def tb(format=self.format):
            if format == "mp4":
                return t[t.index(keywords["mp4"][0]) + 20:][:4]

        def ch(format=self.format):
            if format == "mp4":
                return not (keywords["mp4"][0] in t and len(tb()) == 4)
            else:
                raise UnsupportedFormat(format=format)

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and ch():
                t += f.read(64)
            if ch():
                raise NotFound

        self.duration = int(from_hex(tb()), 16) / self.second
        self.durLocation = t.index(keywords["mp4"][0]) + 20
        return self.duration

    def modify_duration(self, seconds, rewrite=False, byteString=False):
        """
        Changes the duration of the video to make it seem longer than it is.
        You can also use hex to replicate it in the file as python syntax.
        There are some limitations:
        You cant go above python's int limit. The real number is Chosen length * Video FPS.

        Workaround:
        make a byte string like '\xff\xff\xf1\xf0' (0xfffff1f0), and enable byteString
        """
        if type(seconds) != int and len(seconds) != 4:
            raise InputTooShort
        if type(seconds) == bytes:
            byteString = True
        if self.duration is None or self.durLocation is None:
            self.read_duration()
        dur = to_hex_bytes(seconds * self.second) if not byteString else seconds
        if rewrite or system() == "Darwin":  # according to open help, some systems will append no matter what.
            print("Rewrite is enabled. This might take a while...")
            with open(self.fileName, "rb") as f:
                tmp = f.read()
            with open(self.fileName, "wb") as f:
                f.write(tmp[:self.durLocation] + dur + tmp[self.durLocation + 4:])
        else:
            with open(self.fileName, "ab") as f:
                f.seek(self.durLocation)
                f.write(dur)
                if f.read(4) != dur:
                    print("Changes may not be applied. Use rewrite if not working. Reverting changes...")
                    f.seek(f.tell() - 4)
                    if f.read() == dur:
                        print("Confirmed: Changes are at the end of file.")

    def read_time_scale(self, limit=1024, force=False):
        """Reads the duration of the video file directly. 1 second is 1000 * Video FPS"""
        if not force and self.time_scale is not None:
            return self.time_scale

        def tb(format=self.format):
            if format == "mp4":
                return t[t.index(keywords["mp4"][0]) + 16:][:4]

        def ch(format=self.format):
            if format == "mp4":
                return not (keywords["mp4"][0] in t and len(tb()) == 4)
            else:
                raise UnsupportedFormat(format=format)

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and ch():
                t += f.read(64)
            if ch():
                raise NotFound

        self.time_scale = int(from_hex(tb()), 16)
        self.tsLoc = t.index(keywords["mp4"][0]) + 16
        return self.time_scale

    def modify_time_scale(self, time_scale, rewrite=False):
        """
        Changes the duration of the video to make it seem longer than it is.
        You can also use hex to replicate it in the file as python syntax.
        There are some limitations:
        You cant go above python's int limit. The real number is Chosen length * Video FPS.

        Workaround:
        make a byte string like '\xff\xff\xf1\xf0' (0xfffff1f0), and enable byteString
        """
        if type(time_scale) != int and len(time_scale) != 4:
            raise InputTooShort
        if self.time_scale is None or self.tsLoc is None:
            self.read_time_scale()
        if rewrite or system() == "Darwin":  # according to open help, some systems will append no matter what.
            print("Rewrite is enabled. This might take a while...")
            with open(self.fileName, "rb") as f:
                tmp = f.read()
            with open(self.fileName, "wb") as f:
                f.write(tmp[:self.tsLoc] + time_scale + tmp[self.tsLoc + 4:])
        else:
            with open(self.fileName, "ab") as f:
                f.seek(self.tsLoc)
                f.write(time_scale)
                if f.read(4) != time_scale:
                    print("Changes may not be applied. Use rewrite if not working. Reverting changes...")
                    f.seek(f.tell() - 4)
                    if f.read() == time_scale:
                        print("Confirmed: Changes are at the end of file.")

    def __str__(self):
        return str(self.duration)

    def __int__(self):
        return int(self.duration)

    def __float__(self):
        return float(self.duration)


def to_hex_bytes(_int):
    """267507 or 0x000414f3 = b'\x00\x04\x14\xf3'"""
    return int(_int).to_bytes(4, "big", signed=True)


def from_hex(text):
    """b'\x00\x04\x14\xf3' = 0x000414f3"""
    return '0x' + text.hex()


if __name__ == '__main__':
    print("Use this as an module. I don't have that much time for a cli interface, yet.\n"
          "Module usage: module.Video(\"Video name.mp4\").modify_duration(1000)")
    # th = Video("mp4.mp4")
    # temp = th.read_duration()
    # print(temp)
    # th.modify_duration(4 * 60 + 20)
    # print(th.read_duration(force=True))
