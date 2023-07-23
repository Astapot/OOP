import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
from pprint import pprint
from work_with_photos import get_photos
from vk_api import VkApi
from vk_api.upload import VkUpload
from io import BytesIO
from send_mes import write_message, upload_photo, send_photo
from datetime import date


my_vk_token = 'vk1.a.u7bFzy6gtq7feV3_Ojm8lxFbn1RVHEJgVP7D4eYglAfTRoRoBBWlvg4elxV9oZIQ6pZc2VD4D01yDrIxdPMV0EyahZQC_OVd2c3OXEKV6acXl4-gi4eCMOfr7DESErZsiO-wG_wronaI_e5CClZq1kgEpcJhjvB7ejJwLa6fFLXjUiJJBWblNc8AVNa3lczDfJP3enozdRCMllAqywxfdw'
vk_token = 'vk1.a._0ZncLWb3CSLzETNzUmSNwGhk5eqaTfy_V8DUrUZCdnJozvpKTqN6wSskvoV14Lxtn2kA4K_4_n3Wy_ce1jtXaLavVf7O9KYb4erW_HEcIfrm6Ds2XnKzqg_X92XuPS5_ke182mHlZTgwjJQa_0cM6oByflWdSvKFjb235-KSXjxezHiJdHMADs83b6rrCTQZ-6ibBUEB3mHHOKM-fUplw'
auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user = event.user_id
        if message == 'Привет':
            write_message(user, 'Ку')
        elif message == 'Найди людей':
            params_for_get = {
                'user_ids': user,
                'fields': 'city, sex, bdate',
                'access_token': vk_token,
                'v': 5.131
            }
            response = requests.get('https://api.vk.com/method/users.get', params=params_for_get)
            info = response.json()['response'][0]
            user_city = info['city']['title']
            number_user_city = info['city']['id']
            user_sex = info['sex']
            try:
                user_bdate = info['bdate'].split('.')
                year_user, month_user, day_user = reversed(user_bdate)
                d1 = date.today()
                d2 = date(int(year_user), int(month_user), int(day_user))
                delta = d1 - d2
                age_user = delta.days // 365
            except Exception:
                age_user = 27
            if user_sex == 2:
                find_sex = 1
            elif user_sex == 1:
                find_sex = 2
            else:
                find_sex = 0
            params_for_search = {
                'count': 100,
                'fields': 'city, sex, bdate, is_closed, is_friend',
                'city': number_user_city,
                'sex': find_sex,
                'access_token': my_vk_token,
                'age_from': age_user - 5,
                'age_to': age_user + 5,
                'v': 5.131
            }
            found_people = requests.get('https://api.vk.com/method/users.search', params=params_for_search)
            men = found_people.json()['response']['items']
            print(men)
            number = 0
            while men[number]['is_friend'] == 1:
                number += 1
            current_man = men[number]
            name, last_name = current_man['first_name'], current_man['last_name']
            link = 'https://vk.com/id' + str(current_man['id'])
            popular_photos = get_photos(current_man['id'], my_vk_token)
            write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}')
            for photo_url in popular_photos:
                owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                send_photo(auth, user, owner_id, photo_id, access_key)
        elif message == 'Следующий':
            number += 1
            while men[number]['is_friend'] == 1:
                number += 1
            current_man = men[number]
            name, last_name = current_man['first_name'], current_man['last_name']
            link = 'https://vk.com/id' + str(current_man['id'])
            popular_photos = get_photos(current_man['id'], my_vk_token)
            write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}')
            for photo_url in popular_photos:
                owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                send_photo(auth, user, owner_id, photo_id, access_key)
        else:
            write_message(user, f'Я не понимаю вас, {user}')



