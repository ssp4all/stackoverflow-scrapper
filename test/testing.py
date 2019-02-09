# i = 1
# print(str(i).join(''), end='')
# # print(' ', end='')
# print('hello'.capitalize(),end='')


import webbrowser
print('Enter b to open a link')
if input() in ['b', 'B']:
    url = 'fb.com'
    webbrowser.open(url)