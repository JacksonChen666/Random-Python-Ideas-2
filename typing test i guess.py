from tkinter import *
import requests as r
import random
from sys import stderr
import argparse


class CustomText(Text):
    """https://stackoverflow.com/a/3781773
    A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    """

    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        """Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        """

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break  # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class Typing:
    def __init__(self):
        try:
            self.words = r.get(
                "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text.splitlines() \
                if not args.lorem else None
        except r.exceptions.ConnectionError:
            stderr.writelines("Error: Unable to get words online. Using lorem lipsum instead.\n")
            self.words = None
        if self.words is None:
            self.words = self.get_lorem()
            print("Using lorem lipsum dictionary")
        self.window = Tk()
        self.window.title("Typing")
        self.texts = CustomText(self.window, font=("Arial", 16), height=20, wrap=WORD)
        self.texts.tag_config("correct", foreground="green")
        self.texts.tag_config("incorrect", background="red")
        self.texts.bind("<ButtonPress>", lambda e: "break")
        self.texts.pack(fill=BOTH, expand=True)

        self.input_box = Entry(self.window, font=("Arial", 15))
        self.input_box.bind("<Key>", self.verify)
        self.window.bind("<Return>", self.new_typing)
        self.input_box.pack(fill=X)

        self.new_typing()
        self.window.update_idletasks()
        sizes = ((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), (self.window.winfo_width(),
                                                                                       self.window.winfo_height()))
        self.window.minsize(sizes[1][0], sizes[1][1])
        self.window.geometry("+{}+{}".format(sizes[0][0] // 2 - sizes[1][0] // 2, sizes[0][1] // 2 - sizes[1][1] // 2))
        self.window.mainloop()

    def verify(self, e):
        trueText = self.texts.get("1.0", END).rstrip("\n")
        userInput = self.input_box.get() + e.char if e.keycode != 8 else self.input_box.get()[:-1]
        print(e, flush=True)
        self.texts.tag_remove("correct", "1.0", END)
        self.texts.tag_remove("incorrect", "1.0", END)
        if userInput == trueText:
            self.input_box.config({"background": "green3"})
            self.input_box.insert("end", e.char)
            self.input_box.config(state=DISABLED)
            self.texts.tag_add("correct", "1.0", END)
        elif trueText.startswith(userInput):
            self.input_box.config({"background": "white"})
            self.texts.highlight_pattern(userInput, "correct", end=f"1.{len(userInput)}")
        else:
            # TODO: include green highlighting because it's being cleared
            self.input_box.config({"background": "red"})
            notMatched = True
            uInput2, uInput3 = userInput, userInput
            while notMatched:
                if trueText.startswith(uInput2):
                    notMatched = False
                else:
                    uInput2 = uInput2[:-1]
            uInput3 = uInput3[len(uInput2):]
            self.texts.tag_add("incorrect", f"1.{len(uInput2)}", f"1.{len(uInput2) + len(uInput3)}")

    def new_typing(self, e=None, text=None):
        # TODO: take quotes like type racer
        if text is None:
            words = [random.choice(self.words) for i in range(random.randint(args.min, args.max))]
            text = " ".join(words)
        self.set_text(text or "Unknown")
        self.texts.config({"background": "white"})

    def set_text(self, text):
        self.texts.config(state=NORMAL)
        self.texts.delete("1.0", END)
        self.texts.insert("end", text)
        self.texts.config(state=DISABLED)
        self.input_box.config(state=NORMAL)
        self.input_box.delete(0, END)
        self.input_box.focus_set()
        self.input_box.config(background="white")

    def get_lorem(self):
        # no, i cannot include the english dictionary just like lipsum. lipsum is smaller. (26 kb, 8 kb compressed)
        import zipfile as zf
        import tempfile as tf
        from os import remove
        # https://github.com/ccpalettes/sublime-lorem-text/blob/master/wordlist/word_list_random.txt
        lorem_zip = b'PK\x03\x04?\x00\x02\x00\x0e\x00\x00\x00!\x00\xaanPL\xb7\x1c\x00\x00\xbbZ\x00\x00\t\x00\x00\x00lorem.txt\t\x04\x05\x00]\x00\x00\x80\x00\x000\x82\x88K\x9d\xc9\x13o\xa8\xa4Go\xfa\x18vl\xa2\xd9b\x84\xae\t\xae~\xe2nXn\xfe\xd5\xe8N\x1c\xb17%sc\xc0T\xa4\xacI\xcc\x90\x02X\xdf\x04M\x81qz\x8da\xce!"`\xd9\xcb\xb2gK\xdb`3\t\xbd\xe8\x06\x98\xef;$\xa3\xd3\x01A\xe4\xa2\x10\xfa\x01U\x07$\xc5i\xc8\x99\xd7\xb0\x93\xfd\xb1(\xcdN+\xbb\\~\\\xc3s\x11\x98\x18(\x8a3\x9f\xba\x93\xb0\x8dSd\\\xb9\xf4 \xd8\x89s\x87N\xfb\xbd%\xe2\x98\xfb\x89\xferVX\x82K\x8eZp\x18|\xff\x00\xe5\xcc\x8aKL6\xd0iKed\xcb\xf9?\xd6\xa5+\x9c\x80\x95C\xfcWv\xa0\x02Q\xfc\xd0\xddaN\x8a\xfb\x0e\x91\x8b\x1f\x9f\xafXg\xf6r\xab\x87\x12qa\x14i+\xfdr%\xfc\x1a\x86\xf3\x98\x12s\xeb\xaa\xb0\x0f\xab\xf7\xd5\xc2\xc3v\xcc6\x9d\x1bw\xf2\xb1\xc4\xa3\xf9\xfa\xa1>w^#\x07k\x1b<W\xb3?\xf2\x90\x03\x8c\xbf\x92\xea\\fA\x94\xf9n\x90W\x13]\xf9#y\xe1\xb0\x8a\xbfrm\x02\x04\xb99\xf8\xc0~L\x9d\xd5\xaa=\xadP\x84LJ`4_\xf2\x84;\xcd\xbbp\x88\x15\x838\xb7\xe4i\x1f\x15Y\x89\xd4\xde\xb7\x1b\x7f\x12H\xe8\xefg|\x82\xb7\x15\']JV\x1d\x904\xb8\x94;E\xc8V\x11\xc5\xb68\xb1\xa2\xf0]\xbb]\x15\x84\xae\x97\x82\x1c%\x03\x90W\x1b4\xca\xe2]\xff\x1f4\xf5{\x02\x82\x18T\x86\xad\xba*\xf3\x97\xa5L\x86\xec-E\xf8nhF\xc9_^t|LyQh^\xd1\xb2\x95\xbf3R\xa9\xb3\t1i2\xe3\xd0?\xc3\xa9\xea\xf5|_\x82(\xa6\x1e\x86\xa8\xd6\x13\xa8F\x04Td\xc1\xa7\xda\x85\x9bS\xdf\xb1Q\xa5\x9eh\xc2#\xac=\xcf\xe0\xa3\xcd\xb0\xd1\xd7\xdc\x02d\x87\xf2\xf4\x13Q8\x8f0\xba\xf7\x01\x18\xaczC*\xe7k\x8b\x9e\xbd]\x1e\xb2o\xe7ncJ\xf1L\xef\xaa\xa0Kj\x95\x05\xa05<rn\xecI\xc9\x08\xbe\x83\xc8]\xb4\x90\x0e\xdb\xbb\x1a\xd88\'F\xc6J=\x15,\xeb\xf9\xfd*D\xa7\x16\x11f\xcdN\x89m\xa9\xbeU\xce`\xa7+z\xe1\xaa"\x82l\x140\x93\xbc:G\x80\xe7\xdb\x93\x8e\xac\xbdU\x97\x02\x00\x1b`vsc\xdaGY\xa7$$\xfcF\x1e\x07\x99\xef&A}\x07\xe0>\xc3\xcc\x89P\xe0\xe1\xc6^7k"\xc6\xbd\x84\xd0\x1cT\xd5D\xb1$\n7\xed\x8b\xc9 \x82\xd3\x93\xbc\x05"\xe1H\\\x1d\xf4\x03+\xeff\x8c\x8c\x84tW\xe4Ap@\x1c\x7f\x9e\x1f\xf7\xc26\xa6\x91\x08\xc5\n-\x9fh\xc38\xb7\xdf\xa6y3\xd1\xfe\xea\xa7\xf0\xaaC\x7f\xe1o\x12?V\xfc3\x8e\xd2\x1aTq\x1d4>\xaa\xf8\x1a+\x15M\x18\xb5{\x83[\x0b\x85\x01`~1\xab\xce\xfe\xde\xe6\xb0\xf3&\xbe\xd5\x81!TsMY\xb3\xbc\x7f5@\x9c\xcefw\xc5\xf9e\xaf\xd3\'\xaf\xd7\xc8_\xbb\r\x15\xac\xb5\x1f\xda#\x18\xfd~x\xa8\xc2\xbb\xe2fI61$\xd7W\x1e1\xb7\x1f\xea!\t\x18\x84\x1c\xfc\xbeX\xf0X\xe9`\xcf\xacZF\x1d\x0fk\xe7"\xee\x00\xa4\xd1\xcc\xd8\xcc\x942\x8e\xd4\xe6\xd8\x10\x10\xbbR\xd2N\xe9\xadd\x9a\x89\xb0\xfc\xeb\xa4\xe4"3(\xf6\x0f\x92\xa8c\x9a\xda\x83\xf3\x89\x8d\xb6\xe7\x15\'v\x17n\xc2\xe0_\xb9\xe5\xdd\xd0\xc1o\xa9\x07\x8520\x85\xed\xbc%\x81a<\xc8\xbcW\xdf\x97\xc8RVi(\x91\xd3\xd6\xbbzE:\x13\x83\xb7\x8ers\xeb,\xbeH\xf5d\xfcp1\x97\xca\xb1\xf3\xd5\xe6\x98\t)\xcc\x0c\xb6C\xa2j\xcfh@\xfaO\xf3&l\xf2\x95\xc4\x0f:U!\x91\xee\x96{\x14\x9ft\x8c) \xf1\x11\x1fr\x15(/+\xc5W>w\xe8\x06\xe7\xd3\xe7\xa9\x1cs<\xc67\x9f\x01\x9d\x9b\x8f\xd0\x1d\xb2\xf8z\x93"\xde\xc92\x00\xaf\xce\xa0\xdc_\xa5\xa1\x97NG\xae\xf7*B\x84\xa0\x9c\x9a\x0fGf\x83wI\xf2^`\x90`dZ&\xa0\x03\xbc\xf9W04u\x94\xa6\xaa\x04J\xc2\xb9\xf3?{\xef\x9e\x88\xb4\x8b\x95\x18\xdf\x19\x96\x99\xcd\xba\xcf\x97\xc5\xbc\x0c\x843\xc9\xc2!"I`\xeapdG\xc4\x9a\x1d\xe3\xa0\x8eT+\xbc\x95i\xbdB\xde)\xf0\xd4~\x05>= \xf4H\x1a%8\xfd\xb0\x93\\:()\xbc54\xcb\x83*\x8f\xd5\x10\x17\xc7F\x19\xf2\x9a\xd9\x9bT\x10Ja\x97SF\x84\x04_\xf6\xe5l\xc2\xdbQ\xe2\xac\xe7\xdc*}$QU\x10\xcak\xfc\xa9\x8a/\xe9j\xea\xe4+\x8a\xb4\xcd\r`M\'\\\x12\xba>\x9f\xdd\xbc^\x90\xb86"\xd6\x0b\xe7O\xd5\xe7y,i\x15 \xdbf\xaa=\x1dk\xa8\xfcr@x\tDR\x1b\xd3\x9eGL\xe1\xbe%o\xd9\xf1\x9d\x16\x08\x92\xbd\xddOS\xc3\x97\xec\xe8\xder`\x83sJ\x16\x1b#Z\x15.\t\xfe\xfb\x92/>_\xc4\xb2\x06\xd1\xbc\x8aB-F\xa4gD\x93u\xb4\xa2Y\xe4\x8a4Z\x89\xbf\xf0eS\xe4z\xb0\xcb\xa7\x11\x96\x05\xf3\xdbb\xd7\xcbu\xdbO\xd0\xe8\x143nr \xe5\x15;G\xefx<\x19\xf6\xcf\x99\xa1\x19\xbf\xad\xecE\xaf\x1b\xc1\xdeER\x19\xed\x88v\xf4\xacL\xd5\xbb\x96u\x9c\xd8\x07\xb1`P8\\p<\x9f\x0c\x81\xe2\x9a\x06\xcc#\xc0\xe1\x08N\xee\x84t\xb2\xba\xe0\xb1\'\x9c~\xcf%\xa6i\x13FW\xad\xd1\x8cQ\x08:\x88e\xf6\x1ep)\x9b\x0fpwHf~\xb3\xe1MW\xcbG\x0e\x95:\x07\xa2\xf0\x0b!6S\xae!\x95\x8bCM\x8ekntB\xcf8c ?7Ja\xeb\xe2lxKj\xf0_\x13\x83\xb0"T3\x8c\\\xbc\x13\x18\x91C\x93\xb8\x12_N2\xf6\xd9\xd0\xb5\x8ek\'\xd6\x97\x95|\xb1\xf9\x88\xf8[R0c\xcf\xd4L\x88\x85\xbd\x85k\x8c\xdfBIf@\xdav\xa1\x02\xf1K\t2\xa5\xbej\x85\x1a \xeaY\xfe\xac\xfa\xea\x10uwN\x81\x81\xf7\xdc\x1f\x0e\xe5\xf1W\x00c\xa3\x0f\xe4\x194\xf3\xf8\x99\x19\x18\x99+^ \xe6;\xfb\xccH\xe1)_\x9c\xbehrJ\x0f\xd8\xea\x1c\x9a\xb3\xbd\x0es\xe0?\x8d3{sq\x9b\x9aB;V\x1a\xd1;\x12\xc4\xf7\xb7\xdaa=A\xf5\x86\xc4|\xd4\xa7;\x9c\r\xea\xc7E\x0e\xf7\'B9z\xb3~\xc5\x0f2mxr\x06\xe2\x00\xd0\xc6\x08X\x95 F\x03\xa6\xebr\x82~\x1b\xd4\x1e\x01\xc0\x94\xf8[U\x1e\x9d\x82"\x91\xfe\x8d\xc5\x98\xf1D\xcb\xdc\xb3\xa8d}\xacE\xe8[\xaa\xb0\xe8i\xab4Z\xb9\x8b\xa1\xa0O\x9eW5s\xd2\x86\xd6\xf5mu>\xcbXn\xd0\x88\xcd\xe0\xde8a\x0f\xe6?\xe2U\xb7f\xb5\x88^+Y\x9d\xec\rl\x1f\xa7\xe69\x16\xd3l\xdb,\x1aJ\xe6\xc5\xb0K\x966}\xb6\xd5o\xc9\x00^\xf5BQ\xc9Zi\xf6\xa0\xb7:\xed\xdb"\xc9\xd6\x9bA\x907\xdf\xbd\xcaw\xf2\xa4\xf7Z\xf45:\x96~\x04\xc8\t`~\xfd\xa3\xac\xec\xae\xb4u\xbdK\x9f\x1c\x97\xfd\x1a\x7f\x86\xd0\xf5\xabm\xb7\xe8FP\xc2\xb6\xc6@\xd1[\xb7}\xee\xac\xfdR5\xda\xe9\x9eg\x9d"\xcc\x13/\xd2\xc5:\x19\xd5?\x02\xce\x8b\xf3\x15}\x86!\xf2\xd7\xfb`\xfa\xdc0\xd5\xaa\xe01V[6\xad\xd7\xfa3L\x01;s\xaa\xdd\x12\xde\xec\xe3lW\x90\xafV\x04j\xa7\x8e_\xf1\x8e\xb7\xf6\x9fk\x07 \xa7}(\\\x9d\xc3\xf5Y\xf0\xa9\xda]\xd3\x06\x16\xd3\x08\xb6\xba\xa4\xf5\x8b\xb8O{\xeb\xa7\xda\x95\x02#\xf9\xee\x17,\xdd\x00 \x03!\xef\xbe\xdcu\xc1\x9e\x07\x97\x17\x19\xfcA\xb1=\xdb\x03>\xd3\xd4\x7f\xdct\x80u\x93\xbe\xe62\xbf\x0b\x07\xeb@b\x81\xd7\xa5m3\xa7\xeb\xd5\xae%I\x19\xe9^O\'\x8f\xa1*b{\x96\xa1\xdd\x18>\xdc\xe89y\x88\x0b\x01\xa7^\x98E\x03No\xe0\xfd\x9b\x85R\xaf\xe7F\x1c\x865\xc2\x92\xb1\xa8uV\xe0\xe6\xe8\nQ\x10\x87\x9d\xd0\xce\xba\x10\xd4\xf2\xc0\xb6\xd3\x14\xd9\xbc\xf3\xc5\xe5\xf4qj\xe4\xb5r\x95y\xc6\xb8\x86\xc3\xff\xe1\xc8\xc2\xa2H<W\r\xc8\xe7\x95B\xc0\x94(\x057\x18\xee\xc8\xdeF\x98\xc1\x99\xbaC\xe9\xab\xb8\x96\x0e\xc7V\xa9\x02\x988\xef#\x88s\xf4A\x8b4\xce\xab\xde\xb2s?\xef\n\xe0\xe0\x15\xa7\x07\x8bc\xbb\x1a\x14\xe5)\xfc/\x99IE}4\x15\x1a\x90\xb1\xbe\xaa\x85|=#\x98\xa7\xda\x96K|\xc1\x968\xcar\xd5+(\x05rD\xb0\x98e_F\xab\x03h\x0f\xf2\xe7\x07\x1b\x06-K\xcc2EP3\xb0\x1fI\xa8B\xac+\xdaQ\x07\x87+o\x1b\xf7\xc1\xf3\t\xb6\xac\xd2\x04`\xad\x92\xc8!:\xf8\x9d\xfb3\x0b\x13TK/\xb4sa\xaa\xcc\x8eBB\xd7\x8fc/s\x08;\xcc\x1f\x01\x8e4X\x072\xa5\xda\xb9\x17M\xa7,OmK\xc8El\xfeq=\x0b\xe8\xb7\x01\xb5\x16L\xcc+tnqjw\xe0\xdc\xc7\x12C7j\xde\xfcA\xf2{\xf5\x87\xd1X\x97d\xd6\xcb\xe7\xa0\x8e\x01\x804]e\'\x01l\xd7L\xc5\xbb\x81\xa3@\xbcRX\xdc"Z\xe5\xd3\xd3yS(\xccs\xfb\x80\xda$\xb8\x0b5\x9d1"\x06N\x04p\x03\xfd\xcc\x0fB\xd4\x0c\xd9\xf5\xc0\xe7\x96\x12\x16\xdeC?m\xb5E+\xbeen\xcd\x15\x83\xbeGS\n3sZ\xb3\xa3W||\xe8B\x93\xedK\xafH\xc5 \xdc\x81\x13u@\x8a\x18\x86\x87-\x96$tf\xc0\x0f\x9b8!\xa6\xbb\xfe\xa6I\x80}\x95>\xdd\xd4z\x05\x8dZ\x9eU\x97\xdds\x00\xf6)\xa7\x0c4\xc4\x89B\xa3KRZ\xc3\x17F\x91R \xad\xd0\xbf\x90\x83\x15\x8b\xd5\xbbJ9\x7f\x87\n\x02:\xbb\xcc?\xd0\x1c\x18n\xde\x91\xe9r\x06\xbeG\'~kyF\xea^\xd71w\x05\xc8-:\xca&n\x8f\xfd\xcf\x8e.\x15\xf6\xa6Yy\x06\x08V\x8d>\x9f\r\xcd\xeb\xfd\xd9\xf3\xf4\x1b\xb9bS\xe0\xa3\xe7\xd1j\x80D\x05\xd1\x14\x0b\xae}\xef\xe4\xc3\x04\xf0?\x12W\xc4F\xd7\x8d\xac\xa6\x1f&\xa4\x0e\xdd\xf0\x04\x97\xb6M\xf4\xf6N>\xaf\xaf\xc1+"\xbe\x8b^+\xe9rv\x10\xf2\xd1\xec\xd9\x00\xf56#\xd6=\x13 \xd4\xe0\xfd\x0ft\xc5\xac\xd1\xcdx\x7fo\xac>\x8f\xd6\xba\x9ca\xc5\xdd\xf2E\xe0@\x08(s\xfc\xd0S\xbf|\xd8G\xfd\x13\xbd\x81A\xea\x82"\x1an2\xaf\x84\xbf5_4+x\xd6\xc8\xf0vN\xd3\xd0&\x85\x01<c0G\xd1\x1e\xaeCm\xda\xb0\xa5\xb0\xddAj\xd0\x9cO\xacy\xbe=X\xd9\x96\xff\x1bk{\xdcpU\xd2\xd3@\x86\xbe2\xccc\xd1/n\xb2NV=m\xfc]3{\xc4\xdc\'\xa5\x9bO\\>iN\xf2\x85\xed\xbf\xcemB\x9evb\xe1\xc9\xf9\xee\x8bi<\x87:\xac\x9c\xb8\x0eV\xeb\xdb^Q\xdcx\x10\x99\xf2KP\xf8\xaee\xba\x85\xb5\x99\x830\xae\x8f(\xd7\xa6NjNh\xf8w\xc3\xdb@$\x10p\xd6Y>\x1a\xf4\x83*\xf4\xfe\x9f~gy\x14\xf9\xfdB0\x1f\xaf\x94\'t\x90q\xf3?8J\x88\xda\x12\xcf\x8c\xefI\xf9\xf5\xd4\xf5z%pl\r|\xf1\xc6\xe5H"\xbd\r\x8a;\xce\x18\x97^\x10\xc3E\x16\xac\x93f,\xc6\x89Gxa\xde\x7f\xe6\x8cL\x9e\x9e2e\x80\x85k\xfc\x96a-\x85\xcf`\xbdZ\xb8\x96(\x8f\xae\xf4\xb1\xae\xf2\xb5\xeb=\xbc\xbb\xc28\x06\xf6\xa04\x06\x93\xfa\x9f\xfd\x8e\xd22\xa5\xaa\xcb6[4\xab\xaca\xee\xeb\xa5\x1f\x9b\x92\x0f\x9a]\xa1\xdfz\xb4\xc8:^\xcf\x18\xf5!:\x14\xe1\xa1\xb6a\xd7p\xb8\xe8\x95\x0fF.\xbc/pI\x02\xf0z\xafc\xe7\xdeS\xd8J\xbf\xa3\xfeJ\xd4S\xa7\x11LT<P\x9f\xc8\x04\x1e\xc8\'\x05W\xba$\x1d\x93\x02\'\xb7?x\xe1S\t\xd6\xedN=\xfd\xcb$\xd5T*\xf1\xc3F\x16\x13I\x9c?\xfd[\x1a\x1b\xf1\xd7\x8e\xf15\x16[Z\x01\x80\xf3\xe3\x82\xf4\xe3\xff\xa6\x14)\xb4\xe3\xf7\xed\xa9M+\x08\x04\xd6\xf8\xfd\x96\xd5\x14\x03^9r\xe7\x0c\xf5\xb9D\xa6\xe1\xc5\x83\xac\xa4\xa6\xe4\x9c\xcc5\xd3I\x95\xd5\x07:\xe9\x0e\x84$\xa6E\xf4\xb3u\x1ff\xf9`Lcj\xdc=\xd8Coob\xc6\xec%\xc1\xa7\x8c\xd1\xef\r\xb0:\x82%\xc5\xd1\xa7\xa7\xbe\x80n\x04\xc1\xe03l-7\xae\x99\xdf\xd2\x12\xb4b-\xf1~7w%\x98\x9e\x8ca\x84\xe4\'\x15\x9d\x98\x0eWkQ\x8a7#\xbdB89?\xd3\xa6\xe5\xf0\x90\x93\xac\x96\xde{\xb7S\\\x9b\xc7\xed\'\xfc{k\xf9\xd9\xcc.\r/\xc3_\xb4U\xa3\xa6G\xaf\xa9\x1d1\xb4m\xb0\xe7\xf8e\x0b\xa8\xa4?\x8d5\x9ao\x86\x81\xdf\x15T\xfa\x9a<\x14\xba\xcb\x03:\xc6\xaf\x8f\xc9\xc0)\xd7\xe3\xaa@\xe4\xd7\xd9\xa7\r\x9a\xc0{H\xa1?\xdaE0\xa0\x9c\x83Q\xd0\xe4\xf9l)\\\xc0\x1c\xee\xb6\xaf\xf3\x9e/z\xfb9\x8d`\xf5\xf6\xbfX\xe2U\xc1\x87\xdc\xac]\xdfF,\x0e\xbecM\x19(\xa9\xcf\xae8\xa6\xe9\xb9\xf9\x07\xf8J\xafE\xbf+\xfe\'W\xab<\xfc\xa18\x04`\xe4"\xaf<\x1f\xd9\x0b\x00F\xee[\xbf\x91\xc68\xc0\xbe%\xb3b\xb9\x8cq\xa1~A\xdb]`6\x01\xc9\x1b]<\\\xe8\x10\xca>\xfd\xd8\x12\x9c\x91U^\x10\xd3\x18!\xa7\xc0\xe0_\x97P$\xb6\xe1F!\x83\x9e\x17\xcdwk3R\xcdM+,r\xd1\\\xd5\xaf\xcc\xca\xc2\x96%ul\xd9~\x81\x1fs9\xf4\xb1+\x8a\x0e\x13\x80\x90\xec>Gq\x8c\xdcQ\xd8\x10*L\xa1\xd6\x90\x9c,\x9b\xef\x9dc\x97Y\x92/\n\x8a\xcc_1~\xe8b\xeeD\x9f\x855\xa4\xc5\x19s\xaed~\xc5\xbci\xc7\x02\xbe\xf5z\xc9\x19z\xdb&H\x90+r\x97\xbf\x1d[Z\x9b\x10\xfcx\xb6\xc2!\xa9\xdc+\x1b].\xeb\x80S\xdf\rv\xfduK\xea\xa5I\xa8Ca\xbfU*p-\xfe\xde\xed\r\xdfxX\x89A\x153\xfb(\xde\xf1\x97i\x89\xc5\xc3r\xcf\xcb\xa6\xe2\x8d\xef\xad\xaf\x14\xff\xd7\xe6O\xad<\xa8J!-\xf3s]\xb5\xbe\xc0\xd4\xf5+d:T=\xde\x0b\xce#\xc4QY\x99o\x1a\xbc|\x85\xba\x98\xd3I\xe2\xa4\xf5$\x9e\xee\x1e\xbcp,\x88\xfb\x8b\xec\xcc"K\xfe\xddc\xd0\x03\xa9%\x0el\x06y]\xa6\xe6\x17\x00f\x1ao\x8a\xf2F8\x0f9S\xde\xdb\xa7\xd1\xf2?\x11\x10\x14.5D\x9b\x0f&\xab\xb6pf\xe2\x11\xda\xc5/\xe5\xb9\xf5\xc3\xb1\xc7\xd1|\xce\x06\x1d\x9cj\xc1)\x04\xf9\x16\x9c@\x99!V\x98\xd1_\xb2\xa8\xfa\t\xf9N\xdc\x82\x936\x1fa\xb9S=D{J17\x18\x16\xaeT\xb6\xed\xe5\xd9H\xbd\xd8\x91\x9f\xbf\xd7\xde\x89\xc2\xc837\xf4h+\xc0\x01\xf16\xff+}\xc4#;S\xeb\xdb\xcf\xd7\x939\x1a\xf4\x8d\xf57\x08QF\xce\xc6\x99R*\xcfR\x8a\x07~u\x87$v`\x03\xc3\xac\x85w\xd68\x87\xcb\xb1\x95\xc2\xcfj\x1fN\x14\xc8vO\x93\xbd@\x08X\xb3ZO\xb8\xe4\t\xf9\x0c\xa7\xc3o1\xbd\x10\x0c\xe9\xd7\xbdP\x89\xf9g\x0f\x1bh\xd6\xcb\xc9\x85\xcc\x8c\x90~\xb7I\x89\xaa\xacQ\x1f\xef8w]\x13Z\xb9E\xa8\x8ct\x17\xcfIv\x9a\x95\xce\x86D`y\xea=\xba*T%\xdb\x84\n\xe5o[\x1d\xdbu\xa8\xd8\xdc!\x85\x0eI\xeb_=\xf4=\t\x17\xcd1\xfd\x01n\x9d\xe1\xe5L\x18o\x8a\x1b\xd4\x7f*iSG\x11\xd2tlY\xb0\x93E\x0eV\x0eMP\xce\xb4\x04T\xee[\xdbc\x9b*\xfb\xba\x9eK\x00\x16;5\x1c\xb4b0\xfc\x86\x96\xdb4\x86\xbe\xd0\xc8\xefJ\xa2\xf8x\xb5\xe2\xdbX7\x00\xfd,L\xd0s\xce\xff\x08\x97\x18\xa3t\x17P\x11E\x01\xb0\xb5\x88;\x8a\x88\xfa<\xdb\x16\xc7\xc6G9\xf9\x1f\xb4\x13\xb1\xc3cC*\'!x~G|\x08#&\xb9\xa2@\x84\xf9+\xcd(O4\xa91\xde%\x93\xc0d\x1d\xba+p7\x7f\xb6\x93\xb7\xc5`\x10\x9a\xfc3\xa4\xb8kV\xe0\xd9\x1c[\x1e\xe1\x97\xa0\x82\xc4\x9c\x1f\x13\xd8N\x11t\xf4\xeb\x12\x1aO\xa0\x1d\xce\xd9\x87\x11\xd8?)\xb4\xad\xed7\xd1v)\x80\xc7\x93\x898@Of\xd2\x05^\xff\x87:\x8ez\xcb\x8aI7\xc0\x1aP\xf6H&\xea\x10\xc9+\xf0\x7f\xb7#\xc1\x00\xb5\x9a\xe6.\xc1\xc9\xca\xf1\x08fS\xd7\x87A\x8a\x98D\xb7D\x01\xf2gkZ\x8a\xdd\xbf\xcb\xd6\x00\xa9\xb6\xdeF\xb8`\xb6\x1d\x15\xe8\xed\xcbSi\xb1#\xd5\xbdiI\xd6\xcd@\x10n\xa0\x19%\x82\xbc@\x8c\xd9p\xfe\x8d\xd2\xfc\xcc\x93\xdc\x18\x8b\xbe7\xa3\x1f\xac\x0c9\xbc\x00\xe7e\t(#\x9c0\xb3\x93l0\xcdD\x1e\xfb\xdb\xbb\xf1}\xb4hz/|G\x9di6\xe9\x98\xf3\x94\x81\x85\x87\x86g\x80\xba9y\xd6\xa8w\xcfu\xf6\xad5\x86}\xe7\xb4\xb5\x8d\x94\xcc\xc6\xe1\xd5F\x9b\xc9+,\xd7d\x81\xa7\x97a\xa81K\xcd_\xc6\xfbj\xc5.\xbcu\xb6\xe2\x9c\xdf\xaf\xc9C^\xfe\x8ah\xdblh\xeb\x88X\x0c\'\x1c&\x9f\x16\xc9\xaaQ\xb8\x89X\xfc\xa5RM\x18?\x81YY\xd4\xef\xd2b;\x8fX\xa2\xb04\xa6\xc1\xa3\x0e\xea\xe0\x18r\xf7\xe4\xe5\x11\xac\x90~w2O\xec>\x91\xb2\xee\xf9\x93\xb8\x95\xa7\xbaU3c\xd5r\xe6\xf5R#~\xe7\n\xd9\x867\xb7\x9f1\xe1\xa2>\xa3\x86\xca{\x0et/\xca\xd6\xf3k4\x92\xab\xe5\x14\x83d}\xa2\x92\xa6\xd0\x99\xff\xb3/\x92\xcbj\xa5\xff\x96\x85D\xad\xd0\x98I\n_\xa8\x82\r\xec\t\x00\xaf\x04\xb7\x05_\x15\x9b\x9e2\xc3\x1f\xab>\xda\xe1\x1f\xfc\xa5d[)\\!\x95\xb3/<#\x88r\xd64\xdc\xa1\x14\xc1\xa5k\xeb\xbc\xf9vp\xa1\x98U\xd1\xc6\xcf\xea\x16\xfd&\x94\x96~\xc0H\xfa\xfc\xfb\xec\xa7!\xd19\x08\xfa\x15\xc1\\|W\xf0S\x04\xf2!l\xf3\xbe\x18\xff\xc6\xf7\xcf\xc4\r]\xb1\xefg\xd5\xa6\x88\x15\x1a\x90\xa2C\xa1\xecW`\x08\x01\xa4\xca\x81K\x03p``j\x86\x1f\xf2\x14@\x8b"\x91ST\x7fZ$\xf9JX\x8fd<i\xb6Q\x19\xaaC4\x7fw4\x94\xa2\xd2\x02\xa3\xf7I\x137\xc9\x17\xbf\x1bLI\xce\xb3\xa1\x8c)\xe6B\xbd\xf5\x92\xd4\xde\xc5\xaa#&V;\xf2\xe8\xbe\xc8_\xa5^\x1c~\xca\x03\xd5\xdb\x93\xa2-]4\xe6}\xdf\x9c#\x1d\t\xdf~\x13\x05\x9a\x0b4[*V\xab\xe0\xb0W]\xea\x8f$\xc5+\x9e\xf3\x9f\x8f\x14\xc9Z5.\x14x\x07[\xc1xaK;\xd1\x8d\xf0/\x15~\x04\xcd\x96}\xa3\xd2`F\xc6\xe9\x91T\x88\xfa&SL\x1fI.\x0fV\xac\x1cl\x1e\x8f\xab\xba\xc1J\xec\xe1\xe3\x0b;r\x95\xb7\xc3\x87\xbc\xa7\xdf\x8d\xf7\x15\x06\xec\xebQ\x96\x0b\xc4:<\xbcr4\xd1\xba=\xbe\xfc>\xc94{\xc1\xc1S\xde%,_[\xee\xb4m"7c6\x81\xb2\xe8\xe4\xa8\xe2\xe9\x16ibsj\xef\xee\xfd\xcar\x05\xe1\x80\x1cl\xacT(\xf0;\x84\x96\xc2\xef$\xffo\xfb\xeb\xe4N\xee\x81G*\xea\xb6(Z\x1d\x86\xa6\xe0tVN\xd6vw\xc6\xa3\x84\xbc\xfd\xd6k\x9a\xd6\xbd&\xd5\x00\xcf\x0e\x12D\x83\xad\xa1\x8f\xf5A\x1d\xe1\xa8\x85e\x0f\xbf\x0by\xc9\x8b\xc2[\xa4\xd2\xb6Y\xaf}\xdac\xbc\x98\xb3\x87`j\x89H\xf3I.J\x9d\x12\xe4^\xeb\xb4TZ\x9a\x01H\x17Ef6\xfb\xd7I\x84\xd7\x18\'5\xdd:\xc1\x03\xed\x06\x9bX\xeb\x97B\xbe\x1f\xfaP\xa4\x9c>M-X\x85_\x14\xac\xdc\x9eVv\x1b\x16\x1f\x17\x87iL~.T\x18;\x08\x9f\x8d\x96\'T\xea%\x8b\xc6\ra\xb3\x912\xf3P5x*\xddp\xbe\xb2\x1dB\xcf\xa6\xb2\x11\x8c\x07\xadM\xee\x88\xc0_\xa8{\x97\x8f<\xd0\x88b\x86\xda\xb1A`\xceHs\xefBr\xbfO#=Nw=\xd9n\xb3x\xeb;\xbd\x1b\x92te\x14\xc4\xc2\x01\xcb\xc1\x8c\xb8P\xa2`=,n3f\x96\x9c;\xb9b\xd7\xe7\xd14\x91\x15h\xae1\xa6\xdf\xb8\xba.\xb0F\xe0a\xbb\td\x1d\xcd6Y)\xb5\xff\x04\xd4\xf4\xa4z\xacb\x11}\x7fO\x00@\xeb\xcc\xd7q\xe5Zi\xc8vZ\x1f\xbeB\x1e\x1f\xea\xb8\x8a\xc8\x16*/\x18\xc4w\x0f\x1fr\x8cS\x1a\xc4,\x02\xd5\xc1\xc9\xc0\x87M\x01\xc8\xc7\x95\xe2\x1b\x15\xc7\xff\xeb\x01\xeb\xd9\xb4Qu.4\x8c\xac\xd5\x05\xfbs\xffs\xa7\xdfU\x16\xd7\xa8\xc1\xba\xb7u\x0b\x83=?\x07\x9ane\xf93\'(yc\xe0\x1b\x10\x8a\xd7a<\x87\xab\xe1\xc7[\xff8\xde\x0e\xb8\\4\x05\xa5hc?>\xc6a\x1b\xd3\t6a\x15\xbe\x08\x07\nf=\x1c\x9aH\x94YCZ\xa1X \xd6\xa9\xcf\x8d\xae\x9c9\xd6;]}Xk\xea\xdfN\xfethV\xc1@\xa2$r\xe1\xc0\xeb\x12ej\xa1Ah`\xc9aG\xda\xcd\xff\xc0u>\xaa\xbf\xf8\x8a\xb0\t\xe0\xdb\x05FTN\xb7t\x01M\xc2i\x03\xe1\xbeE\xc0\x8ai\xa9\x06!_e\xab\x0ex\xe3\x00h!\xb1\xb4g\xe6\x0b9\xe9\x9e\x87\xd5\xf5&\xa6p\xe5\xebU\xb2\xfe\x12o%&\x03&\xfb\xdd?]]\xd9Gj\xd4\xdc\xab\x1a\x8d\xc3\x89c\xff\x12\x80O\xa2\xd3\x1at\x9d\xe4ZuX\xba\x89\xc8\x8b;\'\xdec%\xdd\x11\xf7\xaeQPb\x14\x13$\x11\xd24\xec\r\xcf\xa3\xd4#W\x96\x87\x14\xadd\xd1?\xdb\xa9\xc3Y\x17\xe7\xcf\xc8j+\x13\nF\x90\x9d\xd9f\x16\x99\xd4Y5\x83\xc5]Y\xaa\x9c4s\x93DY\x96/\x1b\xa5\xd6\xd4\xda|\xfdt\x1eB\xd6X\x9d\xb9\x0e~>cQHt\x92\xa5\x87h\xa0\xa5Naeh\x9b\r\xda\x18\x9a\xcbA\x8a/\x04\xc39\x13\xf3\x95\xcb\x91;mad\xfb\x10\xc8\xde\x1f\xed+z\xd9\x85\x1a$\xfe\xfb\xa6l_\x1eZ\x8c\xd9\xd3\xe0w\x1f#V\x8e\xf3ll\x9b|\xa9\x9a\x08\xb0((\xa7\x1f\xe0\xd0K\x9c\x06\xbax\xb2\t\x85\xf0\xb8{<k58H\x98\x91=\x084[\x946\xdd0z\x11"\xc6\x99\xce\xe7\x17\xf5\x1b\xd2\xba\xc3\xff\x924\x97\x12\x06\x13\xf1\xee\x9c\x14\xd6g|\x95\xfdm^hZh\nL\x8e\x87\xaby\x9f.\x1b\xbf\x02\x93\xcb\x84l\x03\xdah\x0e6\x80\x07\x03fiA[-@\xde\x86%d\x17}\x05s\x80\xa3\xcbn\xd6\x83}t\x8b\xdd\x8eA\xd7N\x18\xf6\xde\xa5\x8b\xde\xc1&\xcf}\xc0_G\xc1\xe8i\xd2\x83\xa2\xeb\xcf\xfa\x8c\xc8\xb1~^4\x8c\xde\xff\x06D\x18\xbe\xb6V4n\xa7Ea\xc4zP w%\xad\x9cJ\xfd72E\t\xe9\xdd\x0e\xe8\x0e\xdd\xcc\xe8e\x1eY\xc0\x1e\x03V\x85\x9bH5\x04?\x01\xce\xab\xfd\xac\nf\x1cGw\x06\xef\x11d\x8ew\x9a^,oUr7\xe4\xfe\xc1wO%d\xc2\xe8M\xcfHf\x90XA\x9e\x9e\xdd\xe3\xd9\x9f\xa7!?b;J&U\x8b3\xe5\xd2\x12h\xae\xccy\x8cvz6\xf8\x9aH\x8dx\xef\xf7\xb2F=\xde\xf7\xef\xde\xbbL\xb3\xb3\x0b\x1f\xe5\xfb\x89=\x9b;\xbb\x8fLE\xd7\xe3\xa8\x94"\xef,\x9a\xe7\xc0K\xa4ph\xba\xa6\x877\x18,\xc4{\x11c7\xb3\x19\x08k\xd25\xb1q\xf7\x99\xd8A\xc2[W4\x99\\\x89\x98\x1bU\xb6\xfa\\\x9a\xedEJ\x00\x98\xaf\x0c\x94\x08\xc9\xa2p\xeaT?6\x98\xa1\xa7C\xf5tK&\x130t\xf8r\x7fv\x83\xf0\x83\x98Bj\x02\n\xd8\x00\xd6\x00\xbf\xcb\xa6\x0fk\xdbw\xe0\xffA\x117\x01,\x18)\xdas\xb2;\x10\x9eh\x8b\xca9\xf1\'tj\xb07\xe7\xb1\xbf\xa3\x1c+0\r\x91\xac\xac\xea\xb3\xd8\xbb}\x9e\x19\xa2.\x19\xf04\xd77~H!\xfb\xb3C\x06V\x98k\xf4\x9c\xb3\xeb\x1a\xbe=\xd5\\\xf4\x91\x034I`S\x14\xae\xe0/\xc9*2\xfe\xc9\x94v\xb8\x88\xe0p\xc3RyH\xa2\xc3O#\x98\x99\x81\xd6\x11X\xa0\x0c\t\xc0\xb0^\xf5%\xbd\xbb\x11\x95~\xb7)\x1f\xe5\x92\xd3\xc0\x1c\x10\x1e\xcd\xce\x0e\x0ba\xc1\xdb\xfdM\x12B\xd2\x846Q\xdc\xf0\xd4W\xf8\xc1>K\xe4\xccN2\xfe\xf95\xcd+\xc2p\xb9"7\xa5\x0e\x08qe\x19\xfc$>\x84\xc6-!\xaf\x0e]\xe3j\x19y)\x11\x8c\x15~\x88\xae4\x04\xfc\xd8\x18+\xa8\x02\x14&\xd6&T\xce:S\xe8"\xae>\xfa\xe1\x0f\xe5X\xc85\x83p\x92\xf6\x08s\xf0\x1f.\xdb*\x88\xb2f\ne\xa7\x90\xfe\xde\xc8\xb5\xf4>\xc1\xd2+\xd8\x86\x03\x1b\xe1\xfe\x84:\x8eE\xdeZ#\xf1\xa7o\x0c\x05\xe2\x81\x97\xb3A\xbb\'\x1e\xbf_\xca\x9bP\x13\xc7/?\x9f2\x9d\n\xd2k9\x16b\xfd\x11\xf9\x8a\x9eM^V*\xf3ya\xadjW\x0c\xb63\xdf\x98=\xcfV\x18\x84\xabm\xee\xb2o\x13\xfa\xd6\xd3\xde)\x15\'@\xc06f\xbf\t\xaf\x8f\xee]\xc5\xde\x04\xb7~\xb3\xb5\x05\x8d!\n++\xde\x16\xe5S Y\xdcC\x04\xbdE)\x11\xfa\xb8\x03\xbfh\xb8\xed\xfe\xb5m80\x05\x8dG\xc9\x92\x10I\xf4C\xb6\xc5\xdd\xd1\xdd\xd6sM\xc0\xa1\x82\x87\xc28C\xb0\n\x17\x81\xb5\x15\x1d\xeb;\x83U|Q\xd58|\x93|Lb1\xc2i\x1dE\xcd\xd3^\xdf\x1fI\tf\\\xe1\xe1\xd1ER\xdd\x81\x9a\xc0-\xfc:\xb1L\xc5O\xdf\x10Q\xc0\x02\xe3(S\x12\xf7^\\}\xdc\r\xda!\xa25\xad\xb3\x96\xac\xed]\xe3\x9c\x11\xe3\x00qC\xc7\xd1O\x0f\xe9}\x9c\xd4\xddL\xd2\x9fz\x0e\xea\xbb\x9e\xa7Jr\xf21\xf8\xfb \x18 \xbd\x94\x92\xb3L\n\xb0\x01O\x8a\xa7\xa3\xf0G\x91zA^ \xda\x83<\xc8\xe2\x1b(\xda\xfe\xc8\xd9\xda\xf8\x9a|\xb0\xa9\xfb%F[\xa7\x12\xca\x83q\xea\x86\x88!!\xbf\x16\x8b\xdf\xe9\xae\xe0\x9a\xf1\x10:p\xdb\x16\xba\x94d\xca\x8a\'\xc8\xdf\x00?\xbf\x8e\xd1C\xe2#\xd3\x08y\xffgY\x02\xb3\x89c\xb7|\xdc\xdc;\x97,\xffwl\x9a\x93\x0c\xec\xeaL\xa6xa\xc1\xa5\xb7\xa0\x1eE\x8cD\xb2\x1a\xdc\xc1\xaeN\xfd\xf3(\x8d\x8b\xbf*m_m\x0e\xbe8\x9a\xab\x9c\xde\xa3x\xd6\xe2^\xd3z\x85\xb5\xf0\xb7BMQ@\x13v\xd0{3\x84\xa5\xbfB\xa8\xe3XA\xae\x16\xe5w4\x91\rN\xf2\x00ee\xf7\x02\x8a\xf8\xbe+\xafHv\x94\x9ac<i\xc5aY\xcd\x97=\xe1\x13\xe8\xeef\xed\xe0\xee\x84c9d\xf0\xc0\xa8n\xc9"s\x06Z`w\x02\x02%\x02#\xf3Rj\x99\x7f!\xb5}?m\x9b~=\xc1\x8d3\x9f\xbd\xdc\x00<\x1f\x8f\xbe\xac\xc0\x08\\\xce?\x8fm\xb7A\xbdz\xf7\xa7\xb7;\xcc6\x98?&u\xef\x89\xcc\xd8!!#\xd7\x82\x1ev\x866r\xdd\x88.\x99O"\xad\x1fd)ofy\xab@q\xd4b\x8e|\x01x<z\xc0\x8c\x85\\\xad)\x1c:\x12\xed"F\x1f\xe3\xafB\xaf\xf3\xedG\x15hY\xaa7\x80\x9b>\xaf\xf3\x0ft\x937\x924@q8\xce\xbe\x96]W\x1e\xda\x7fr_\xde\x9f\x8f\xbfm\xb1\xbf\x85\x16\x8a\xb9l\xb1\xeb8\xa7\xe2$\xfa\xce\x80\xa8\xea\x848\xdd\x81\xe3\x9f\xd7\x9d\xc4\xfcH\xdck/s\xe7P\xbe\xa68\x0b \x82\x16\xdbe\x98\x02\xdf\xec(\xa8\x8dM\x12\xfaU\xc0\x8b\xe7w\x9f\xa2`\xd4\x9dj\x85\xe5\xe1\x04\xbcA\xe3\xbf\x88\x95?\x8e5\xa6\x82\xd5\xc44\xc0zz\xac\xacoF;$\xc2\x11x\x04\xa9\xbd\xd737/\x12\n\x9f\xdf\x8a\x0f1\x8b6\x01\x16\xc8\x91\x13L\x88e*.;3\x05\x93p\x0c\x93N\x19$\xd9\xf3\x06|\xad\xa8\x80\xdd>\xaf\x84W\xda3\'\x01\xd7\xf0?![\x07qg\x95\x99\\\x06\xbc\x7f\xa6\xb3J\xa1\x9c<\xbd\xae\xcal\xf2\xf4\x8c\xd1\xc7\x9f\xa5Lns.^CJ\xfdV\x13zY7C\x00"x\xba\xd1\xa1\xe4|\x8c\xb6!\xd9$\xee\xa7\t\xa8L\xfd\xd2\xc4\x8d@?\x91\x9aoMC\x05\x0b9\xf8\xe6\x94\x90\xc3\xf9\x85\xd7)+\xaa\x95G\xf6r\x17/D\xf6\xb8\xe0\xb1\x13\x17\xa1\x92\x0bQ\x94a\xac\x99\xbcHNb?\xbdZ\xd7\xb3\x7f\x92\xb8\xa89\x1a\xcb(`%\x94k\xa3\x12\x03\'\xcb\xedN\xbfA\x90\x85\xc0\xd1/&\x1a\x04\xf7z\x9d?u\xccb\xb0\xd3[\xa3\xae\xf5\xb7\x9c\'\xec<\x8dxh\xf1\xcb\xb3o\x0f\xd0\xcb\xd5f\x1f\x10\xf1)\xb0V\xbeW\'dUef\xb7VO\x1fe\x9d\x06\x15]\x92\x92\x9b\xc8\xa3d\x07\xd0<\xb8\xe4q\xf1\xeb\x11\xb0\x8cq\x08k\x9bx\xde\x04\xa3\r1\x85-\xd1\x08r\xf2\x08-N\xc0w\x04\x96\xe8T\x05e\xf8d\x1d\xf5\xfa\t\x15\x8dg/%2\xf9T\xa0\xc4\xb2\x06\x81Z-M\xe1\xfe\x9fO\xc8\x9d\x08a\\8\xa3\xa1n7T\x10\xcc3\xa6\xdb\x80\x08\x84\xb9\xc2\x91\xd0W\xab\xb2\xae\xf8\xeb\xf6\x1c\x02\x9e\xa2;n7\x15\xb4I<\xc3\x08\x03:$\xe1\x9cC+`%\xb5\x89\x9fO\xb8\xe5\xdd\x02a\xfb,\x087\x13\t\xc5\x9e\x1f&w\x88\xb7\xea\xd8\x88f\xb4\xed\\\x14\xeb\x96\x05\xc1\xcc\x86\xd7\xd4\xfa\x11\x9ba\x93\'\xb5\xa4\x81\xf0X\xd8x\x82\xf1\x1a\xfb\x97)\xb9\x9f\x8f\xd7$\xe9\xd6\xb4\x1a\xfe\xf3p\x9a\xeb\x98\x8f|\x89R\xadE\x00\x12[hD\xccw\xfa\xae\xec\xe1Hm\xcf\xb8\x87\xe3U\x80\xc3\x85\x18\x9d\xb3n\xaf{\xb6\x93\xd1/\xb5R\xeb\x80\x0b\x0b\xa7\xbc\x98\x8az\x89\x88G\xe8aO\xfe-\x9a\x8d\xfb\xca\x93\xd8\x10\xc6\x82\xb6t\xc2m\xad\xc1n\x03\'\x97\x85\x0b@\xe6\xc8\x0eV\xae\x00Y\x1d j\x86\xf4!\xc9\xb3\xce\x14l\t\x891\x1297\xff\xc7\xc2\x85wPK\x01\x02?\x00?\x00\x02\x00\x0e\x00\x00\x00!\x00\xaanPL\xb7\x1c\x00\x00\xbbZ\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x00\x00\x00\x00lorem.txtPK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x007\x00\x00\x00\xde\x1c\x00\x00\x00\x00'
        temp_zip = tf.NamedTemporaryFile("wb", delete=False)
        temp_zip.write(lorem_zip)
        temp_zip_loc = temp_zip.name
        temp_zip.close()
        with zf.ZipFile(temp_zip_loc) as z:
            with z.open("lorem.txt") as f:
                lorem = f.read().decode("utf-8").splitlines()
        remove(temp_zip_loc)
        return lorem


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Type random words from the dictionary")
    parser.add_argument("-l", "--lorem", help="Use the lorem lipsum dictionary instead of the english dictionary",
                        action="store_true")
    parser.add_argument("-min", metavar="3", help="Minimum amount of words", type=int, default=3)
    parser.add_argument("-max", metavar="50", help="Maximum amount of words", type=int, default=50)
    args = parser.parse_args()
    tkWin = Typing()
