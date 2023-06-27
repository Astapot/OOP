from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)


result = []
contacts = []
for id, string in enumerate(contacts_list):
    string1 = ', '.join(string)
    contact = []
    if id == 0:
        contacts.append(string)



    # Задание 1. Разбор ФИО



    for value in range(3):
        pattern = r"\s"
        part_of_name = re.split(pattern, string[value])
        contact.extend(part_of_name)
    while len(contact) != 3:
        contact.remove('')


    # Добавление неизменяемой информации

    contact.append(string[3])
    contact.append(string[4])

    # 2. Изменение и добавление номера

    pattern_tel = r"(\+7|8)\s*\(?(\d{3})\)?(\s|-)?(\d*)(\s|-)*(\d*)(\s|-)*(\d*)(\s*)\(?(доб.)?\s*([0-9]*)\)?"
    subst_pattern_tel = r"+7(\2)\4\6\8\9\10\11"
    new_string = re.sub(pattern_tel, subst_pattern_tel, string1)
    result.append(new_string)
    pattern_2 = r"\+7\(\d{3}\)\d{7}\s?(доб.)?(\d+)?"
    tel_2 = re.search(pattern_2, new_string)
    if tel_2 is not None:
        contact.append(tel_2.group())
    else:
        contact.append('')

    #  Добавление неизменяемой информации

    contact.append(string[6])

    # Запись в список

    contacts.append(contact)
# pprint(contacts)

# Объединение и удаление дублей
for id, string in enumerate(contacts):
    for id_2, string_2 in enumerate(contacts):
        if id >= id_2:
            continue
        for k in range(7):
            if k in [3,4]:
                continue
            if string[k] != string_2[k]:
                continue
            if len(string[k]) == 0 and len(string_2[k]) == 0:
                continue
            else:
                # doubles[id] = id_2
                for id_double, word in enumerate(contacts[id]):
                    if len(word) == 0 and len(contacts[id_2][id_double]) > 0:
                        contacts[id][id_double] = contacts[id_2][id_double]
                contacts.pop(id_2)
                break
# pprint(contacts)




with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts)
