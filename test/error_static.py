# extract error using python script

import re
sample = '''\
Traceback (most recent call last):
    File "sample.py", line 1, in <module>
        hello 
NameError: name 'hello' is not defined
 '''

error = re.search(
    r'Traceback \(most recent call last\):\n(?:[ ]+.*\n)*(\w+: .*)', sample).groups()

print(error)
