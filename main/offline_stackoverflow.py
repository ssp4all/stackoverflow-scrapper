import string
import sys

import html2text
import nltk
import urwid
from termcolor import colored

from animals import print_animal
from ScrollBar import *
from spinner import spinner

question_to_id, id_to_question, ans_id_mapping = {}, {}, {}
TfIdVector, tfidf_values, sentence_tokens, search_results = [], [], [], []
default_answer = "No answer found :("


def offline_search(query):
    """If internet is not there... """
    print_animal()
    read_data()
    matches = get_answers(query)
    group_answers(matches)

def read_data():
    """Read csv files to generate information """
    global sentence_tokens, question_to_id, id_to_question, ans_id_mapping, sentence_tokens
    global TfIdVector, tfidf_values
    
    import pickle

    spinner()
    try:
        question_to_id, id_to_question = pickle.load(
            open(sys.path[0]+'/data/question_data.pickle', 'rb'))
        ans_id_mapping, sentence_tokens = pickle.load(
            open(sys.path[0]+'/data/answer_data.pickle', 'rb'))
        TfIdVector, tfidf_values = pickle.load(
            open(sys.path[0]+'/data/model.pickle', 'rb'))
    except FileNotFoundError:
        print(colored('File not found!', 'red', 'on_white', attrs=['reverse']))
    
    for question_id in id_to_question.keys():
        if question_id not in ans_id_mapping:
            continue
        for i, answer1 in enumerate(ans_id_mapping[question_id]):
            for j, answer2 in enumerate(ans_id_mapping[question_id]):
                if answer1['score'] < answer2['score']:
                    temp = ans_id_mapping[question_id][i]
                    ans_id_mapping[question_id][i] = ans_id_mapping[question_id][j]
                    ans_id_mapping[question_id][j] = temp

def get_answers(query):
    """ Compile answer from data """
    global question_to_id, ans_id_mapping
    # print(query)
    questions = compute_similarity(query)
    if questions == default_answer:
        return default_answer

    ids = list(map(lambda qn: question_to_id[qn[:-1]], questions))
    # print(ids)
    results = {}
    for question_id in ids:
        try:
            results[question_id] = ans_id_mapping[question_id]
        except:
            pass

    return results


def details(question_id):
    """answer details for a given question """
    answers = []
    for i, answer in enumerate(ans_id_mapping[question_id]):
        answers.append(html2text.html2text(answer['body']))
    if len(answers) == 0:
        answers.append(urwid.Text(
            ("no answers", u"\nNo answers for this question.")))
    return answers

def compute_similarity(query):
    """ Finds similarity from values"""
    global sentence_tokens, default_answer
    global TfIdVector, tfidf_values
    from sklearn.metrics.pairwise import cosine_similarity

    tfidf_query = TfIdVector.transform([query])[0]
    similarity_values = cosine_similarity(tfidf_query, tfidf_values)
    flattened = similarity_values.flatten()
    flattened.sort()
    req_tfidf = flattened[-2]

    if req_tfidf == 0:
        return default_answer
    else:
        indexes = similarity_values.argsort()[0][::-1][:10]
    return list(map(lambda idx: sentence_tokens[idx], indexes))

def group_answers(matches):
    """ Returns a dictionary of question data"""
    global id_to_question, search_results
    
    for question_id in matches.keys():
        question = id_to_question[question_id]

        if question_id not in ans_id_mapping:
            continue
        search_results.append({
            'q_id': question_id,
            'title': question['title'],
            'author': question['author'],
            'answers': 1,
            'q_desc': html2text.html2text(question['body'])
        })
    App(search_results)


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
        global search_results
        if input == "enter":  # View answers
            q_id = self._get_selected_id()

            if q_id != None:
                self.viewing_answers = True
                answers = details(q_id)
                op = [i['q_desc'] for i in search_results if i['q_id'] == q_id]
                q_desc = op[0]
                pile = urwid.Pile(self._stylize_question(q_desc) + [urwid.Divider('*')]
                                  + self._stylize_answers(answers))
                # pile = urwid.Pile(self._stylize_question(q_desc) + [urwid.Divider('*')]
                #                   + self.interleave2(answers))

                padding = ScrollBar(Scrollable(
                    urwid.Padding(pile, left=2, right=2)))
                #filler = urwid.Filler(padding, valign="top")
                linebox = urwid.LineBox(padding)

                menu = urwid.Text([
                    u'\n',
                    ("menu", u" ESC "), ("light gray", u" Go back "),
                    ("menu", u" Q "), ("light gray", u" Quit"),
                ])

                self.main_loop.widget = urwid.Frame(body=urwid.Overlay(
                    linebox, self.content_container, "center", ("relative", 60), "middle", 23), footer=menu)

        elif input == "esc":  # Close window
            if self.viewing_answers:
                self.main_loop.widget = self.original_widget
                self.viewing_answers = False
            else:
                raise urwid.ExitMainLoop()
        elif input in ('q', 'Q'):  # Quit
            raise urwid.ExitMainLoop()

    def _get_selected_id(self):
        focus_widget, idx = self.content_container.get_focus()  # Gets selected item
        title = focus_widget.base_widget.text

        for result in self.search_results:
            # Found selected title's search_result dict
            if title == self._stylize_title(result):
                return result["q_id"]

    def _stylize_title(self, search_result):
        if search_result["answers"] == 1:
            return "%s (1 Answer)" % search_result["title"]
        else:
            return "%s (%s answers)" % (search_result["title"], search_result["answers"])

    def _stylize_question(self, question):
        new_question = urwid.Text(("Question", u"%s" % question))
        return [new_question]

    def _stylize_answers(self, answer):
        new_ans = urwid.Text(("Answer", u"%s" % answer[0]))
        return [new_ans]

# if __name__ == "__main__":
#     offline_search("Typerror: str not int")