import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from work_with_photos import get_photos
from vk_api.upload import VkUpload
from send_mes import write_message, upload_photo, send_photo
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from BD import add_elect_user, find_elect_id, give_all_elect_users, get_number, update_number
from get_info import get_info, find_people, get_friends

my_vk_token = ''
vk_token = ''
auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)

# Клавиатура
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


# Цикл общения с ботом
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user = event.user_id
        # Кнопка старт ранее собирала информацию о пользователе, сейчас по сути является рудиментом,
        # но пусть будет, лишний раз можно будет вспомнить как все работало
        if message.capitalize() == 'Старт':
            write_message(user, 'Ку', start_keyboard)
            user_city, number_user_city, user_sex, age_user, amplitude = get_info(user)
        # В команде "найди людей" следовало бы исправить то, что поиск начинается всегда с нуля,
        # а не с номера пользователя. Но, возможно, в следующий раз:)
        elif message == 'Найди людей':
            user_city, number_user_city, user_sex, age_user, amplitude = get_info(user)
            try:
                # Для того чтобы бот работал с несколькими людьми одновременно, пришлось вставлять одни и те же функции
                # в разные команды, думал из-за этого он сильно замедлится, но я ошибался)
                men, find_sex = find_people(number_user_city, user_sex, age_user, amplitude)
                number = 0
                current_man = men[number]
                favourite = find_elect_id(current_man['id'], user)
                friends_ids = get_friends(user)
                while True:
                    number += 1
                    current_man = men[number]
                    favourite = find_elect_id(current_man['id'], user)
                    if current_man['id'] not in friends_ids and not favourite:
                        break
                update_number(user, number)
                name, last_name = current_man['first_name'], current_man['last_name']
                link = 'https://vk.com/id' + str(current_man['id'])
                popular_photos = get_photos(current_man['id'], my_vk_token)
                write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}', keyboard=continue_keyboard)
                for photo_url in popular_photos:
                    owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                    send_photo(auth, user, owner_id, photo_id, access_key)
            #  трай ексепт не убирал, он не мешает. Но сейчас по сути рудимент, так как все возможные ошибки убрал
            except Exception:
                write_message(user, 'Вас пока нет в базе, попробуйте выбрать Старт', start_keyboard)
        #    кнопка следующий, теперь заново собирает информацию о пользователе и уже потом дает ему следующего
        # тем самым теперь можно работать с несколькими людьми одновременно
        elif message == 'Следующий':
            user_city, number_user_city, user_sex, age_user, amplitude = get_info(user)
            number = get_number(user)[0]
            number += 1
            if number >= 500:
                write_message(user, 'Люди закончились, попробуй заново!', start_keyboard)
            else:
                men, find_sex = find_people(number_user_city, user_sex, age_user, amplitude)
                current_man = men[number]
                favourite = find_elect_id(current_man['id'], user)
                friends_ids = get_friends(user)
                while True:
                    number += 1
                    current_man = men[number]
                    favourite = find_elect_id(current_man['id'], user)
                    if current_man['id'] not in friends_ids and not favourite:
                        break
                update_number(user, number)
                current_man = men[number]
                name, last_name = current_man['first_name'], current_man['last_name']
                link = 'https://vk.com/id' + str(current_man['id'])
                popular_photos = get_photos(current_man['id'], my_vk_token)
                write_message(user, f'имя - {name}, фамилия - {last_name}, ссылка - {link}')
                for photo_url in popular_photos:
                    owner_id, photo_id, access_key = upload_photo(upload, photo_url)
                    send_photo(auth, user, owner_id, photo_id, access_key)
        elif message == 'В начало':
            write_message(user, 'Снова здесь', start_keyboard)
        elif message == 'Добавить в избранное':
            user_city, number_user_city, user_sex, age_user, amplitude = get_info(user)
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



