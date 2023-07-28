import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from work_with_photos import get_photos
from vk_api.upload import VkUpload
from send_mes import write_message, upload_photo, send_photo
from datetime import date
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from BD import add_user, add_elect_user, find_elect_id, give_all_elect_users

my_vk_token = ''
vk_token = ''
auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)
start_keyboard = VkKeyboard(one_time=True)
start_keyboard.add_button('Найди людей', color=VkKeyboardColor.PRIMARY)
start_keyboard.add_line()
start_keyboard.add_button('Вывести список избранных', color=VkKeyboardColor.SECONDARY)
start_keyboard.add_line()
start_keyboard.add_button('Старт', color=VkKeyboardColor.NEGATIVE)

continue_keyboard = VkKeyboard(one_time=False)
continue_keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
continue_keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.PRIMARY)
continue_keyboard.add_line()
continue_keyboard.add_button('В начало', color=VkKeyboardColor.NEGATIVE)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user = event.user_id
        if message.capitalize() == 'Старт':
            write_message(user, 'Ку', start_keyboard)
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
        elif message == 'Найди людей':
            try:
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
                number = 0
                current_man = men[number]
                favourite = find_elect_id(current_man['id'], user)
                params_for_friends = {
                    'user_id': user,
                    'access_token': my_vk_token,
                    'v': 5.131
                }
                response_for_friends = requests.get('https://api.vk.com/method/friends.get', params=params_for_friends)
                friends_ids = response_for_friends.json()['response']['items']
                while True:
                    number += 1
                    current_man = men[number]
                    favourite = find_elect_id(current_man['id'], user)
                    if current_man['id'] not in friends_ids and not favourite:
                        break
                name, last_name = current_man['first_name'], current_man['last_name']
                link = 'https://vk.com/id' + str(current_man['id'])
                popular_photos = get_photos(current_man['id'], my_vk_token)
                write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}', keyboard=continue_keyboard)
                for photo_url in popular_photos:
                    owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                    send_photo(auth, user, owner_id, photo_id, access_key)
            except Exception:
                write_message(user, 'Вас пока нет в базе, попробуйте выбрать Старт', start_keyboard)
        elif message == 'Следующий':
            try:
                number += 1
                if number >= params_for_search['count']:
                    write_message(user, 'Люди закончились, попробуй заново!', start_keyboard)
                else:
                    current_man = men[number]
                    favourite = find_elect_id(current_man['id'], user)
                    params_for_friends = {
                        'user_id': user,
                        'access_token': my_vk_token,
                        'v': 5.131
                    }

                    response_for_friends = requests.get('https://api.vk.com/method/friends.get', params=params_for_friends)
                    friends_ids = response_for_friends.json()['response']['items']
                    while True:
                        number += 1
                        current_man = men[number]
                        favourite = find_elect_id(current_man['id'], user)
                        if current_man['id'] not in friends_ids and not favourite:
                            break
                    current_man = men[number]
                    name, last_name = current_man['first_name'], current_man['last_name']
                    link = 'https://vk.com/id' + str(current_man['id'])
                    popular_photos = get_photos(current_man['id'], my_vk_token)
                    write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}')
                    for photo_url in popular_photos:
                        owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                        send_photo(auth, user, owner_id, photo_id, access_key)
            except NameError:
                write_message(user, 'Обновите базу, нажмите \'Старт\'', start_keyboard)

        elif message == 'В начало':
            write_message(user, 'Снова здесь', start_keyboard)
        elif message == 'Добавить в избранное':
            el_man_id = current_man['id']
            result = add_elect_user(user, el_man_id, name, last_name, link, find_sex, user_city)
            if result:
                write_message(user, 'Данный пользователь уже есть в избранном!',
                              continue_keyboard)
            else:
                write_message(user, 'Пользователь успешно добавлен в избранное!',
                              continue_keyboard)
        elif message == 'Вывести список избранных':
                    result = give_all_elect_users(user)
                    if type(result) == list:
                        for number, man in enumerate(result):
                            write_message(user, f'{number + 1}. Имя - {man[0]}, фамилия - {man[1]}, страница - {man[2]}',
                                          start_keyboard)
                    elif result == 'no users':
                        write_message(user, 'У вас пока нет избранных пользователей', start_keyboard)
                    elif not result:
                        write_message(user, 'Вас нет в базе, попробуйте выбрать команду "Старт"', start_keyboard)

        else:
            params_for_get = {
                'user_ids': user,
                'access_token': vk_token,
                'v': 5.131
            }
            response = requests.get('https://api.vk.com/method/users.get', params=params_for_get)
            info = response.json()['response'][0]
            write_message(user, f'Я не понимаю вас, пожалуйста, перейдите в "Старт", {info["first_name"]}', start_keyboard)