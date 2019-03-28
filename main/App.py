import urwid
import webbrowser
from scrape import *
from ScrollBar import *
from urwid.widget import BOX, FIXED, FLOW

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


class App(object):
    def __init__(self, search_results):
        self.search_results, self.viewing_answers = search_results, False
        self.palette = [
            ("title", "light cyan,bold", "default", "standout"),
            ("stats", "light green", "default", "standout"),
            ("menu", "black", "light cyan", "standout"),
            ("reveal focus", "black", "light cyan", "standout"),
            ("no answers", "light red", "default", "standout"),
            ("code", "brown", "default", "standout")
        ]
        self.menu = urwid.Text([
            u'\n',
            ("menu", u" ENTER "), ("light gray", u" View answers "),
            ("menu", u" B "), ("light gray", u" Open browser "),
            ("menu", u" Q "), ("light gray", u" Quit"),
        ])

        results = list(map(lambda result: urwid.AttrMap(SelectableText(self._stylize_title(
            result)), None, "reveal focus"), self.search_results))  # TODO: Add a wrap='clip' attribute
        content = urwid.SimpleListWalker(results)
        self.content_container = urwid.ListBox(content)
        layout = urwid.Frame(body=self.content_container, footer=self.menu)

        self.main_loop = urwid.MainLoop(
            layout, self.palette, unhandled_input=self._handle_input)
        self.original_widget = self.main_loop.widget

        self.main_loop.run()

    def _handle_input(self, input):
        if input == "enter":  # View answers
            url = self._get_selected_link()

            if url != None:
                self.viewing_answers = True
                question_title, question_desc, question_stats, answers = get_question_and_answers(
                    url)

                pile = urwid.Pile(self._stylize_question(question_title, question_desc, question_stats) + [urwid.Divider('*')] +
                                  interleave(answers, [urwid.Divider('-')] * (len(answers) - 1)))
                padding = ScrollBar(Scrollable(
                    urwid.Padding(pile, left=2, right=2)))
                #filler = urwid.Filler(padding, valign="top")
                linebox = urwid.LineBox(padding)

                menu = urwid.Text([
                    u'\n',
                    ("menu", u" ESC "), ("light gray", u" Go back "),
                    ("menu", u" B "), ("light gray", u" Open browser "),
                    ("menu", u" Q "), ("light gray", u" Quit"),
                ])

                self.main_loop.widget = urwid.Frame(body=urwid.Overlay(
                    linebox, self.content_container, "center", ("relative", 60), "middle", 23), footer=menu)
        elif input in ('b', 'B'):  # Open link
            url = self._get_selected_link()

            if url != None:
                webbrowser.open(url)
        elif input == "esc":  # Close window
            if self.viewing_answers:
                self.main_loop.widget = self.original_widget
                self.viewing_answers = False
            else:
                raise urwid.ExitMainLoop()
        elif input in ('q', 'Q'):  # Quit
            raise urwid.ExitMainLoop()

    def _get_selected_link(self):
        focus_widget, idx = self.content_container.get_focus()  # Gets selected item
        title = focus_widget.base_widget.text

        for result in self.search_results:
            # Found selected title's search_result dict
            if title == self._stylize_title(result):
                return result["URL"]

    def _stylize_title(self, search_result):
        if search_result["Answers"] == 1:
            return "%s (1 Answer)" % search_result["Title"]
        else:
            return "%s (%s Answers)" % (search_result["Title"], search_result["Answers"])

    def _stylize_question(self, title, desc, stats):
        new_title = urwid.Text(("title", u"%s" % title))
        new_stats = urwid.Text(("stats", u"%s\n" % stats))

        return [new_title, desc, new_stats]
