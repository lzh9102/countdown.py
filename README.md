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
