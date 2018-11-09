# This file will scrape Stake Overflow site for given query

import sys
import os
from bs4 import BeautifulSoup
import requests
from subprocess import PIPE, Popen
import time




########################################
# Logic to scrape
########################################

def get_search_results(query):
    """Returns a list of dictionaries containing each search result."""

    URL = 'https://stackoverflow.com'       # Scrape this URL
    SO_URL = "https://stackoverflow.com/search?q="

    response = requests.get(SO_URL+query)
    soup = BeautifulSoup(response.text, 'html.parser')

    search_results = []
    posts = soup.find_all(class_="question-summary search-result")
    i = 1
    for result in posts:
        title = result.find(class_="result-link").get_text().replace('\n', '')
        title_link = result.find(class_="result-link").find('a')['href']

        ans_status = ''
        if (result.find(class_="status answered")) != None:  # Has answers
            answer_count = int(result.find(
                class_="status answered").find("strong").get_text())
            ans_status = 'NOT ACCEPTED'
        # Has an accepted answer (closed)
        elif result.find(class_="status answered-accepted") != None:
            answer_count = int(result.find(
                class_="status answered-accepted").find("strong").get_text())
            ans_status = 'ACCEPTED'
        else:  # No answers
            answer_count = 0

        # Print content
        print()
        print(i)
        print(title)
        print("ANS-COUNT : ",sep = " ",end = "")
        print(answer_count, sep = ' ', end = '  ')
        print(ans_status)
        print("LINK: "+ (URL + title_link))
        i += 1

        # search_results.append({
        #     "Title": title,
        #     "Answers": answer_count,
        #     "URL": URL + title_link
        # })

        search_results.append(URL + title_link)
        
    #Get post number 
    print()
    print('Enter a Number :')
    no = int(input())
    post_no = search_results[no-1]

    # Scrape particular post
    new_url = post_no
    new_response = requests.get(new_url)
    new_soup = BeautifulSoup(new_response.text, 'html.parser')

    new_title = new_soup.find(
        'h1', {'class': 'grid--cell fs-headline1 fl1'}).get_text().replace('\n', '')

    post_body = new_soup.find(class_='post-text').get_text()

    print()
    print(new_title)
    print(post_body)
