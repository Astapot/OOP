import os
import requests

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_link(self, file_for_replace):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': file_for_replace, 'overwrite': 'true'}
        response = requests.get(url, headers=headers, params=params)
        print(response.json())
        href = response.json()['href']
        return href

    def upload(self, file_path: str, file_for_replace):
        key = self.get_link(file_for_replace= file_for_replace)
        with open('estsetset.txt') as data:
            response = requests.put(key, data)
        print(response)


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    file_for_replace = 'test/new.docx'
    a = os.getcwd()
    b = 'estsetset.txt'
    print(os.path.join(a, b))
    path_to_file = os.path.join(a, b)
    token = 'здесь должен был быть токен, не понял в чем смысл был убирать его, но все работало'
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file, file_for_replace)