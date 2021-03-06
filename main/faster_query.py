from animals import print_animal
from funtions import *
from termcolor import colored

def faster_query(query):
    """Print code part for faster response."""
    
    output, error = run(["howdoi", query])
    if output is None:
        print(colored('No result found', 'red', attrs='reverse'))
    else:
        print_animal()
        clear_terminal()
        print(colored('OUTPUT:', 'white', attrs=['reverse', 'bold']))
        print(colored(toString(output), 'yellow'))
