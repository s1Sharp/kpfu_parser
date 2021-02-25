from ildar import get_link_from_menu_list_left, gather_name_link_of_employees, gather_name_link_of_cathedras_of_ivmiit


def parse_higher_school_buisness(link):
    employees_link = get_link_from_menu_list_left(link, 'Список сотрудников')
    return {'Основная кафедра школы': gather_name_link_of_employees(employees_link)}


def parse_economics(link):
    struct_link = get_link_from_menu_list_left(link, 'Структура')
    cathedras_link = get_link_from_menu_list_left(struct_link, 'Кафедры')

    cathedras = gather_name_link_of_cathedras_of_ivmiit(cathedras_link)
    result = {}

    for name, link in cathedras:
        stuff_link = get_link_from_menu_list_left(link, 'Сотрудники')
        result[name] = stuff_link

    return result


