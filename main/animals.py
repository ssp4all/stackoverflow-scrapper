from cowsay import *
from random import randint
from functools import partial
from termcolor import colored
from spinner import spinner

def print_animal():
    """Print random animal with a msg"""
    t = partial(tux, colored("hold tight...", 'magenta')) 
    m = partial(milk, colored(
        "hold tight...", 'magenta'))
    b = partial(beavis, colored(
        "hold tight...", 'red'))
    c = partial(cheese, colored(
        "hold tight...", 'yellow'))
    d = partial(daemon, colored(
        "hold tight...", 'blue'))
    co = partial(cow, colored(
        "hold tight...", 'cyan'))
    k = partial(kitty, colored(
        "hold tight...", 'white'))

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
