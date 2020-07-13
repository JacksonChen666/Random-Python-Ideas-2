import signal
from os import getpid


def signalHandler(num, frame):
    print(f"\rReceived signal: {num}")
    return


if __name__ == '__main__':
    things = [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGILL, signal.SIGTRAP, signal.SIGABRT,
              signal.SIGBUS, signal.SIGFPE, signal.SIGUSR1, signal.SIGSEGV, signal.SIGUSR2, signal.SIGPIPE,
              signal.SIGALRM, signal.SIGTERM]
    for i in things:
        signal.signal(i, signalHandler)

    print(f"Waiting for signals... PID: {getpid()}")
    while True: signal.pause()
