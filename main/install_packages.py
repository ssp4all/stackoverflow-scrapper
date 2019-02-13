# Program to be executed First
import os
import subprocess
import sys
from os import path

from funtions import run, runrealtime, toString


def install():
    #
    # checking for python version 3
    #
    print("Checking if Python installed...")
    if os.name == 'nt':
        output, error = run(["python", "-V"])
    else:
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
    if os.name == 'nt':
        output, error = runrealtime(
            ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    else:
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
        here = path.abspath(path.dirname(__file__))
        p = here + "/requirements.txt"
    else:
        p = sys.path[0]+'/requirements.txt'  # path for req. file(linux)
    
    try:
        print("Installing required packages...")
        if os.name == 'nt':
            output, error = runrealtime(
                ["pip3", "install", "-r", p])
        else:
            output, error = runrealtime(
                ["pip3", "install", "-r", p])

        if len(error) == 0:
            print('Done, Good to GO!')
        else:
            print(toString(error))
            print()
            print('Error...Unable to Download packages!')
            exit(0)
    # else:
    except FileNotFoundError:
        print('Requirement File not found - Check directory!')
        print()
        print('Incomplete Requirements...Exiting!')
        exit(0)

if __name__ == "__main__":
    install()
