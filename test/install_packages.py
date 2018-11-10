# Program to be executed First

import os
import subprocess
import sys
from pathlib import Path, PureWindowsPath

from funtions import run, runrealtime, toString

def install():
    #
    # checking for python version 3
    #
    print("Checking if Python installed...")
    output, error = run(["python3", "-V"])
    if len(error) != 0:
        # python 3 is not installed
        print('Python installed')
        print(toString(output))
        # sys.exit(1)
    else:
        print("Python3 not installed!")
        print()

    #
    # checking if pip installed
    #
    print("Checking if pip installed...")
    output, error = run(["pip3", "-V"])

    if len(error) != 0:
        # pip not installed
        print("pip not installed")
        print()
    else:
        # pip is installed. proceed further.
        print("pip is installed")
        print()

    #
    # Upgrade setuptools and wheel
    #
    print("upgrading setuptools and wheel...")
    output, error = runrealtime(
        ["python3", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    if len(error) != 0:
        print(toString(error))
        sys.exit(1)

    #
    # install packages from requirement.txt
    #
    print()
    print("Checking for requirement file...")
    if os.name == 'nt':
        path = PureWindowsPath(sys.path[0]+"/requirements.txt")  # for Windows
    else:
        path = sys.path[0]+'/requirements.txt'  # path for req. file(linux)
    cpath = Path(path)
    try:
        print("Installing required packages...")
        output, error = runrealtime(
            ["pip3", "install", "-r", cpath])

        if len(error) == 0:
            print('Done, Good to GO!')
        else:
            print(toString(error))
            print()
            print('Error...Unable to Download packages!')
            sys.exit()
    # else:
    except FileNotFoundError:
        print('Requirement File not found - Check directory!')
        print()
        print('Incomplete Requirements...Exiting!')
        exit(1)

if __name__ == "__main__":
    install()