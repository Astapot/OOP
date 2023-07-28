import vk_api
from vk_api.longpoll import VkLongPoll
import requests
from vk_api.upload import VkUpload
from datetime import date
from BD import add_user


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


my_vk_token = ''
vk_token = ''
auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)


