import requests
from pprint import pprint
from progress.bar import IncrementalBar

YA_TOKEN = ''
ID_app = ''
VK_TOKEN = ''
headers = {'Content-Type': 'application/json',
           'Authorization': 'OAuth {}'.format(YA_TOKEN)}
url = 'https://cloud-api.yandex.net/v1/disk/resources'
result = []


def backup(folder_for_backup, offset=0, count=5):
    new_offset = offset
    params = {
        'owner_id': '',
        'album_id': 'profile',
        'access_token': VK_TOKEN,
        'extended': 1,
        'photo_sizes': 0,
        'offset': new_offset,
        'count': 5,
        'v': 5.131
    }
    response = requests.get('https://api.vk.com/method/photos.get', params=params)
    array_photos = response.json()['response']['items']
    if len(array_photos) != 0:
        bar = IncrementalBar('Finished', max=min(count - new_offset, int(params['count']), len(array_photos)))
        for num, photo in enumerate(array_photos):
            if new_offset + num == count:
                return result
            photo_url = photo['sizes'][-1]['url']
            photo_name = '/' + str(photo['likes']['count']) + '_' + str(photo['date']) + '.png'
            if photo_name.split('_')[1] in array:
                continue
            upload_photo(photo_url, photo_name)
            result.append({'file_name': photo_name.lstrip('/'), 'size': photo['sizes'][-1]['type']})
            bar.next()
        new_offset = params['offset'] + params['count']
        bar.finish()
        backup(folder_for_backup, new_offset, count)
    return result


def upload_photo(url_photo, photo_name):
    params = {'path': folder_for_backup + photo_name, 'url': url_photo}
    response = requests.post(url + '/upload', headers=headers, params=params)
    return


def ya_info(folder):
    array_ = []
    params = {'path': folder}
    files = requests.get(url, headers=headers, params=params)
    for photo in files.json()['_embedded']['items']:
        array_.append(photo['name'].split('_')[1])
    return array_


if __name__ == '__main__':
    folder_for_backup = ''
    array = ya_info(folder_for_backup)
    pprint(backup(folder_for_backup, 0, 6))
