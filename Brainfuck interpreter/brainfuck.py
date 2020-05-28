#!/usr/bin/env python3# original: https://github.com/pocmo/Python-Brainfuckfrom os import namefrom time import timeimport loggingimport traceback as tbli, ld, lw = logging.info, logging.debug, logging.warninguIP = True# i can't seem to get the original sourceif name == 'nt':    import msvcrt    def g(): return msvcrt.g().decode()else:    import sys, tty, termios    fd = sys.stdin.fileno()    try: old_settings = termios.tcgetattr(fd)    except termios.error:        lw("Getting user input is impossible without the correct interactive shell. If your code contains user input, it will not continue.")        uIP = False    def g():        try:            tty.setraw(sys.stdin.fileno())            ch = sys.stdin.read(1)        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)        return chdef is_int(strs):    try: int(strs); return True    except ValueError: return FalselogFormat = "%(levelname)s:%(message)s"def evaluate(cd, non8bit=False, maxMemPrint=100, debugger=False, eTime=False, debug=False, verbose=False):    """    This part of the code executes brainfuck code, and can be used by modules.    :param cd: Brainfuck code    :param non8bit: Allow memory to go beyond numbers between 0 and 255    :param maxMemPrint: How much of the memory should be showed    :param debugger: Stops at every piece of code to see what's happening    :param eTime: Print execution time after executing    :param debug: Logging debug (Memory, Memory pointer position, Code position alongside running code)    :param verbose: Logging verbose (Code, Bracemap)    :return: Memory after execution    """    global skips, continuing    if not uIP:        if "," in cd: raise Exception("The code contains user input commands, and your console does not have support. Please check your console.")        elif debugger: raise Exception("You cannot use debugging mode without user input support")    if debug or debugger: logging.basicConfig(level=logging.DEBUG, format=logFormat)    elif verbose: logging.basicConfig(level=logging.INFO, format=logFormat)    if maxMemPrint < 0 or debugger: maxMemPrint = 0xffffffffff    cd, mm, mp, cp, p, d = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], cd)), [0], 0, 0, sys.stdout.write, debugger; bm = bbm(cd)    li("Code: {}".format(cd))    li("Bracemap: {}".format(bm))    printText = ""    if debugger:        if __name__ != "__main__": lw("Debugging was enabled outside of itself. Not recommended!")        li("Started debugging session")        li("Press Control-C to stop executing, or Control-D to stop debugging (forever this session), or press any key to go to next part of code. Numbers to skip how many parts of code, 0 is 10 parts. Use - to remove from skips. After that, using enter to skip specified lines.")        skips, continuing = 0, False    t0 = time()    while cp < len(cd):        if debugger: ld("Debugger: Mem: {}\tMem pos: {}\tCode pos: {}/{}\tNext code: {}".format(mm, mp, cp + 1, len(cd), cd[cp]))        elif not len(mm) >= maxMemPrint and not debugger: ld("Mem: {}\tMem pos: {}\tCode pos: {}/{}\tNext code: {}".format(mm, mp, cp + 1, len(cd), cd[cp]))        elif len(mm) >= maxMemPrint and not debugger: ld("Mem: {}\tMem pos: {}\tCode pos: {}/{}\tNext code: {}".format(len(mm), mp, cp + 1, len(cd), cd[cp]))        while debugger and d:            if skips != 0 and not continuing: break            elif skips == 0: continuing = True            print("Skips: {} ".format(skips), end="\r", flush=True)            t = ord(g())            if t == 3: li("Canceled"); return mm            elif t == 4: li("Debugging session ended"); debugger = False            elif is_int(chr(t)) and 0 <= int(chr(t)) <= 10: skips = skips + int(chr(t)) if 10 > int(chr(t)) >= 1 else skips + 10            elif "-" in chr(t) or "+" in chr(t): skips = 0 if skips <= 0 and chr(t) == "-" else skips + 1 if chr(t) == "+" else skips - 1            else: skips = 1 if skips == 0 else skips; continuing = False        c = cd[cp]        try:            if c == ">" or c == "<": mp = mp + 1 if c == ">" else mp - 1 if not mp <= 0 and c == "<" else 0; mm = mm + [0] if mp == len(mm) else mm            elif c == "+": mm[mp] = mm[mp] + 1 if mm[mp] < 255 and not non8bit else mm[mp] + 1 if non8bit else 0            elif c == "-": mm[mp] = mm[mp] - 1 if mm[mp] > 0 and not non8bit else mm[mp] - 1 if non8bit else 255            elif c == "[" and mm[mp] == 0 or c == "]" and mm[mp] != 0: cp = bm[cp]            elif c == ".": p(chr(mm[mp])); printText += chr(mm[mp])            elif c == ",": mm[mp] = ord(g())        except KeyError:            tb.print_exc()            print("Possibly unbalanced amount of brackets")        cp += 1        if debugger: skips = 0 if skips <= 0 else skips - 1    t1 = time()    if not d and eTime: print("\nFinished code execution in {} seconds".format(round(t1 - t0, 15)))    if (debug or debugger) and uIP: p(printText)    return mmdef bbm(cd):    tbs, bm = [], {}    for ps, c in enumerate(cd):        try:            if c == "[": tbs.append(ps)            elif c == "]": s = tbs.pop(); bm[s], bm[ps] = ps, s        except IndexError:            tb.print_exc()            print("Possibly unbalanced amount of brackets")    return bmdef consoleMode():    if __name__ != "__main__": return False    global code    import argparse    # argparse known bug: using "-" as the first character with inline code breaks the thing    parser = argparse.ArgumentParser(description="Run Brainfuck code")    parser.add_argument("FileCode", type=str, help="File of code or just code (Uses file if file with the exact name exists)", default=None)    parser.add_argument("-D", "--debugger", help="Debugger for Brainfuck", action="store_true")    parser.add_argument("-m", "--memory", help="Print memory after completed execution", action="store_true")    parser.add_argument("-f", "--full", help="Allow numbers over 255 and under 0 (may break some code)", action="store_true")    parser.add_argument("-t", "--time", help="Get the execution time after execution", action="store_true")    parser.add_argument("-d", "--debug", help="Shows info about: Memory, Memory pointer position, Code position alongside running code", dest="debug", action="store_true")    parser.add_argument("-v", "--verbose", help="Shows info about: Code, Bracemap", action="store_true")    parser.add_argument("-l", "--length", metavar="number", help="Limits the maximum size of the memory can be logged (in debug only). 0 disallows memory printing and -1 and below prints no matter what", type=int, default=100)    args = parser.parse_args()    if args.debugger: logging.basicConfig(level=logging.DEBUG, format=logFormat); li("Debugger enabled, specific settings has been overwritten")    elif args.verbose: logging.basicConfig(level=logging.INFO, format=logFormat)    elif args.debug: logging.basicConfig(level=logging.DEBUG, format=logFormat)    ld("Arguments: {}".format(args))    if args.FileCode:        try: code = open(args.FileCode).read()        except FileNotFoundError: code = args.FileCode    else: return parser.print_usage()    mmOut = evaluate(code, args.full, args.length, args.debugger, args.time, args.debug, args.verbose)    if args.memory: print("\nMemory: {}".format(mmOut))    return codeif __name__ == "__main__": consoleMode()