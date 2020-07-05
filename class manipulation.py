from pydub import AudioSegment

class CustomAudioSegment(AudioSegment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def amplify(self, ampLevel, ampToOriginal=False, start=None, end=None):
        def timeToMS(timeIn):
            """how it works:
            take the hours, turn it into minutes and add the minutes
            take the minutes, turn it into seconds and add the seconds
            take the seconds, turn it into milliseconds"""
            # format: (Hours, Minutes, Seconds, Milliseconds) (its a tuple, or a list)
            if timeIn is not None and len(timeIn) == 4: return int(
                ((timeIn[0] * 60 + timeIn[1]) * 60 + timeIn[2]) * 1000 + timeIn[3])
            return

        def cutAudio(inAudio, starting=None, ending=None):
            # cutting audio: https://gist.github.com/gchavez2/53148cdf7490ad62699385791816b1ea
            starting = timeToMS(starting)
            ending = timeToMS(ending)
            return inAudio[starting:ending], starting, ending

        def ampUp(inAudio, ampLevels, starting=None, ending=None):
            if starting is not None: return partlyAmpUp(inAudio, ampLevels, starting, ending)
            while True:
                try:
                    return inAudio.apply_gain(ampLevels)
                except OverflowError:
                    ampLevels -= 1
                    if ampLevels <= -1: raise ValueError(
                        f"Audio level has reached -1 or below, making it impossible to amplify. Level: {ampLevel}")

        def partlyAmpUp(inAudio, ampLevels, starting=None, ending=None):
            cut, starting, ending = cutAudio(inAudio, starting, ending)
            cut, ampLevels = ampUp(cut, ampLevels)
            if ending is None: return inAudio[:starting] + cut, ampLevels  # without ending
            return inAudio[:starting] + cut + inAudio[ending:], ampLevels  # with ending

        def ampDown(inAudio, orgAudio):
            return inAudio.apply_gain(orgAudio.dBFS - inAudio.dBFS)

        original = self
        final = ampUp(original, ampLevel, start, end)
        if ampToOriginal: final = ampDown(final, original)
        return final


audio = CustomAudioSegment.from_file("cringe.ogg")
audio.amplify(10000)
audio.export("lol.ogg")
