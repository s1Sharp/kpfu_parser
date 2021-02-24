import os
import random
import time

import requests
from selenium import webdriver

import constants
from proxy import PROXY

A_BORDER_SEC = 10
B_BORDER_SEC = 100


def get_random_header():
    return random.choice(constants.headers)


def get_html(url):
    try:
        response = requests.get(url, headers={'https': get_random_header()})
        return response.text
    except:
        print(f'{url} did not respond...')
        return None


def get_html_with_engine(url):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('general.useragent.override', get_random_header())
    driver = webdriver.Firefox(profile, executable_path=constants.gecko_path)
    try:
        driver.get(url)
        html = driver.page_source
    except:
        print(f'{url} did not respond...')
        return None
    driver.quit()
    return html


def get_html_confidently(url):
    while True:
        try:
            response = requests.get(url, headers=get_random_header(), proxies=PROXY.get_next_proxy())
            return response.text
        except:
            print(f'{url} did not respond...')
        time.sleep(random.uniform(A_BORDER_SEC, B_BORDER_SEC))


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_progress(a, b):
    print(f'{a} of {b}')
