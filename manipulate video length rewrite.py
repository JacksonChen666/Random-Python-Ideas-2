SUPPORTED_FORMATS = ["mp4"]

loc_keywords = {"mp4": [b"mvhd"]}


class Video:
    def __init__(self, fileName: str, format: str = None, limit: int = 1024):
        self.fileName = fileName
        self._format = format or fileName.rpartition(".")[2].lower()
        self.duration, self.dur_loc = 0, 0
        self.time_scale, self.ts_loc = 0, 0
        self.seconds = 0
        self._limit = limit
        self.read_time(limit=limit, force=True)

    @staticmethod
    def _locate(text: bytes, start_loc: int, format: str):
        if format == "mp4":
            return text[text.index(loc_keywords["mp4"][0]) + start_loc:][:4]

    def _check(self, text: bytes, start_loc: int, format: str):
        if format == "mp4":
            return loc_keywords["mp4"][0] in text and len(self._locate(text, start_loc, format))

    def _read_duration(self, limit: int = 1024, force: bool = False):
        """Reads the duration of the video directly. Time scale is required to calculate the seconds"""
        if not (force or self.duration):
            return self.duration

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self._check(t, 20, self._format):
                t += f.read(64)
            if not self._check(t, 20, self._format):
                raise Exception("Not found")

        self.duration = int(self.from_hex(self._locate(t, 20, self._format)), 16)
        self.dur_loc = t.index(loc_keywords["mp4"][0]) + 20
        return self.duration

    def _read_time_scale(self, limit: int = 1024, force: bool = False):
        """Reads the time scale. Required to translate duration into seconds."""
        if not (force or self.time_scale):
            return self.time_scale

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self._check(t, 16, self._format):
                t += f.read(64)
            if not self._check(t, 16, self._format):
                raise Exception("Not found")

        self.time_scale = int(self.from_hex(self._locate(t, 16, self._format)), 16)
        self.ts_loc = t.index(loc_keywords["mp4"][0]) + 16
        return self.time_scale

    def __modify(self, seconds: int or bytes, loc: int, rewrite: bool = False):
        if type(seconds) != int and len(seconds) != 4:
            raise Exception("Input size incorrect")
        dur = self.to_hex_bytes(seconds * self.time_scale) if type(seconds) != bytes else seconds
        if rewrite:
            with open(self.fileName, "ab+") as f:
                f.seek(0)
                tmp = f.read()
                f.truncate(0)
                f.write(tmp[:loc] + dur + tmp[loc + 4:])
        else:
            with open(self.fileName, "ab+") as f:
                f.seek(loc)
                f.write(dur)
                f.seek(loc)
                if f.read(4) != dur:
                    print("Changes may have failed to apply. Reviewing...")
                    f.seek(f.tell() - 4)
                    if f.read(4) == dur:
                        print("Yep, changes are at the end. Truncating...")
                        f.truncate(f.tell() - 4)
        self.read_time(limit=self._limit, force=True)

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

    def read_time(self, limit: int = 1024, force: bool = False):
        if not (force or self.seconds):
            return self.seconds

        self._read_duration(limit=limit, force=force)
        self._read_time_scale(limit=limit, force=force)
        self.seconds = self.duration / self.time_scale
        return self.seconds

    def modify_time(self, duration: int or bytes, time_scale: int or bytes = None, rewrite: bool = False):
        """You can modify the time displayed"""
        if rewrite: print("Rewrite is enabled. This might take a while...")
        if time_scale: self.__modify(time_scale, self.ts_loc, rewrite=rewrite)
        if duration: self.__modify(duration, self.dur_loc, rewrite=rewrite)


if __name__ == '__main__':
    e = Video("mp4.mp4")
    print(e)
    e.modify_time(10, rewrite=True)
    e.read_time(force=True)
    print(e)
