class Exceptions(BaseException):
    def __init__(self, message=None):
        """
        The Base exceptions for everything
        :param message: Message
        """
        super(Exceptions, self).__init__(message or "")


class InputSizeIncorrect(Exceptions):
    def __init__(self, message=None):
        """
        The given bytes string has the incorrect size to be written
        :param message: Message
        """
        super(InputSizeIncorrect, self).__init__(message or "Incorrect input size")


class NotFoundError(Exceptions):
    def __init__(self, message=None):
        """
        Data in the video file was not found.
        :param message: Message
        """
        super(NotFoundError, self).__init__(message or "Not found in file")


class UnsupportedFormat(Exceptions):
    def __init__(self, message=None, format=None):
        """
        The given format is unsupported.
        :param message: Message
        :param format: The unsupported video format
        """
        super(UnsupportedFormat, self).__init__(f"{message or 'Format not supported.'} Format: {format}")


class Video:
    def __init__(self, fileName: str, format: str = None, limit: int = 1024):
        """
        Read and write duration to the video file
        :param fileName: Video file name to read from
        :param format: Video format. Completely optional.
        :param limit: How many bytes to read maximum
        """
        self.fileName = fileName
        self._format = (format or fileName.rpartition(".")[2]).lower()
        self.duration, self.dur_loc = 0, 0
        self.time_scale, self.ts_loc = 0, 0
        self.seconds = 0
        self._limit = limit
        self.SUPPORTED_FORMATS = ["mp4"]
        self.loc_keywords = {"mp4": [b"mvhd"]}
        self.read_time(limit=limit, force=True)

    def _locate(self, text: bytes, start_loc: int, format: str):
        """
        Locate the data for duration or time scale
        :param text: The data in bytes
        :param start_loc: Starting location
        :param format: Video format
        :return: Bytes of data
        """
        if format == "mp4":
            return text[text.index(self.loc_keywords["mp4"][0]) + start_loc:][:4]
        else:
            raise UnsupportedFormat(format=format)

    def _check(self, text: bytes, start_loc: int, req_len: int, format: str):
        """
        Looks if the required data is in the text
        :param req_len:
        :param text: The text in bytes
        :param start_loc: Starting location
        :param format: Video format
        :return: Boolean for if it's found and works
        :raise: UnsupportedFormat if the format given is unsupported
        """
        if format == "mp4":
            return self.loc_keywords["mp4"][0] in text and len(self._locate(text, start_loc, format)) == req_len
        else:
            raise UnsupportedFormat(format=format)

    def _read_duration(self, limit: int = 1024, force: bool = False):
        """
        Reads the duration of the video directly. Time scale is required to calculate the seconds.
        :param limit: How many bytes to read maximum.
        :param force: Read the video file anyways if true.
        :return: The duration
        :raise: UnsupportedFormat if the format given is unsupported
        """
        if not (force or self.duration):
            return self.duration

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self._check(t, 20, 4, self._format):
                t += f.read(64)
            if not self._check(t, 20, 4, self._format):
                raise NotFoundError

        self.duration = int(self._from_hex(self._locate(t, 20, self._format)), 16)
        self.dur_loc = t.index(self.loc_keywords["mp4"][0]) + 20
        return self.duration

    def _read_time_scale(self, limit: int = 1024, force: bool = False):
        """
        Reads the time scale. Required to translate duration into seconds.
        :param limit: How many bytes to read maximum
        :param force: Read the video file anyways if true.
        :return: The time scale
        :raise: NotFoundError if the required data is not found.
        """
        if not (force or self.time_scale):
            return self.time_scale

        with open(self.fileName, "rb") as f:
            t = b""
            while (len(t) < limit or not limit) and not self._check(t, 16, 4, self._format):
                t += f.read(64)
            if not self._check(t, 16, 4, self._format):
                raise NotFoundError

        self.time_scale = int(self._from_hex(self._locate(t, 16, self._format)), 16)
        self.ts_loc = t.index(self.loc_keywords["mp4"][0]) + 16
        return self.time_scale

    def __modify(self, seconds: int or bytes, loc: int, time_scale: bool = False, data_len: int = 4,
                 rewrite: bool = False):
        """
        Modify in the file. If it finds that the changes are at the end instead, then it will rewrite.
        :param seconds: Some number or hex in bytes
        :param loc: Location of modified bytes
        :param time_scale: Modify the time scale. This is used to know if it's duration or time scale.
        :param data_len: Required data length to be directly written in bytes
        :param rewrite: Rewrite the entire file. May be needed for some system which adds to the end anyways.
        :return:
        :raise: InputSizeIncorrect if given bytes data is not equal to some length
        """
        if type(seconds) == bytes and len(seconds) != data_len:
            raise InputSizeIncorrect
        time = self._to_hex_bytes(seconds * self.time_scale if not time_scale else seconds) if type(
            seconds) != bytes else seconds
        if rewrite:
            with open(self.fileName, "ab+") as f:
                f.seek(0)
                tmp = f.read()
                f.truncate(0)
                f.write(tmp[:loc] + time + tmp[loc + 4:])
        else:
            with open(self.fileName, "ab+") as f:
                f.seek(loc)
                f.write(time)
                f.seek(loc)
                if f.read(4) != time:
                    print("Changes may have failed to apply. Rewriting...")
                    f.seek(f.tell() - 4)
                    maybe = f.read(4)
                    if maybe == time: f.truncate(f.tell() - 4)
                    self.__modify(seconds, loc, time_scale=time_scale, rewrite=True)
        self.read_time(limit=self._limit, force=True)

    @staticmethod
    def _to_hex_bytes(_int: int):
        """267507 or 0x000414f3 = b'\x00\x04\x14\xf3'"""
        return int(_int).to_bytes(4, "big", signed=True)

    @staticmethod
    def _from_hex(text: bytes):
        """b'\x00\x04\x14\xf3' = 0x000414f3"""
        return '0x' + text.hex()

    def __int__(self):
        """
        Returns seconds in int
        :return: int seconds
        """
        return int(self.seconds)

    def __float__(self):
        """
        Return seconds in float
        :return: float seconds
        """
        return float(self.seconds)

    def __str__(self):
        """
        Return seconds in str
        :return: str seconds
        """
        return str(self.seconds)

    def read_time(self, limit: int = 1024, force: bool = False):
        """
        Read the duration in seconds. If it's already done, return whatever it was.
        :param limit: How many bytes to read maximum
        :param force: Reread the duration, even if there is one already working
        :return: The duration (in seconds) in the video file.
        """
        if not (force or self.seconds):
            return self.seconds

        self._read_duration(limit=limit, force=force)
        self._read_time_scale(limit=limit, force=force)
        self.seconds = self.duration / self.time_scale
        return self.seconds

    def modify_time(self, duration: int or bytes, time_scale: int or bytes = None, rewrite: bool = False):
        """
        Modify the time displayed.
        The lower the time scale, the more time you can squeeze, but with less float precision.
        The higher the time scale, the more precise the seconds can be, but with less time.
        :param duration: The duration in seconds. Negative numbers maybe treated as positive. If given bytes string,
        it is directly written.
        :param time_scale: The time scale. This is required to calculate the seconds.
        :param rewrite: Rewrite the entire file. Maybe required for some systems.
        :return:
        """
        if rewrite: print("Rewrite is enabled. This might take a while...")
        if time_scale: self.__modify(time_scale, self.ts_loc, time_scale=True, rewrite=rewrite)
        if duration: self.__modify(duration, self.dur_loc, rewrite=rewrite)


if __name__ == '__main__':
    vid = Video("mp4.mp4")
    print(vid)
    # vid.modify_time(b"\xff\xff\xff\xff", 1)
    # print(vid)
