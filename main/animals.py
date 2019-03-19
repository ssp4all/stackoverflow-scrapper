from cowsay import *
from random import randint
from functools import partial
# animals = [
#     beavis('Hold tight'),
#     cheese('Hold tight'), daemon('Hold tight'), cow('Hold tight'),
#     ghostbusters('Hold tight'), kitty(
#         'Hold tight'), meow('Hold tight'),
#     milk('Hold tight'), stegosaurus('Hold tight'), stimpy(
#         'Hold tight'), tux('Hold tight')]


# anim = ["beavis", lambda: milk('gfgfd')]

def print_animal():
    """Print random animal with a msg"""
    t = partial(tux, "hold tight") 
    m = partial(milk, "hold tight")
    b = partial(beavis, "hold tight")
    c = partial(cheese, "hold tight")
    d = partial(daemon, "hold tight")
    co = partial(cow, "hold tight")
    k = partial(kitty, "hold tight")

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

# print_animal()
