import unittest

import requests
from unittest import TestCase
import pytest

path = "test_netology"
YA_Token = ''
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {YA_Token}'}
params = {'path': path}

# необходимые функции:


def create_folder(URL, params, headers):
    response = requests.put(URL, params=params, headers=headers)
    return response
# create_folder(URL, params, headers)


def check_folder(URL, path, headers):
    params = {'path': path}
    response = requests.get(URL, headers=headers, params=params)
    return response

def find_files(headers):
    files = []
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    response = requests.get(URL, headers=headers)
    result = response.json()['items']
    for item in result:
        name = item['name'].split('.')
        files.append(name[0])
    return files


# Тесты:
class TestYaApi(TestCase):
    def test_checkfolder1(self):
        result = check_folder(URL, 'test_netology', headers).status_code
        expected = 200
        self.assertEqual(result, expected, 'something wrong')

    @unittest.expectedFailure
    def test_wrongfolder(self):
        result = check_folder(URL, 'tests_netology', headers).status_code
        expected = 200
        self.assertEqual(result, expected, 'something wrong')


# не понял как проверить есть ли папка в списке файлов, так как в полигоне не нашел метода получить все папки, только файлы.
# Поэтому вот вам тест для проверки наличия какого-либо файла

    def test_find_file(self):
        files = find_files(headers)
        name_of_your_file = 'Мишки'
        self.assertIn(name_of_your_file, files, 'Такого нет')





