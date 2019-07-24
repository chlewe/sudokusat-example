import psutil
import sys
import os

from sys import stderr

def handler(signum, frame):
    print("signum {}".format(signum), file=stderr)
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        print("Child pid is {}\n".format(child.pid), file=stderr)
        print("Killing child.", file=stderr)
        try:
            os.kill(child.pid, 15)
        except OSError as e:
            print("Process might already be gone. See error below.", file=stderr)
            print(e, file=stderr)

    print("SIGNAL received", file=stderr)
    if signum == 15:
        raise TimeoutError("signal")
    else:
        raise InterruptedError("signal")

def nothing(signum, frame):
    print("SIGNAL received\n", file=stderr)
    print("SIGNAL ignored...\n", file=stderr)
