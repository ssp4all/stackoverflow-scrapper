# This file will scrape Stake Overflow site for given query

import os
import sys
import time
from subprocess import PIPE, Popen
import webbrowser
import keyboard
import requests
from bs4 import BeautifulSoup

from terminal import get_terminal_size

########################################
# Logic to scrape
########################################

def get_search_results(query):
    """Returns a list of dictionaries containing each search result."""
    while True:
        #   
        # Get current terminal width
        #
        sizex, sizey = get_terminal_size()
        #
        # Scraping
        #
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
            print('-'*sizex)   #find current teminal width
            print(i, end='  ')
            # print('  ', end='')
            print(title.strip())
            print('-'*sizex)
            print("ANS-COUNT : ", sep=" ", end="")
            print(answer_count, sep=' ', end='  ')
            print(ans_status)
            print("LINK: " + (URL + title_link))
            i += 1

            search_results.append(URL + title_link)

        # Get post number
        print()
        try:
            choice = input("Enter post no or 'q' to EXIT: ")
            if choice in ['q', 'Q']:
                print('Exiting...')
                exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            exit(1)
        except ValueError:
            print('Invalid Input')
        except EOFError:
            print('Exiting...')
            exit(0)
        
        # if choice <= 1 and choice >= i:
        #     print('Invalid Input...Exiting....')
        #     break
        # Scrape particular post
        try:
            post_no = search_results[int(choice)-1]
        except IndexError:
            print('Invalid Input')
            continue
        except ValueError:
            print('Enter interger only!')
            continue
            
        new_url = post_no
        new_response = requests.get(new_url)
        new_soup = BeautifulSoup(new_response.text, 'html.parser')

        new_title = new_soup.find(class_='grid--cell fs-headline1 fl1 ow-break-word').get_text().replace('\n', '')
        print()

        print('#'*sizex)
        print(new_title)
        print('#'*sizex, end="\n\n")

        # post_bodies = new_soup.find_all(class_ = 'post-text')
        post_body = new_soup.find(class_='answer')
        # print(post_body)    
        try:
            pbody = post_body.find_all(['p','code'])  # find all p
            for p in pbody:
                print(p.get_text().strip())
                print()
        except AttributeError:
            print('This Question has NO solution, Try again!')
            time.sleep(3)
            continue

        pvote = post_body.find(
            class_='js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center').get_text()
        print()
        print('*'*sizex, end='')
        print("*    VOTES : ", end='')
        print(pvote+"   *")

        print('*'*sizex)
        print('1. EXIT (q)')
        print('2. Open in Browser (b)')
        print('3. Continue (y)')
        ch = input()

        if ch in ['q', 'Q', 'n']:
            print('\nExiting....')
            exit(0)
        elif ch in ['b', 'B']:
            webbrowser.open(new_url)
            continue
        else:
            if os.name != 'nt':
                os.system("clear")
            else:
                os.system("cls")
