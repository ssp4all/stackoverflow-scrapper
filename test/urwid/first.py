from urwid import *

txt = Text(u"Hola")
fill = Filler(txt, "top")
loop = MainLoop(fill)
loop.run()
