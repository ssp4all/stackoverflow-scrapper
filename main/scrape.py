# This file will scrape Stack Overflow site for a given query

import os
import random
import re
import sys
import time
import webbrowser

import requests
import urwid
from bs4 import BeautifulSoup
from termcolor import colored

from funtions import clear_terminal
from user_agents import user_agents
from offline_stackoverflow import offline_search
URL = 'https://stackoverflow.com'   # Scrape this URL

########################################
# Logic to scrape
########################################


def url_to_soup(url, query):
    """Convert URL to soup object"""
    # print(url)
    try:
        html = requests.get(
            url, headers={"User-Agent": random.choice(user_agents())})
    except requests.exceptions.RequestException:
        print(colored("\nPlease check your Internet!",
                      'red', 'on_white', attrs=['reverse']))
        # print(str(query))
        offline_search(str(query))
        # if query.find('TypeError') != -1:
        #     offline_search("python3 TypeError")
        # elif query.find('IndexError') != -1:
        #     offline_search("python3 IndexError")
        # else:
        #     print(colored("\nUnknown Error!",
        #               'red', 'on_white', attrs=['reverse']))
            
        clear_terminal()
        sys.exit(0)

    if re.search("\.com/nocaptcha", html.url):  # URL is a captcha page
        return None
    else:
        return BeautifulSoup(html.text, "html.parser")


def search_stackoverflow(query):
    """Generate URL then convert it to soup"""
    url = URL + "/search?pagesize=10&q=%s" % query.replace(' ', '+')
    # print(url)
    soup = url_to_soup(url, query)
    # soup = url_to_soup(SO_URL + query.replace(' ', '+'))
    if soup is None:
        return (None, True)
    else:
        return (soup, False)


def get_search_results(soup):
    """Returns a list of dictionaries containing each search result."""
    search_results = []

    for result in soup.find_all("div", class_="question-summary search-result"):
        title_container = result.find_all(
            "div", class_="result-link")[0].find_all("a")[0]
        # print(result)

        if result.find_all("div", class_="status answered") != []:  # Has answers
            answer_count = int(result.find_all("div", class_="status answered")[
                               0].find_all("strong")[0].text)
        # Has an accepted answer (closed)
        elif result.find_all("div", class_="status answered-accepted") != []:
            answer_count = int(result.find_all(
                "div", class_="status answered-accepted")[0].find_all("strong")[0].text)
        else:  # No answers
            answer_count = 0

        search_results.append({
            "Title": title_container["title"],
            "Answers": answer_count,
            "URL": URL + title_container["href"]
        })

    return search_results


def stylize_code(soup):
    """Identifies and stylizes code in a question or answer."""
    # TODO: Handle blockquotes and markdown
    stylized_text = []
    code_blocks = [block.get_text() for block in soup.find_all("code")]
    blockquotes = [block.get_text() for block in soup.find_all("blockquote")]
    newline = False

    for child in soup.recursiveChildGenerator():
        name = getattr(child, "name", None)

        if name is None:  # Leaf (terminal) node
            if child in code_blocks:
                if newline:  # Code block
                    # if code_blocks.index(child) == len(code_blocks) - 1: # Last code block
                        #child = child[:-1]
                    stylized_text.append(("code", u"\n%s" % str(child)))
                    newline = False
                else:  # In-line code
                    stylized_text.append(("code", u"%s" % str(child)))
            else:  # Plaintext
                newline = child.endswith('\n')
                stylized_text.append(u"%s" % str(child))

    if type(stylized_text[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if stylized_text[-2][1].endswith('\n'):
            stylized_text[-2] = ("code", stylized_text[-2][1][:-1])

    return urwid.Text(stylized_text)


def get_question_and_answers(url):
    """Returns details about a given question and list of its answers."""
    soup = url_to_soup(url, "")
    if soup == None:  # Captcha page
        return "Sorry, Stack Overflow blocked our request. Try again in a couple seconds.", "", "", ""
    else:
        question_title = soup.find_all(
            'a', class_="question-hyperlink")[0].get_text()
        question_stats = soup.find(
            "div", class_="js-vote-count").get_text()  # Vote count

        try:
            question_stats = question_stats + " Votes | " + '|'.join((((soup.find_all("div", class_="module question-stats")[0].get_text())
                                                                       .replace('\n', ' ')).replace("     ", " | ")).split('|')[:2])  # Vote count, submission date, view count
        except IndexError:
            question_stats = "Could not load statistics."

        question_desc = stylize_code(soup.find_all(
            "div", class_="post-text")[0])  # TODO: Handle duplicates
        question_stats = ' '.join(question_stats.split())

        answers = [stylize_code(answer) for answer in soup.find_all(
            "div", class_="post-text")][1:]
        if len(answers) == 0:
            answers.append(urwid.Text(
                ("no answers", u"\nNo answers for this question.")))

        return question_title, question_desc, question_stats, answers
