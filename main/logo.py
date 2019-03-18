import sys

from colorama import init
from termcolor import cprint

from pyfiglet import figlet_format
def logo():
       """Draw logo on terminal """
       init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

       cprint(figlet_format('      Intelligent      Codemate      ', font='standard'),
              'white', 'on_blue', attrs=['bold'])
