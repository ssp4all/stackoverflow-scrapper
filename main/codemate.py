# This file will extract error from file passed as extension
import os
import re
import sys

from termcolor import colored

from execution import execute
from funtions import runrealtime, toString
from get_error import get_error_message
from scrape import *
from terminal import get_terminal_size

# ASCII color codes
GREEN = '\033[92m'
GRAY = '\033[90m'
CYAN = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'

########################################
# Get file type by knowing its extension
########################################


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


def print_help():
    print()
    print(colored('%sIntelligent-Codemate Developed by %s@ssp4all','red')%(BOLD, GREEN))
    print(colored('WELCOME','green'))
    print()
    print('1]   python codemate.py -q your_query_here')
    print()
    print('2]   python codemate.py your_file.py')
    print()
    print('3]   python codemate.py')


########################################
# Accept file
########################################

# Get terminal size
sizex, sizey = get_terminal_size()

def main():
    # Main function here
    if len(sys.argv) == 1 or sys.argv[1].lower() == '-h':
        print_help()
    elif sys.argv[1].lower() == '-q' or sys.argv[1].lower() == '--query':
        query = ' '.join(sys.argv[2:])

        print()
        print('#'*sizex, end='')  # find current teminal width
        print(query.upper())
        print('#'*sizex)
        print()
        soup, captcha = search_stackoverflow(query)
        if captcha:
            print(colored("\n Sorry, Try again Later",'red'))
            return
        get_search_results(soup)
        

    else:
        language = get_language(sys.argv[1].lower())
        if language == ' ':
            sys.stdout.write("\nSorry, Unknown File type...")

        file_path = sys.argv[1:]
        error_msg = get_error_message(file_path, language)
        
        if error_msg != None:
           
            # Fix language compiler command
            language = 'java' if language == 'javac' else language
            query = "%s %s" % (language, error_msg)
            soup, captcha = search_stackoverflow(query)

            if soup is not None:
                if captcha:
                    print("\n%s%s%s" % (
                        RED, "Sorry, Stack Overflow blocked our request. Try again in a minute.\n", END))
                    return
                c = input('Do you want to seach web(y/n) :')
                if c == 'y':
                    get_search_results(soup)
                else:
                    print('Exiting....')
                    exit(1)
            #     elif confirm("\nDisplay Stack Overflow results?"):
            #         App(search_results)  # Opens interface
            else:
                print("\n%s%s%s" %
                      (RED, "No Stack Overflow results found.\n", END))
        else:
            print("\n%s%s%s" % (CYAN, "No error detected :)\n", END))


if __name__ == "__main__":
    main()
