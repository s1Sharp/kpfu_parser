from bs4 import BeautifulSoup

import tools


def gather_name_link_of_institutes_and_branches(html):
    soup = BeautifulSoup(html, 'lxml')

    ul = soup.find_all('ul', class_='menu_list')[:2]
    lis = ul[0].find_all('li', class_='li_spec')
    lis += ul[1].find_all('li', class_='li_spec')

    institutes = [(li.find('a').text, li.find('a').get('href')) for li in lis]

    return institutes


def get_link_from_menu_list_left(link, button_name: str):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    ul = soup.find('ul', class_='menu_list_left')
    lis = ul.find_all('li')

    for li in lis:
        a = li.find('a')
        if a.text == button_name:
            return a.get('href')


def gather_name_link_of_cathedras_of_ivmiit(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')
    uls = div.find_all('ul')

    lis = []
    for ul in uls:
        lis += ul.find_all('li', class_='li_spec')

    cathedras = []
    for li in lis:
        a = li.find('a')
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
    return cathedras


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


def parse_ivmiit(link):
    about_button_link = get_link_from_menu_list_left(link, 'Об институте')

    cathedras = gather_name_link_of_cathedras_of_ivmiit(about_button_link)
    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, 'Сотрудники')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees(stuff_link)

    return result


def gather_name_link_of_cathedras_of_geogr(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')

    links = div.find_all('a')

    cathedras = []
    for a in links:
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
    return cathedras


def parse_geogr(link):
    struct_button_link = get_link_from_menu_list_left(link, 'Структура')

    cathedras = gather_name_link_of_cathedras_of_geogr(struct_button_link)
    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, 'Состав')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees(stuff_link)

    return result


def parse_physical(link):
    struct_button_link = get_link_from_menu_list_left(link, 'Структура')

    stuff_link = get_link_from_menu_list_left(struct_button_link, 'Сотрудники')

    result = {'Основная кафедра': gather_name_link_of_employees(stuff_link)}

    return result
