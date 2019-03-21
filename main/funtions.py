""" 
This file contains all utility functions!
"""
import os
import subprocess
import time
from termcolor import colored
from logo import logo

    
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
        # print(output)
    return process.communicate()

def clear_terminal():
    """Clear terminal """
    time.sleep(3)
    if os.name != 'nt':
        os.system("clear")
    else:
        os.system("cls")


def confirm(question):
    """Prompts a given question and handles user input."""
    valid = {"yes": True, 'y': True, "ye": True,
             "no": False, 'n': False, '': True}
    prompt = " [Y/n] "

    while True:
        print(colored(question + prompt, 'white', attrs=[
            'reverse'] ))
        choice = input().lower()
        if choice in valid:
            return valid[choice]

        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def print_help():
    logo()
    print(colored('\nIntelligent-Codemate Developed by @ssp4all\n',
                  'yellow', attrs=['reverse', 'bold']))
    print(colored('\nTry following commands...', 'green', attrs=['underline']))
    print('\n$   python codemate.py -q your_query_here')
    print('\n$   python codemate.py your_file.py\n')


def get_language(file_path):
    """Returns the language a file is written in."""
    if file_path.endswith(".py"):
        return "python3"
    elif file_path.endswith(".js"):
        return "node"
    elif file_path.endswith(".go"):
        return "go run"
    elif file_path.endswith(".rb"):
        return "ruby"
    elif file_path.endswith(".java"):
        return 'javac'  # Compile Java Source File
    elif file_path.endswith(".class"):
        return 'java'  # Run Java Class File
    else:
        return ''  # Unknown language
