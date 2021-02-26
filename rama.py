from bs4 import BeautifulSoup
from ildar import get_link_from_menu_list_left, gather_name_link_of_employees, gather_name_link_of_cathedras_of_ivmiit
import tools


def get_link_from_menu_list_left_engineer(link, button_name: str):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    ul = soup.find('ul', class_='menu_list_left')
    lis = ul.find_all('li')

    for li in lis:
        a = li.find('a')
        if a.text == button_name:
            return a.get('href')


def gather_name_link_of_cathedras_of_engineer(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='area_width')
    links = div.find_all('a')

    cathedras = []
    for a in links:
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
    return cathedras


def gather_name_link_of_employees_engineer(link):
    html = tools.get_html(link)
    if html is None:
        return
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('table', class_='cke_show_border')
    links = div.find_all('a')
    employees = []
    for a in links:
        if a:
            employees.append((a.text, a.get('href')))

    return employees


def parse_engineer(link):
    struct_button_link = get_link_from_menu_list_left_engineer(link, 'Структура')
    cathedras = gather_name_link_of_cathedras_of_engineer(struct_button_link)

    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left_engineer(link, 'Состав кафедры')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees_engineer(stuff_link)
    return result


def parse_engineer2(link):
    struct_button_link = get_link_from_menu_list_left_engineer(link, 'Структура')
    cathedras = gather_name_link_of_cathedras_of_engineer(struct_button_link)

    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left_engineer(link, 'Сотрудники кафедры')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees(stuff_link)
    return result
