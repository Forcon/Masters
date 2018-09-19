# from operator import attrgetter


mas_sql = {'1': 'Masya',
           '2': 'Forcon', '3':'Forcon', '4': 'Forcon',
           '5': 'Alex',
           '6': 'Tupsya', '7': 'Tupsya'
            }

len_user = {'Masya': 1, 'Forcon': 3, 'Alex': 1, 'Tupsya': 2}

def dict_to_mass_value(dict_autor):
    massiv_rez = []
    for key, value in dict_autor.items():
        massiv_rez.append(value)

    return massiv_rez


def toomass_to_mass(dict_autor, elem=None):
    massiv_rez = []
    for el in dict_autor:
        massiv_rez.append(el[elem])

    return massiv_rez


def sort_massiv(mas_sql, len_user):
    """
    Сортирует массив типа "словарь" по принципу: сначала идут те, у которых больше значений внутри
    :param mas_sql:
    :param len_user:
    :return:
    """
    rez_sort = sorted(len_user.items(), key=lambda x: x[1], reverse = True)

    dict_mas = {}
    # m = dict_mas.fromkeys(list(len_user.keys()))
    m_dict = dict_mas.fromkeys([i[0] for i in rez_sort])

    # print(rez_sort)

    rez = []
    old_key = list(len_user.keys())[0]
    for key, value in mas_sql.items():
        if old_key != value:
            rez = []
        rez.append(key)
        m_dict[value] = rez
        old_key = value

    return dict_to_mass_value(m_dict), toomass_to_mass(rez_sort, 0), toomass_to_mass(rez_sort, 1)
    #     print(m_dict)
    #
    # print(m_dict)
    # print(rez_sort)

if __name__ == '__main__':
    autor_name = 'forcon'
    t_search = 'выдра'
    sort_massiv(mas_sql, len_user)