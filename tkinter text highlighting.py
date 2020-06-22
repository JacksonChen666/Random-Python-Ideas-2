from tkinter import *


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


win = Tk()
t = CustomText(win)
t.insert(END, "Green, Red, Normal, Red")
t.tag_config("green", foreground='green3')
t.tag_config("red", background="red2")
t.highlight_pattern("Green", "green")
t.highlight_pattern("Red", "red")
t.pack()

win.mainloop()
