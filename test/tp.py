import subprocess
import sys
import os

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
#checking for python version 3
#
print("Checking if Python installed...")
error, output  = run(["python3", "--version"])
if len(error) != 0:
    #python 3 is not installed
    print("install python 3")
    print()
    sys.exit(1)
else:
    print('Python installed')
    print()

#
#checking if pip installed
#
print("Checking if pip installed...")
output, error = run(["pip3", "--version"])

if len(error) != 0:
    #pip not installed
    print("pip not installed")
    print()
else:
    #pip is installed. proceed further.
    print("pip is installed")
    print()

#
#Upgrade setuptools and wheel
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
    print(error)
    print(output)
else:
    print('Requirement File not found')
    print()
    print('Incomplete Requirements...Exiting!')
    sys.exit(1)
