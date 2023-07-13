# я не стал менять полностью структуру старого дз, изменил только простой код на функции, чтобы все работало,
# поэтому не придирайтесь пожалуйста к pep8:)



def find_russia(geo_logs):
    new = []

    for item in geo_logs:
        visit = list(item.values())[0]
        if 'Россия' in visit:
            new.append(item)
    geo_logs = new
    return geo_logs


# ЗАДАНИЕ 2

def find_unique_id(ids):
    # ids = {'user1': [213, 213, 213, 15, 213],
    #        'user2': [54, 54, 119, 119, 119],
    #        'user3': [213, 98, 98, 35]}

    all = []

    for id in ids.values():
      all.extend(id)

    res = list(set(all))
    return res


# ЗАДАНИЕ 3


# queries = [
#     'смотреть сериалы онлайн',
#     'новости спорта',
#     'афиша кино',
#     'курс доллара',
#     'сериалы этим летом',
#     'курс по питону',
#     'сериалы про спорт'
#     ]

# quantity = []

# for sen in queries:
#   count = sen.count(' ') + 1
#   quantity.append(count)


# Развилка на 2 решения, первое просто через цикл, второе через словарь, мне больше 1 нравится но тема лекции про словарь была, поэтому вот:


# 1 решение


# for i in set(quantity):
#   print(f'Поисковых запросов из {i} слов(а): {round(quantity.count(i)/len(quantity) * 100)} %')


# 2 решение

# result = {f'Поисковых запросов из {i} слов' : f'{round(quantity.count(i)/len(quantity) * 100)} %' for i in quantity}
# print(result)


# ЗАДАНИЕ 4

def find_max_stats(stats):

    # stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}

    # 1 решение, было самым очевидным сразу

    # max = max(list(stats.values()))
    # print(list(stats.keys())[list(stats.values()).index(max)])

    # 2 решение. хз мне ни одно почему-то не нравится, хотелось что-то поумнее, но уже лень

    for name, vol in list(stats.items()):
        if vol == max(list(stats.values())):
            return(name)

# Задание 5

# spisok = ['2018-01-01', 'yandex', 'cpc', 100]
# slovar = {spisok[-1]}

# for i in range(len(spisok)-1):
#     slovar = {spisok[-i-2]: slovar}

# print(slovar)