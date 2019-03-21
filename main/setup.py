# Program to be executed First
import os
import sys
from termcolor import colored

from funtions import run, runrealtime, toString, clear_terminal
from loader import loader
from logo import logo

def install():
    """Checking for python version 3 """
    print()
    print(colored("Checking if Python installed...", 'white', attrs=['reverse']))
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
    print(colored("Checking if PIP installed...", 'white', attrs=['reverse']))
    output, error = run(["sudo","pip3", "-V"])
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

    
    # Upgrade setuptools and wheel
    
    print(colored("Upgrading setuptools and wheel...", 'white', attrs=['reverse']))
    if os.name == 'nt':
        output, error = runrealtime(
            ["sudo", "python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    else:
        output, error = runrealtime(
            ["sudo", "-H", "python3", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    res = len(error)
    if res != 0:
        loader(res)
        print(toString(error))
        sys.exit(1)
    else:
        loader(res)
    #
    # install packages from requirement.txt
    #
    print()
    print(colored("Checking for requirement file...", 'white', attrs=['reverse']))
    
    if os.name == 'nt':
        here = path.abspath(path.dirname(__file__))
        p = here + "/requirements.txt"
    else:
        p = sys.path[0]+'/requirements.txt'  # path for req. file(linux)
    
    try:
        loader(0) #succeess
        print(colored("Installing required packages...", 'white', attrs=['reverse']))
        if os.name == 'nt':
            output, error = runrealtime(
                ["pip3", "install", "-r", p])
        else:
            output, error = runrealtime(
                ["pip3", "install", "-r", p])
        res = len(error)
        if res == 0:
            loader(res)
            print(colored('Done, Good to GO!', 'green', attrs=['bold']))
            clear_terminal()

        else:
            loader(res)
            print(toString(error))
            print()
            print(colored('Error...Unable to Download packages!', 'red', attrs=['bold']))
            clear_terminal()
            exit(0)
    # else:
    except FileNotFoundError:
        loader(1)#error
        print(colored('Requirement File not found - Check directory!', 'red', attrs=['red']))
        print()
        print(colored('Incomplete Requirements...Exiting!', 'red', attrs=['reverse']))
        clear_terminal()
        exit(0)

if __name__ == "__main__":
    logo()
    install()
