# Program to be executed First

import os
import subprocess
import sys


def toString(byte):
    return byte.decode("utf-8").strip()


def run(args):
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def runrealtime(args):
    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while process.poll() is None:
        output = process.stdout.readline().decode("utf-8").strip()
        print(output)
    return process.communicate()


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

if 'requirements.txt' in os.listdir():
    print("Installing required packages...")
    output, error = runrealtime(
        ["pip3", "install", "-r", "requirements.txt"])

    if len(error) == 0:
        print('Done, Good to GO!')
    else:
        print(toString(error))
        print()
        print('Error...Unable to Download package!')
        sys.exit()

else:
    print('Requirement File not found - Check directory in which you are running!')
    print()
    print('Incomplete Requirements...Exiting!')
    sys.exit(1)
