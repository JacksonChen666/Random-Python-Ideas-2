SUPPORTED_FORMATS = ["mp4"]

loc_keywords = {"mp4": [b"mvhd"]}


class Video:
    def __init__(self, fileName, format=None, limit=1024):
        self.fileName = fileName
        self.format = format or fileName.rpartition(".")[2].lower()
        self.duration, self.dur_loc = 0, 0
        self.time_scale, self.ts_loc = 0, 0
        self.read_time_scale(limit=limit, force=True)
        self.read_duration(limit=limit, force=True)
        self.seconds = self.duration / self.time_scale

    def read_duration(self, limit=1024, force=False):
        """Rads the duration of the video directly. Time scale is required to calculate the seconds"""

        def locate(format=self.format):
            if format == "mp4":
                return t[t.index(loc_keywords["mp4"][0]) + 20:][:4]

        def check(format=self.format):
            if format == "mp4":
                return not (loc_keywords["mp4"][0] in t and len(locate(format)))

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and check():
                t += f.read(64)

        self.duration = int(self.from_hex(locate()), 16)
        self.dur_loc = t.index(loc_keywords["mp4"][0]) + 20
        return self.duration

    def read_time_scale(self, limit=1024, force=False):
        """Reads the time scale. Required to translate duration into seconds."""

        def locate(format=self.format):
            if format == "mp4":
                return t[t.index(loc_keywords["mp4"][0]) + 16:][:4]

        def check(format=self.format):
            if format == "mp4":
                return not (loc_keywords["mp4"][0] in t and len(locate()) == 4)

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and check():
                t += f.read(64)

        self.time_scale = int(self.from_hex(locate()), 16)
        self.ts_loc = t.index(loc_keywords["mp4"][0]) + 16

    @staticmethod
    def to_hex_bytes(_int):
        """267507 or 0x000414f3 = b'\x00\x04\x14\xf3'"""
        return int(_int).to_bytes(4, "big", signed=True)

    @staticmethod
    def from_hex(text):
        """b'\x00\x04\x14\xf3' = 0x000414f3"""
        return '0x' + text.hex()

    def __int__(self):
        return int(self.seconds)

    def __float__(self):
        return float(self.seconds)

    def __str__(self):
        return str(self.seconds)


if __name__ == '__main__':
    e = Video("mp4.mp4", limit=541232451425)
    print(e)
