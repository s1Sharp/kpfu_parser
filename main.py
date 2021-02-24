import tools
import constants
from pprint import pprint

from ildar import gather_name_link_of_institutes, parse_ivmiit


def main():
    html = tools.get_html(constants.initial_url)
    institutes = gather_name_link_of_institutes(html)
    print(f'институты: {institutes}')
    print(f'количество институтов: {len(institutes)}')

    parsing_dictionary = {'Институт вычислительной математики и информационных технологий': parse_ivmiit}

    data = {}
    for name, link in institutes:
        func = parsing_dictionary.get(name)
        if func:
            data[name] = func(link)

    pprint(data)


if __name__ == '__main__':
    main()
