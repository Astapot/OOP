import requests

vk_token = 'vk1.a._0ZncLWb3CSLzETNzUmSNwGhk5eqaTfy_V8DUrUZCdnJozvpKTqN6wSskvoV14Lxtn2kA4K_4_n3Wy_ce1jtXaLavVf7O9KYb4erW_HEcIfrm6Ds2XnKzqg_X92XuPS5_ke182mHlZTgwjJQa_0cM6oByflWdSvKFjb235-KSXjxezHiJdHMADs83b6rrCTQZ-6ibBUEB3mHHOKM-fUplw'
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
