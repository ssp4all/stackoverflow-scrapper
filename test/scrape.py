# This file will scrape Stake Overflow site for given query

import sys
import os
from bs4 import BeautifulSoup
import requests
from subprocess import PIPE, Popen
import time


########################################
# Scrape this URL
########################################
SO_URL = "https://stackoverflow.com/search?q=array+comprehension"


########################################
# Logic to scrape
########################################
def get_search_results(soup):
    """Returns a list of dictionaries containing each search result."""
    search_results = []
    posts = soup.find_all(class_="question-summary search-result")
    for result in posts:
        title = result.find(class_="result-link").get_text().replace('\n', '')
        title_link = result.find(class_="result-link").find('a')['href']

        if (result.find(class_="status answered")) != None:  # Has answers
            answer_count = int(result.find(
                class_="status answered").find("strong").get_text())
        # Has an accepted answer (closed)
        elif result.find(class_="status answered-accepted") != None:
            answer_count = int(result.find(
                class_="status answered-accepted").find("strong").get_text())
        else:  # No answers
            answer_count = 0

        # answer_count = 0
        search_results.append({
            "Title": title,
            "Answers": answer_count,
            "URL": SO_URL + title_link
        })

    print(search_results)

########################################
# Main
########################################

def main():
    response = requests.get(SO_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    get_search_results(soup)


if __name__ == "__main__":
    main()
