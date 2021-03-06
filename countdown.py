#!/usr/bin/env python
# countdown.py - A simple countdown timer in python
# Author: Che-Huai Lin <lzh9102@gmail.com>
# License: MIT License

import time
import argparse
import re
import sys
import select
import tty
import os
from dateutil import parser as dateparser

# TODO: i18n
_ = lambda s: s;

class Countdown(object):

    def __init__(self, args):
        if args.till:
            self.until = args.till
        elif args.duration:
            self.until = time.time() + args.duration
        self.args = args
        self.refreshInterval = 1

    def moveCursor(self, row, col):
        """ Move the cursor to position (row, col). Row and column indices are
            zero-based """
        sys.stdout.write("\033[%d;%df" % (row+1, col+1))
        sys.stdout.flush()

    def hideCursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def restoreCursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def clearScreen(self):
        sys.stdout.write("\033[2J")
        sys.stdout.flush()

    def printLine(self, s):
        sys.stdout.write("%s\n\r" % s)
        sys.stdout.flush()

    def timeStr(self, t):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

    def display(self):
        self.clearScreen()
        self.moveCursor(0, 0)
        now = time.time()
        diff = self.until - now + 1
        self.printLine(_("until: %s") % self.timeStr(self.until))
        self.printLine(_("now:   %s") % self.timeStr(now))
        if self.args.execute:
            self.printLine(_("command: %s") % self.args.execute)
        self.printLine("")
        self.printLine(_("press [q] to timeup immediately"))
        self.printLine(_("press [^C] to cancel"))

    def keyPressed(self, key):
        if key == "q":
            self.cancel = True
        elif key == "\003": # Ctrl-C
            raise KeyboardInterrupt()

    def waitForKey(self, timeout):
        """ Wait for user input for at most <timeout> seconds. Returns the
            pressed if there is an input; None otherwise. """
        (rlist, _, _) = select.select([sys.stdin], [], [], timeout)
        if len(rlist) > 0:
            return sys.stdin.read(1)
        else:
            return None

    def start(self):
        # save original tty state
        origmode = tty.tcgetattr(sys.stdin.fileno())
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
            # restore stdin to normal state
            tty.tcsetattr(sys.stdin.fileno(), tty.TCSAFLUSH, origmode)
            self.clearScreen()
            self.moveCursor(0, 0)
            self.restoreCursor()
        return True

def time_value(s):
    datetime = dateparser.parse(s)
    return time.mktime(datetime.timetuple())

def duration_value(s):
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
    parser.add_argument("-e", "--execute", type=str, default=None,
                        help="the command to execute on timeup or exit")
    # time can be specified either by duration (relative) or till (absolute)
    timespec = parser.add_mutually_exclusive_group(required=True)
    timespec.add_argument("duration", type=duration_value, nargs="?",
                          help="the countdown duration")
    timespec.add_argument("-t", "--till", type=time_value,
                          help="countdown until the given absolute time")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    countdown = Countdown(args)
    timeup = countdown.start()
    if timeup:
        print _("timeup")
        if args.execute:
            os.system(args.execute)
    else:
        print _("cancelled")
