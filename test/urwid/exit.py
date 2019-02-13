import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'yellow'),
    ('streak2', 'black', 'yellow'),
    ('bg', 'black', 'white') ]

txt = urwid.Text(('banner', u" Hello World "), align='right')
map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1)

txt2 = urwid.Text(('banner', u" Hello World "), align='left')
map3 = urwid.AttrMap(txt2, 'streak2')
fill2 = urwid.Filler(map3)


map2 = urwid.AttrMap(fill, 'bg')
loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)

map4 = urwid.AttrMap(fill2, 'bg')
loop = urwid.MainLoop(map4, palette, unhandled_input=exit_on_q)

loop.run()
