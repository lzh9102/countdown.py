countdown.py
============

_A simple command-line countdown timer written in python_

Usage
-----
	usage: countdown.py [-h] [-e EXECUTE] [-t TILL] [duration]

Options
-------
	duration            Duration of the countdown timer
	-t, --till TILL     Specify the time instead of duration.
	-e, --execute       EXECUTE  Execute command *EXECUTE* on timeup.

Examples
--------
	countdown.py 30        # delay 30 seconds
	countdown.py 1:20:30   # delay 1 hour 20 minutes and 30 seconds
	countdown.py 23:30     # delay 23 minutes and 30 seconds
	countdown.py -t 23:30  # delay until 11:30 PM

License
-------

Copyright (C) 2014 Che-Huai Lin <lzh9102@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
