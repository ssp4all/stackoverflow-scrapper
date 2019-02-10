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
from pathlib import Path
p = Path('test') / 'req.txt'
print(p)
