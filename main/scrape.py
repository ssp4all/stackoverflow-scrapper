# This file will scrape Stake Overflow site for given query

import os
import sys
import re
import time
import webbrowser
import requests
import random
from bs4 import BeautifulSoup
from termcolor import colored
from terminal import get_terminal_size
from user_agents import user_agents

sizex, sizey = get_terminal_size()  # Get current terminal width
URL = 'https://stackoverflow.com'   # Scrape this URL
SO_URL = "https://stackoverflow.com/search?q="


########################################
# Logic to scrape
########################################
def clear_terminal():
    """Clear terminal """
    if os.name != 'nt':
        os.system("clear")
    else:
        os.system("cls")    

def url_to_soup(url):
    """Convert URL to soup object"""
    
    try:
        html = requests.get(
            url, headers={"User-Agent": random.choice(user_agents())})
    except requests.exceptions.RequestException:
        print(colored("Unable to fetch results...\nPlease check your Internet!",'red'))
        sys.exit(1)

    if re.search("\.com/nocaptcha", html.url):  # URL is a captcha page
        return None
    else:
        return BeautifulSoup(html.text, "html.parser")

def search_stackoverflow(query):
    """Generate URL then convert it to soup"""
    
    # soup = url_to_soup(SO_URL + "/search?pagesize=50&q=%s" %
    #               query.replace(' ', '+'))

    soup = url_to_soup(SO_URL + query.replace(' ', '+'))
    if soup is None:
        return (None, True)
    else:
        return (soup, False)

def get_search_results(soup):
    """Returns a list containing each search result."""
    
    while True:
    
        if soup is None:
            print(colored('Unable to fetch data bcoz of CAPTCHA','red'))
            time.sleep(2)
            clear_terminal()
            exit(1)
        
        search_results = []
        try:
            posts = soup.find_all(class_="question-summary search-result")
        except AttributeError:
            print(colored('No results found', 'red'))
            time.sleep(2)
            clear_terminal()
            sys.exit(1)

        if posts is None:
            print(colored('No results found','red'))
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
            # print(URL + title_link)
            i += 1
            search_results.append(URL + title_link)

        # Get post number
        print()
        try:
            choice = input("Enter post no or 'q' to EXIT: ")
            if choice in ['q', 'Q']:
                print('Exiting...')
                time.sleep(2)
                clear_terminal()
                exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            clear_terminal()
            exit(1)
        except ValueError:
            print('Invalid Input')
        except EOFError:
            print('Exiting...')
            clear_terminal()
            exit(1)
        
        # Scrape particular post
        try:
            post_no = search_results[int(choice)-1]
        except IndexError:
            print('Invalid Input')
            time.sleep(2)
            continue
        except ValueError:
            print('Enter interger only!')
            time.sleep(2)
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
        # post_body = new_soup.find(class_='post-text')

        try:
            pbody = post_body.find_all(['p','code'])  # find all p
            
            for p in pbody:
                print(p.get_text().strip())
                print()
        except AttributeError:
            print('This Question has NO solution, Try again!')
            time.sleep(2)
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
            clear_terminal()
            exit(0)
        elif ch in ['b', 'B']:
            webbrowser.open(new_url)
            continue
        else:
            clear_terminal()
