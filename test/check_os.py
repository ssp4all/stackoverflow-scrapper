import os

current_os = os.name
print(current_os)
if current_os == 'nt':
    os.system('cls')
if current_os in ['Linux', 'Darwin', 'posix'] or current_os.startswith('CYGWIN'):
    os.system('clear')
