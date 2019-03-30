import itertools
import sys
import time

def spinner():
	spinner = itertools.cycle('-/|\\')
	for _ in range(30):
		sys.stdout.write(next(spinner))  # write the next character
		time.sleep(0.1)
		sys.stdout.flush()                # flush stdout buffer (actual character display)
		sys.stdout.write('\b')
