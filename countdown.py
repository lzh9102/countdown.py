#!/usr/bin/env python
# countdown.py - A simple countdown timer in python
# Author: Che-Huai Lin <lzh9102@gmail.com>

import time
import argparse
import re

# TODO: i18n
_ = lambda s: s;

class Countdown(object):

    def __init__(self, args):
        self.args = args
        self.until = time.time() + args.duration
        self.refreshInterval = 1

    def display(self):
        diff = self.until - time.time() + 1
        print _("remaining seconds: %d") % diff

    def start(self):
        try:
            while time.time() < self.until:
                self.display()
                time.sleep(self.refreshInterval)
        except KeyboardInterrupt:
            return False
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
