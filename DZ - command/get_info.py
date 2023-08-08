import vk_api
from vk_api.longpoll import VkLongPoll
import requests
from vk_api.upload import VkUpload
from datetime import date
from BD import add_user
from config import vk_token, my_vk_token

def get_info(user):
    params_for_get = {
        'user_ids': user,
        'fields': 'city, sex, bdate',
        'access_token': vk_token,
        'v': 5.131
    }
    response = requests.get('https://api.vk.com/method/users.get', params=params_for_get)
    info = response.json()['response'][0]
    if 'city' in info:
        user_city = info['city']['title']
        number_user_city = info['city']['id']
    else:
        user_city = 'Воронеж'
        number_user_city = '42'
    if 'sex' in info:
        user_sex = info['sex']
    else:
        user_sex = 0
    try:
        user_bdate = info['bdate'].split('.')
        year_user, month_user, day_user = reversed(user_bdate)
        d1 = date.today()
        d2 = date(int(year_user), int(month_user), int(day_user))
        delta = d1 - d2
        age_user = delta.days // 365
        amplitude = 5
    except Exception:
        age_user = 0
        amplitude = 100
    add_user(user, info["first_name"], info["last_name"], user_sex, age_user, user_city)
    return user_city, number_user_city, user_sex, age_user, amplitude


def find_people(number_user_city, user_sex, age_user, amplitude):
    if user_sex == 2:
        find_sex = 1
    elif user_sex == 1:
        find_sex = 2
    else:
        find_sex = 0
    params_for_search = {
        'count': 500,
        'fields': 'city, sex, bdate, is_closed, is_friend',
        'city': number_user_city,
        'sex': find_sex,
        'access_token': my_vk_token,
        'age_from': age_user - amplitude,
        'age_to': age_user + amplitude,
        'v': 5.131
    }
    found_people = requests.get('https://api.vk.com/method/users.search', params=params_for_search)
    men = found_people.json()['response']['items']
    return men, find_sex


def get_friends(user):
    params_for_friends = {
        'user_id': user,
        'access_token': my_vk_token,
        'v': 5.131
    }
    response_for_friends = requests.get('https://api.vk.com/method/friends.get', params=params_for_friends)
    friends_ids = response_for_friends.json()['response']['items']
    return friends_ids


def get_photos(user_id, vk_token, offset=0):
    three_popular_photos = []
    result_photos = {}
    new_offset = offset
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'access_token': vk_token,
        'extended': 1,
        'photo_sizes': 0,
        'offset': new_offset,
        'count': 10,
        'v': 5.131
    }
    while True:
        try:
            response = requests.get('https://api.vk.com/method/photos.get', params=params)
            array_photos = response.json()['response']['items']
            if len(array_photos) != 0:
                for num, photo in enumerate(array_photos):
                    photo_likes = photo['likes']['count']
                    photo_url = photo['sizes'][-1]['url']
                    result_photos[photo_url] = photo_likes
                params['offset'] = params['offset'] + params['count']
        except Exception:
            break
    if len(result_photos.values()) > 3:
        popular_photo_likes = sorted(result_photos.values())[-1:-4:-1]
    else:
        popular_photo_likes = result_photos.values()
    for i in popular_photo_likes:
        for url in result_photos.keys():
            if result_photos[url] == i:
                three_popular_photos.append(url)
                break
    return three_popular_photos





auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)


