import os
import sys
path = os.path.join(sys.path[0],'b.py')
print(path)


lol = os.path.isfile(os.path.join(sys.path[0]+'/a.py'))
print(lol)
