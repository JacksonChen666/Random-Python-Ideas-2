SUPPORTED_FORMATS = ["mp4"]

loc_keywords = {"mp4": [b"mvhd"]}


class Video:
    def __init__(self, fileName, format=None, limit=1024):
        self.fileName = fileName
        self.format = format or fileName.rpartition(".")[2].lower()
        self.duration, self.dur_loc = 0, 0
        self.time_scale, self.ts_loc = 0, 0
        self.seconds = 0
        self.read_time(limit=limit, force=True)

    @staticmethod
    def locate(text, start_loc, format):
        if format == "mp4":
            return text[text.index(loc_keywords["mp4"][0]) + start_loc:][:4]

    def check(self, text, start_loc, format):
        if format == "mp4":
            return loc_keywords["mp4"][0] in text and len(self.locate(text, start_loc, format))

    def _read_duration(self, limit=1024, force=False):
        """Reads the duration of the video directly. Time scale is required to calculate the seconds"""
        if not (force or self.duration):
            return self.duration

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self.check(t, 20, self.format):
                t += f.read(64)
            if not self.check(t, 20, self.format):
                raise Exception("Not found")

        self.duration = int(self.from_hex(self.locate(t, 20, self.format)), 16)
        self.dur_loc = t.index(loc_keywords["mp4"][0]) + 20
        return self.duration

    def _read_time_scale(self, limit=1024, force=False):
        """Reads the time scale. Required to translate duration into seconds."""
        if not (force or self.time_scale):
            return self.time_scale

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self.check(t, 16, self.format):
                t += f.read(64)
            if not self.check(t, 16, self.format):
                raise Exception("Not found")

        self.time_scale = int(self.from_hex(self.locate(t, 16, self.format)), 16)
        self.ts_loc = t.index(loc_keywords["mp4"][0]) + 16
        return self.time_scale

    def read_time(self, limit=1024, force=False):
        if not (force or self.seconds):
            return self.seconds

        self._read_duration(limit=limit, force=force)
        self._read_time_scale(limit=limit, force=force)
        self.seconds = self.duration / self.time_scale
        return self.seconds

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
    e = Video("mp4.mp4")
    print(e)
