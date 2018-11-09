# This file will extract error from file passed as extension

import sys
import os
from scrape import get_search_results
########################################
# Get file type by knowing its extension
########################################

def get_language(file_path):
    if file_path.endswith(".py"):
        return "python3"
    elif file_path.endswith(".js"):
        return "node"
    elif file_path.endswith(".go"):
        return "go run"
    elif file_path.endswith(".rb"):
        return "ruby"
    elif file_path.endswith(".class"):
        return "java"
    else:
        return ' '  # Unknown filetype


########################################
# Extract error
########################################
def get_error_message():
    print("Checking for the error in the testing file...")
    output, error = runrealtime(["python", "buggy-file.py"])
    if len(error) == 0:
        print('Done, Good to GO!')
    else:
        err = toString(error)
        er = re.search('\n(?:[ ]+.*\n)*(\w+: .*)', err).groups()
        error = er[0]  # To get first element of tuple consists of errors
        # print(value) 
        print('Error...Unable to run file!')
        # sys.exit()          

    return error

def print_help():
    print('Help --> Intelligent-Codemate')
    print('WELCOME to IC')


########################################
# Accept file
########################################

def main():
    if len(sys.argv) == 1 or sys.argv[1].lower() == '-h':
        print_help()
    elif sys.argv[1].lower() == '-q' or sys.argv[1].lower() == '--query':
        query = ' '.join(sys.argv[2:])
        print(query)
        get_search_results(query)
        # search_results, captcha = seach_stackoverflow(query)

        # if search_results != []:
        #     if captcha:
        #         sys.stdout.write("\n Sorry, Try again Later")
        #         return
        #     else:
        #         return #currently Do nothing
    else:
        language = get_language(sys.argv[1].lower())
        print(language)
        if language == ' ':
            sys.stdout.write("\nSorry, Unknown File type...")
            print()


if __name__ == "__main__":
    main()
