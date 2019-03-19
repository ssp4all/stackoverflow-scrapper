import urwid

# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# Scrollbar positions
SCROLLBAR_LEFT = "left"
SCROLLBAR_RIGHT = "right"

class ScrollBar(urwid.WidgetDecoration):
    # TODO: Change scrollbar size and color(?)

    def sizing(self):
        return frozenset((BOX,))

    def selectable(self):
        return True

    def __init__(self, widget, thumb_char=u'\u2588', trough_char=' ',
                 side=SCROLLBAR_RIGHT, width=1):
        """Box widget that adds a scrollbar to `widget`."""
        self.__super.__init__(widget)
        self._thumb_char = thumb_char
        self._trough_char = trough_char
        self.scrollbar_side = side
        self.scrollbar_width = max(1, width)
        self._original_widget_size = (0, 0)
        self._dragging = False

    def render(self, size, focus=False):
        maxcol, maxrow = size

        ow = self._original_widget
        ow_base = self.scrolling_base_widget
        ow_rows_max = ow_base.rows_max(size, focus)
        if ow_rows_max <= maxrow:  # Canvas fits without scrolling - no scrollbar needed
            self._original_widget_size = size
            return ow.render(size, focus)

        sb_width = self._scrollbar_width
        self._original_widget_size = ow_size = (maxcol-sb_width, maxrow)
        ow_canv = ow.render(ow_size, focus)

        pos = ow_base.get_scrollpos(ow_size, focus)
        posmax = ow_rows_max - maxrow

        # Thumb shrinks/grows according to the ratio of
        # <number of visible lines> / <number of total lines>
        thumb_weight = min(1, maxrow / max(1, ow_rows_max))
        thumb_height = max(1, round(thumb_weight * maxrow))

        # Thumb may only touch top/bottom if the first/last row is visible
        top_weight = float(pos) / max(1, posmax)
        top_height = int((maxrow-thumb_height) * top_weight)
        if top_height == 0 and top_weight > 0:
            top_height = 1

        # Bottom part is remaining space
        bottom_height = maxrow - thumb_height - top_height
        assert thumb_height + top_height + bottom_height == maxrow

        # Create scrollbar canvas
        top = urwid.SolidCanvas(self._trough_char, sb_width, top_height)
        thumb = urwid.SolidCanvas(self._thumb_char, sb_width, thumb_height)
        bottom = urwid.SolidCanvas(self._trough_char, sb_width, bottom_height)
        sb_canv = urwid.CanvasCombine([
            (top, None, False),
            (thumb, None, False),
            (bottom, None, False),
        ])

        combinelist = [(ow_canv, None, True, ow_size[0]),
                       (sb_canv, None, False, sb_width)]
        if self._scrollbar_side != SCROLLBAR_LEFT:
            return urwid.CanvasJoin(combinelist)
        else:
            return urwid.CanvasJoin(reversed(combinelist))

    @property
    def scrollbar_width(self):
        return max(1, self._scrollbar_width)

    @scrollbar_width.setter
    def scrollbar_width(self, width):
        self._scrollbar_width = max(1, int(width))
        self._invalidate()

    @property
    def scrollbar_side(self):
        return self._scrollbar_side

    @scrollbar_side.setter
    def scrollbar_side(self, side):
        if side not in (SCROLLBAR_LEFT, SCROLLBAR_RIGHT):
            raise ValueError(
                "scrollbar_side must be 'left' or 'right', not %r" % side)
        self._scrollbar_side = side
        self._invalidate()

    @property
    def scrolling_base_widget(self):
        """Nearest `base_widget` that is compatible with the scrolling API."""
        def orig_iter(w):
            while hasattr(w, "original_widget"):
                w = w.original_widget
                yield w
            yield w

        def is_scrolling_widget(w):
            return hasattr(w, "get_scrollpos") and hasattr(w, "rows_max")

        for w in orig_iter(self):
            if is_scrolling_widget(w):
                return w

    @property
    def scrollbar_column(self):
        if self.scrollbar_side == SCROLLBAR_LEFT:
            return 0
        if self.scrollbar_side == SCROLLBAR_RIGHT:
            return self._original_widget_size[0]

    def keypress(self, size, key):
        return self._original_widget.keypress(self._original_widget_size, key)

    def mouse_event(self, size, event, button, col, row, focus):
        ow = self._original_widget
        ow_size = self._original_widget_size
        handled = False
        if hasattr(ow, "mouse_event"):
            handled = ow.mouse_event(ow_size, event, button, col, row, focus)

        if not handled and hasattr(ow, "set_scrollpos"):
            if button == 4:  # Scroll wheel up
                pos = ow.get_scrollpos(ow_size)
                if pos > 0:
                    ow.set_scrollpos(pos - 1)
                    return True
            elif button == 5:  # Scroll wheel down
                pos = ow.get_scrollpos(ow_size)
                ow.set_scrollpos(pos + 1)
                return True
            elif col == self.scrollbar_column:
                ow.set_scrollpos(int(row*ow.scroll_ratio))
                if event == "mouse press":
                    self._dragging = True
                elif event == "mouse release":
                    self._dragging = False
            elif self._dragging:
                ow.set_scrollpos(int(row*ow.scroll_ratio))
                if event == "mouse release":
                    self._dragging = False

        return False






