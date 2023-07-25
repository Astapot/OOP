import vk_api
from vk_api.utils import get_random_id
import requests
from vk_api.upload import VkUpload
from io import BytesIO

my_vk_token = 'vk1.a.u7bFzy6gtq7feV3_Ojm8lxFbn1RVHEJgVP7D4eYglAfTRoRoBBWlvg4elxV9oZIQ6pZc2VD4D01yDrIxdPMV0EyahZQC_OVd2c3OXEKV6acXl4-gi4eCMOfr7DESErZsiO-wG_wronaI_e5CClZq1kgEpcJhjvB7ejJwLa6fFLXjUiJJBWblNc8AVNa3lczDfJP3enozdRCMllAqywxfdw'
vk_token = 'vk1.a._0ZncLWb3CSLzETNzUmSNwGhk5eqaTfy_V8DUrUZCdnJozvpKTqN6wSskvoV14Lxtn2kA4K_4_n3Wy_ce1jtXaLavVf7O9KYb4erW_HEcIfrm6Ds2XnKzqg_X92XuPS5_ke182mHlZTgwjJQa_0cM6oByflWdSvKFjb235-KSXjxezHiJdHMADs83b6rrCTQZ-6ibBUEB3mHHOKM-fUplw'
auth = vk_api.VkApi(token=vk_token)
# longpoll = VkLongPoll(auth)
vk = auth.get_api()
upload = VkUpload(vk)
url = 'https://sun9-34.userapi.com/impf/WHJspkX57kqpCZYuJh091aZdpGX20ZYOWh1d6w/cRWfo0uM_X4.jpg?size=810x1080&quality=96&sign=cbe690ce218ffb3750835c54193d269d&c_uniq_tag=Hr7rOcQ8F4-wWXzdfHUVh3ojIirK8W3QpdpO3fb-PGw&type=album'


def write_message(user, message, keyboard=None):
    if keyboard == None:
        auth.method('messages.send', {'user_id': user, 'message': message, 'random_id': get_random_id()})
    else:
        auth.method('messages.send', {'user_id': user, 'message': message, 'random_id': get_random_id(), 'keyboard': keyboard.get_keyboard()})



def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)
    response = upload.photo_messages(f)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    return owner_id, photo_id, access_key


def send_photo(auth, user, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    auth.method('messages.send', {'user_id': user, 'attachment': attachment, 'random_id': get_random_id()})

#
# pprint(upload_photo(upload, url))