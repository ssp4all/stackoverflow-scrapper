from cowsay import *
from random import randint
from functools import partial
from termcolor import colored
from spinner import spinner

def print_animal():
    """Print random animal with a msg"""
    t = partial(tux, colored("hold tight...", 'magenta')) 
    m = partial(milk, colored(
        "hold tight...", 'magenta', 'on_white', attrs=['reverse']))
    b = partial(beavis, colored(
        "hold tight...", 'red', 'on_white', attrs=['reverse']))
    c = partial(cheese, colored(
        "hold tight...", 'yellow', 'on_white', attrs=['reverse']))
    d = partial(daemon, colored(
        "hold tight...", 'blue', 'on_white', attrs=['reverse']))
    co = partial(cow, colored(
        "hold tight...", 'cyan', 'on_white', attrs=['reverse']))
    k = partial(kitty, colored(
        "hold tight...", 'white', 'on_white', attrs=['reverse']))

    animals = ['t', 'm', 'b', 'd', 'co', 'k']
    r = randint(0, len(animals)-1)
    x = animals[r]

    if x == 't':    t()
    if x == 'm':    m()
    if x == 'b':    b()
    if x == 'c':    c()
    if x == 'd':    d()
    if x == 'co':   co()
    if x == 'k':    k()
    spinner()
# print_animal()
