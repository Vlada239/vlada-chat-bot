from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from defs.functions import *
from defs.tools import *
from dicts.dictionaries import *

VK_TOKEN = 'a47436d8894f49e81a488838f5ad9d9e56718655410b974ded4d48739f1ac128e19e12209fd8fd1e47b9f'
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user = event.user_id

        if not (user in статусы):
            статусы[user] = {'статус': '0', 'mode': '', 'answer': '', 'question': '', 'dict': ''}

        if check_word_matching(request, {'назад'}):
            назад(статусы, user)
        elif check_word_matching(request, {'привет', 'хай', 'начать', 'хаюшки', 'здравствуй'}):
            статусы[user] = {'статус': '0', 'mode': '', 'answer': '', 'question': '', 'dict': ''}
            name = get_user_name(event.user_id)
            if name == 'Влада' or name == 'Vlada':
                send_msg(event.user_id, 'Повинуюсь, создательница')
            else:
                send_msg(event.user_id, f'Привет, {name}!')
            просмотр(статусы, user)

        elif конец(статусы[user]['статус']) and статусы[user]['mode'] == '':
            if request == '1':
                статусы[user]['mode'] = 'a'
                send_msg(user, 'Ты перешел в режим переводчика.')
                send_msg(user, 'Введи термин')
            elif request == '2':
                статусы[user]['mode'] = 'b'
                b_q(user)
            elif request == '3':
                статусы[user]['mode'] = 'c'
                c_q(user)
            else:
                send_msg(user, 'Что-то не то. Если хочешь вернуться назад, напиши "выход".')

        elif not статусы[user]['mode'] == '':
            if статусы[user]['mode'] == 'a':
                a(request, user)
            elif статусы[user]['mode'] == 'b':
              if check_word_matching(request, {'ответ'}):
                b_a(user)
                b_q(user)
              else:
                send_msg(user, 'Мне кажется, такого варианта не было. Если хочешь вернуться назад, напиши "выход".')
            elif статусы[user]['mode'] == 'c':
                c_a(user, request)
                c_q(user)
        else:
            вперед(статусы, user, request)