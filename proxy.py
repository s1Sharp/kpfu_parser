import requests
import bs4

import constants


def get_html(url):
    response = requests.get(url)
    return response.text


def get_proxies(url=constants.url_proxy):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')

    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')

    proxies = []
    for tr in trs:
        tds = tr.find_all('td')
        if tds[6].text.strip() == 'yes':
            proxies.append(tds[0].text.strip() + ':' + tds[1].text.strip())
    return proxies


class Proxy:
    def __init__(self):
        self.proxies = []
        self.cur = 0
        self.size = 0
        self.refresh_proxies()

    def get_next_proxy(self):
        if self.cur == self.size:
            self.refresh_proxies()
        proxy = {'https': 'https://' + self.proxies[self.cur]}
        self.cur += 1
        return proxy

    def refresh_proxies(self):
        self.cur = 0
        self.proxies = get_proxies()
        self.size = len(self.proxies)

# PROXY = Proxy()
