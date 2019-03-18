# Program to be executed First
import os
import sys
from termcolor import colored

from funtions import run, runrealtime, toString
from loader import loader


def install():
    """Checking for python version 3 """
    print()
    print(colored("Checking if Python installed...", 'blue', attrs=['reverse']))
    if os.name == 'nt':
        output, error = run(["python", "-V"])
    else:
        output, error = run(["python3", "-V"])
    res = len(output)
    # print(error)
    if res == 0:
        # python 3 is not installed
        loader(res)
        print(colored('PYTHON is installed', 'green', attrs=['bold']))
        print(toString(output))

    else:
        loader(res)
        print(colored("PYTHON is not installed!", 'red', attrs=['bold']))
        print()

    #
    # checking if pip installed
    #
    print(colored("Checking if PIP installed...", 'blue', attrs=['reverse']))
    output, error = run(["pip3", "-V"])
    res = len(error)
    if res != 0:
        # pip not installed
        loader(res)
        print(colored("PIP not installed", 'red', attrs=['bold']))
        print()
    else:
        # pip is installed. proceed further.
        loader(res)
        print(colored("PIP is installed", 'green', attrs=['bold']))
        print()

    #
    # Upgrade setuptools and wheel
    #
    # print("upgrading setuptools and wheel...")
    # if os.name == 'nt':
    #     output, error = runrealtime(
    #         ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # else:
    #     output, error = runrealtime(
    #         ["python3", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    # if len(error) != 0:
    #     print(toString(error))
    #     sys.exit(1)

    # #
    # # install packages from requirement.txt
    # #
    # print()
    # print("Checking for requirement file...")
    
    # if os.name == 'nt':
    #     here = path.abspath(path.dirname(__file__))
    #     p = here + "/requirements.txt"
    # else:
    #     p = sys.path[0]+'/requirements.txt'  # path for req. file(linux)
    
    # try:
    #     print("Installing required packages...")
    #     if os.name == 'nt':
    #         output, error = runrealtime(
    #             ["pip3", "install", "-r", p])
    #     else:
    #         output, error = runrealtime(
    #             ["pip3", "install", "-r", p])

    #     if len(error) == 0:
    #         print('Done, Good to GO!')
    #     else:
    #         print(toString(error))
    #         print()
    #         print('Error...Unable to Download packages!')
    #         exit(0)
    # # else:
    # except FileNotFoundError:
    #     print('Requirement File not found - Check directory!')
    #     print()
    #     print('Incomplete Requirements...Exiting!')
    #     exit(0)

if __name__ == "__main__":
    install()
