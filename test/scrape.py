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
    while True:
        URL = 'https://stackoverflow.com'       # Scrape this URL
        SO_URL = "https://stackoverflow.com/search?q="

        response = requests.get(SO_URL+query)
        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = []
        posts = soup.find_all(class_="question-summary search-result")
        i = 1
        for result in posts:
            title = result.find(
                class_="result-link").get_text().replace('\n', '')
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
            print('-'*60)
            print(i)
            print(title)
            print("ANS-COUNT : ", sep=" ", end="")
            print(answer_count, sep=' ', end='  ')
            print(ans_status)
            print("LINK: " + (URL + title_link))
            i += 1

            # search_results.append({
            #     "Title": title,
            #     "Answers": answer_count,
            #     "URL": URL + title_link
            # })

            search_results.append(URL + title_link)

        # Get post number
        print()
        try:
            choice = int(input("Enter your choice: "))
        except KeyboardInterrupt:
            print("Exiting...")
            exit(1)
        
        if choice <= 1 and choice >= i:
            print('Invalid Input...Exiting....')
            break


        # Scrape particular post
        try:
            post_no = search_results[choice-1]
        except IndexError:
            print('Invalid Input')
            continue
            
        new_url = post_no
        new_response = requests.get(new_url)
        new_soup = BeautifulSoup(new_response.text, 'html.parser')

        new_title = new_soup.find(
            'h1', {'class': 'grid--cell fs-headline1 fl1'}).get_text().replace('\n', '')
        print()

        print('#'*50)
        print(new_title)
        print('#'*50, end="\n\n")

        # post_bodies = new_soup.find_all(class_ = 'post-text')
        post_body = new_soup.find(class_='answer')

        # print(post_body)
        pbody = post_body.find_all('p')  # find all p
        for p in pbody:
            print(p.get_text())
            print()
        # print(pbody)

        pcode = post_body.find_all('code')  # find all code
        for c in pcode:
            print(c.get_text())
            print()
        # print(pcode)

        pvote = post_body.find(class_="vote").find('span').get_text()
        print()
        print('*'*18)
        print("*    VOTES : ", end='')
        print(pvote+"   *")

        print('*'*18)

        ch = input('Do you want to EXIT y/n :')
        if ch == 'y':
            print('\nExiting....')
            exit(1)
        else:
            if os.name != 'nt':
                os.system("clear")
            else:
                os.system("cls")


