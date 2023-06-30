import bs4
import requests
import fake_headers as fk
from pprint import pprint
import re
import json

# получаю все вакансии
result = {}
headers = fk.Headers(browser='firefox', os='win').generate()
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url, headers=headers).text
soup = bs4.BeautifulSoup(response, 'lxml')
step_1 = soup.find_all('div', class_='serp-item')
number = 1

for vacancy in step_1:
    # получаю ссылку на каждую вакансию и проверяю, что внутри нее в описании есть django flask
    body_tag = vacancy.find('div', class_='vacancy-serp-item-body__main-info')
    a_tag = body_tag.find('a')
    link = a_tag['href']
    description_response = requests.get(link, headers=headers).text
    description_soup = bs4.BeautifulSoup(description_response, 'lxml')
    description = description_soup.find('div', class_="g-user-content").text
    pattern_desc = r'[dD]?jango|[fF]lask'
    results_d = re.findall(pattern_desc, description)
    if len(results_d) == 0:
        continue

    # получаю зарплату(был метод text), город и компанию

    salary1 = body_tag.find('span', class_='bloko-header-section-3')

    # дальнейший способ решения не для слабонервных) я делал это сначала и только под конец дз узнал что можно было просто сделать .text:(((

    str_salary = str(salary1)
    pattern = r'\d+\s\d+'
    results = re.findall(pattern, str_salary)
    pattern_for_sub = r'\u202f'
    pattern_after_replace = r' '
    final_salary = []
    for i in results:
        zp = re.sub(pattern_for_sub, pattern_after_replace, i)
        final_salary.append(zp)
    if len(final_salary) > 1:
        salary = f'от {final_salary[0]} до {final_salary[1]}'
    elif len(final_salary) == 1:
        salary = f'{final_salary[0]} ровно'
    else:
        salary = f'зарплата неизвестна'
    city_tag = body_tag.find('div', class_='vacancy-serp-item-company')
    city_tag2 = city_tag.find('div', class_='vacancy-serp-item__info')
    city_tag3 = city_tag2.find_all('div', class_='bloko-text')
    city = city_tag3[1].text
    company_a_tag = city_tag2.find('a')
    company = company_a_tag.text
    # заполняю словарь
    result[number]={'ссылка': link, 'вилка зп': salary, 'название компании': company, 'город': city}
    number += 1
# pprint(result)
# записываю в файл
with open('work.json', 'w') as f:
    json.dump(result, f)


# проверка файла
# with open('work.json', 'r', encoding='utf-8') as f:
#     text = json.load(f)
#     print(text)