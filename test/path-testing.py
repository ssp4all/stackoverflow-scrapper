from pathlib import Path, PureWindowsPath
import sys
import webbrowser
import os
# data_folder = Path("test/")

if os == 'nt':
    print('Linux')
else:
    path = PureWindowsPath(sys.path[0]+"/requirements.txt")
    print(path)
    if os.path.isfile(path):
        print('true')
    else:
        print('not found')
# print(file_to_open.read_text())
# webbrowser.open('http://github.com/ssp4all')
