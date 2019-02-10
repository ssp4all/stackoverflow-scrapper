# i = 1
# print(str(i).join(''), end='')
# # print(' ', end='')
# print('hello'.capitalize(),end='')


# import webbrowser
# print('Enter b to open a link')
# if input() in ['b', 'B']:
#     url = 'fb.com'
#     webbrowser.open(url)

# import re
# str = "purple alice@google.com, blah monkey bob@abc.com blah dishwasher"

# ## Here re.findall() returns a list of all the found email strings
# # ['alice@google.com', 'bob@abc.com']
# emails = re.findall(r'[w.-]+@[w.-]+', str)
# print(emails)
# print('ecit')
# for email in emails:
#     # do something with each found email string
#     print(email)
# from pathlib import Path
# p = Path('test') / 'req.txt'
# print(p)
from termcolor import colored
print(colored('hello', 'red'), colored('world', 'green'))

from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
