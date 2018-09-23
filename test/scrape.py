# This file will scrape Stake Overflow site for given query

import sys
import os
from bs4 import BeautifulSoup
import requests
from queue import Queue
from subprocess import PIPE, Popen
import webbrowser
import time

SO_URL = "https://stackoverflow.com"

# ASCII color codes
GREEN = '\033[92m'
GRAY = '\033[90m'
CYAN = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'
