import re
import random
import subprocess
import sys
import os
from funtions import toString, run, runrealtime


print("Checking for the error in testing file...")
output, error = runrealtime(["python", os.path.join(
    sys.path[0], "buggy-file.py")])  # check directory

if len(error) == 0:
    print('Done, Good to GO!')
else:
    err = toString(error)
    er = re.search(
        '\n(?:[ ]+.*\n)*(\w+: .*)', err).groups()
    value = er[0]  # To get first element of tuple consists of errors
    print(value)    
    print('Error...Unable to run file!')
    # sys.exit()
