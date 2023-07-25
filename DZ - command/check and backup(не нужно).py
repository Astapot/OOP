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