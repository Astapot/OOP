import vk_api
from vk_api.utils import get_random_id
import requests
from vk_api.upload import VkUpload
from io import BytesIO
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_token, my_vk_token

auth = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(auth)
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