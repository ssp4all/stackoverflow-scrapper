# This file will extract error from file passed as extension
import os
import re
import sys

from termcolor import colored

from animals import print_animal
from App import App
from execution import execute
from funtions import *
from get_error import get_error_message
from logo import logo
from scrape import *
from ScrollBar import ScrollBar


def main():
    # Main function here
    search_results = []
    if len(sys.argv) == 1 or sys.argv[1].lower() == '-h':
        clear_terminal()
        print_help()
    elif sys.argv[1].lower() == '-q' or sys.argv[1].lower() == '--query':
        query = ' '.join(sys.argv[2:])

        soup, captcha = search_stackoverflow(query)
        if captcha:
            print(colored("\n Sorry, Captcha blocked our request", 'red', attrs=['reverse']))
            clear_terminal()
            sys.exit(0)
        search_results = get_search_results(soup)
        if search_results != []:
                if captcha:
                    print(colored(
                        "\nSorry, Stack Overflow blocked our request. Try again in a minute.\n", 'red', attrs=['reverse']))
                    clear_terminal()
                    sys.exit(1)
                else:
                    print_animal()
                    clear_terminal()
                    App(search_results)  # Opens interface
        else:

            print(colored("\nNo Stack Overflow results found. Try other keywords!",
                              'red', attrs=['reverse']))
            clear_terminal()
            sys.exit(0)

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
            search_results = get_search_results(soup)
            
            if search_results != []:
                if captcha:
                    print(colored("\nSorry, Captcha blocked our request.\n", 'red', attrs=['reverse']))
                    return
                else:
                    if confirm("\nDisplay Stack Overflow results?"):
                        print_animal()
                        clear_terminal()
                        App(search_results)  # Opens interface
            else:
                print(colored("\nNo Stack Overflow results found.\n", 'red', attrs=['reverse']))
        else:
            print(colored("\nNo error detected :)\n", 'cyan', attrs=['reverse']))



## Main ##

if __name__ == "__main__":
    main()
