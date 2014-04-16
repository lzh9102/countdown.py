#!/usr/bin/env python
# countdown.py - A simple countdown timer in python
# Author: Che-Huai Lin <lzh9102@gmail.com>

import time
import argparse
import re
import sys
import select
import tty

# TODO: i18n
_ = lambda s: s;

class Countdown(object):

    def __init__(self, args):
        self.args = args
        self.until = time.time() + args.duration
        self.refreshInterval = 1

    def moveCursor(self, row, col):
        """ Move the cursor to position (row, col). Row and column indices are
            zero-based """
        sys.stdout.write("\033[%d;%df" % (row+1, col+1))

    def hideCursor(self):
        sys.stdout.write("\033[?25l")

    def restoreCursor(self):
        sys.stdout.write("\033[?25h")

    def clearScreen(self):
        sys.stdout.write("\033[2J")

    def display(self):
        self.moveCursor(0, 0)
        self.clearScreen()
        diff = self.until - time.time() + 1
        print _("remaining seconds: %d") % diff

    def keyPressed(self, key):
        if key == "q":
            self.cancel = True

    def waitForKey(self, timeout):
        """ Wait for user input for at most <timeout> seconds. Returns the
            pressed if there is an input; None otherwise. """
        (rlist, wlist, xlist) = select.select([sys.stdin], [], [], timeout)
        if len(rlist) > 0:
            return sys.stdin.read(1)
        else:
            return None

    def start(self):
        # set raw input (read one character one time) and hide cursor
        tty.setraw(sys.stdin.fileno())
        self.hideCursor()
        self.cancel = False
        try:
            while time.time() < self.until and (not self.cancel):
                self.display()
                key = self.waitForKey(timeout=1)
                if key:
                    self.keyPressed(key)
        except KeyboardInterrupt:
            return False
        finally:
            self.restoreCursor()
        return True

def time_string(s):
    # match the pattern <hour>:<minute>:<second> (three integer numbers)
    # hour and minute are optional
    pattern = r'^(((?P<hour>[0-9]+):)?(?P<minute>[0-9]+):)?(?P<second>[0-9]+)$'
    match = re.match(pattern, s)
    if not match:
        msg = _("%r: malformed time format") % s
        raise argparse.ArgumentTypeError(msg)
    matched_groups = match.groupdict()
    # compute the total seconds
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    seconds = int(matched_groups["second"])
    if matched_groups["minute"]:
        seconds += int(matched_groups["minute"]) * SECONDS_PER_MINUTE
    if matched_groups["hour"]:
        seconds += int(matched_groups["hour"]) * SECONDS_PER_HOUR
    return seconds

def parse_args():
    parser = argparse.ArgumentParser(
        description=_("A simple countdown timer"))
    parser.add_argument('duration', type=time_string,
                        help="the countdown duration")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    countdown = Countdown(args)
    timeup = countdown.start()
    if timeup:
        print _("timeup")
    else:
        print _("cancelled")
