#!/usr/bin/env python
# countdown.py - A simple countdown timer in python
# Author: Che-Huai Lin <lzh9102@gmail.com>

import time
import argparse

# TODO: i18n
_ = lambda s: s;

class Countdown(object):

    def __init__(self, args):
        self.args = args
        self.until = time.time() + int(args.duration)
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

def parse_args():
    parser = argparse.ArgumentParser(
        description=_("A simple countdown timer"))
    parser.add_argument('duration', type=str,
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
