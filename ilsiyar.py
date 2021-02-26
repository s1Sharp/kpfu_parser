from bs4 import BeautifulSoup

import tools
import requests
from ildar import get_link_from_menu_list_left, gather_name_link_of_employees


def gather_name_link_of_cathedras_of_phys(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')

    serach_cat = {}

    links = div.find_all('a')

    cathedras = []
    for a in links:
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
            serach_cat[a.text] = 'Сотрудники'
    return cathedras, serach_cat


def parse_phys(link):
    struct_button_link = get_link_from_menu_list_left(link, 'Структура')

    cathedras, search_cath = gather_name_link_of_cathedras_of_phys(
        struct_button_link)
    result = {}
    search_cath['Кафедра теоретической физики'] = 'Коллектив кафедры'
    search_cath[
        'Кафедра астрономии и космической геодезии'] = 'Сотрудники кафедры'
    search_cath['Кафедра вычислительной физики'] = 'Коллектив кафедры'

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, search_cath[name])
        result[name] = stuff_link

    for name, stuff_link in result.items():
        if name == 'Кафедра радиоастрономии':
            result[name] = get_phys_teachers_rad_astr(stuff_link)
        else:
            try:
                result[name] = gather_name_link_of_employees(stuff_link)
            except AttributeError:
                result[name] = get_phys_teachers(stuff_link)

    return result


def gather_name_link_of_cathedras_of_chem(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='visit_link')
    uls = div.find_all('ul')

    i = 0

    lis = []
    for ul in uls:
        if i == 0:
            lis += ul.find_all('li', class_='li_spec')
        i = 1
    cathedras = []
    for li in lis:
        a = li.find('a')
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
    return cathedras


def parse_chem(link):
    struct_button_link = get_link_from_menu_list_left(link, 'Структура')

    cathedras = gather_name_link_of_cathedras_of_chem(struct_button_link)
    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, 'Список сотрудников')
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees(stuff_link)

    return result


def gather_name_link_of_employees_of_law3(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="lxml")
    teachers_list = soup.select('p>a[href]')
    employees = []
    for i in teachers_list:
        if i.text:
            employees.append((i.text, i.get('href')))
    return employees


def gather_name_link_of_cathedras_of_law(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    uls = soup.find_all('ul', class_='menu_list')

    lis = []
    search_cat = {}

    i = 0
    for ul in uls:
        if i < 2:
            lis += ul.find_all('li', class_='li_spec')
        i += 1
    cathedras = []

    for li in lis:
        a = li.find('a')
        if a.text.startswith('Кафедра'):
            cathedras.append((a.text, a.get('href')))
            search_cat[a.text] = 'Сотрудники'
    return cathedras, search_cat


def parse_law(link):
    result = {}

    cathedras, search_cath = gather_name_link_of_cathedras_of_law(link)
    search_cath[
        'Кафедра предпринимательского и энергетического права'] = 'Сотрудники кафедры'

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, search_cath[name])
        result[name] = stuff_link

    for name, stuff_link in result.items():
        result[name] = gather_name_link_of_employees_of_law3(stuff_link)
    return result


def get_phys_teachers(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    teachers_list = soup.select('p a[href]')
    employees = []
    for i in teachers_list:
        employees.append((i.text, i.get('href')))
    return employees


def get_phys_teachers_rad_astr(link):
    html = tools.get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    teachers_list = soup.select('.visit_link ul li a[href]')
    rad_astr = []
    for i in teachers_list:
        rad_astr.append((i.text, i.get('href')))
    return rad_astr
