from os import path
import sys
from pathlib import Path, PureWindowsPath

# if os.name == 'nt':
#     print('windows')
#     path = PureWindowsPath(sys.path[0]+"/requirements.txt")  # for Windows
# else:
#     path = sys.path[0]+'/requirements.txt'  # path for req. file(linux)
# print(path)
# cpath = Path(path)
# print(cpath)

here = path.abspath(path.dirname(__file__))
print(here+'\\req.txt')

