from bs4 import BeautifulSoup

import tools


def get_info_from_html(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')
    p = div.find_all('p')

    result = []
    for current in p:
        result.append(current.text)
    return result


def gather_name_link_of_employees(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    iframe = soup.find('iframe')
    outer_src = iframe.get('src')

    html = tools.get_html(outer_src)
    soup = BeautifulSoup(html, 'lxml')

    spans = soup.find_all('span', class_='fio')

    employees = []
    for span in spans:
        a = span.find('a')
        if a:
            employees.append((a.text, a.get('href')))

    return employees


def get_link_from_menu_list_left(link, button_name: str):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    ul = soup.find('ul', class_='menu_list_left')
    lis = ul.find_all('li')

    for li in lis:
        a = li.find('a')
        if a.text == button_name:
            return a.get('href')


def get_links_from_menu_list_left(link, button_name: str):
    # get many links, not once
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    ul = soup.find('ul', class_='menu_list_left')
    lis = ul.find_all('li')

    links_res = []
    for li in lis:
        a = li.find('a')
        if a.text.startswith == button_name:
            links_res.append(a.get('href'))
    return links_res


def gather_name_link_of_cathedras_of_ipot(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')

    links = div.find_all('a')

    cathedras = []
    for a in links:
        if a.text.startswith('Центр'):
            cathedras.append((a.text, a.get('href')))
    return cathedras


def clear_parsing_info(res):  # clear from any symbols
    bad_chars = [';', ':', '!', "*", ".", "\\", "/", "-", "\t", "\r", "\n", "\ufeff", "\xa0"]
    ans = []

    for current in res:
        for char in bad_chars:
            current = current.replace(char, "")
        if current != "":
            ans.append(current)
    return ans


def parse_ipot(link):  # main parse func
    struct_links = gather_name_link_of_cathedras_of_ipot(link)

    result = {}

    for name, link in struct_links:
        stuff_link = get_link_from_menu_list_left(link, 'Сотрудники')
        if stuff_link != None:
            result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = get_info_from_html(stuff_link)
    for name, info in result.items():
        result[name] = clear_parsing_info(info)

    return result
