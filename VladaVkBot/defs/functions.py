from defs.tools import *
from dicts.dictionaries import *
import random


def начало(элемент):
    if элемент in основное_меню.keys():
        return False
    else:
        return True


def конец(элемент):
    if элемент in основное_меню_реверс.keys():
        return False
    else:
        return True


def send_msg(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': randint(1e16, 1e18)})


def a(request, user):
    actual_dict = статусы[user]['dict']
    if request in actual_dict:
        send_msg(user, actual_dict[request])
    else:
        send_msg(user, 'Извини, этого я пока не знаю.')


def b_q(user):
    dict = статусы[user]['dict']
    term, статусы[user]['question'] = random.choice(list(dict.items()))
    send_msg(user, term)
    send_msg(user, 'Если хочешь прочитать правильное определение, напиши "ответ".')


def b_a(user):
    send_msg(user, статусы[user]['question'])


def c_q(user):
  dict = статусы[user]['dict']
  статусы[user]['answer'], definition = random.choice(list(dict.items()))
  print(type(definition))
  send_msg(user, definition)
  send_msg(user, 'Напиши, что это за термин.')


def c_a(user, request):
  if request == статусы[user]['answer']:
    send_msg(user, 'Ты молодец! Это верно.')
  else:
    send_msg(user, 'Неверно.')
    send_msg(user, f"правильный ответ: {статусы[user]['answer']}")


def назад(статусы, пользователь):
    статусы[пользователь]['mode'] = ''
    if not начало(статусы[пользователь]['статус']):
        статусы[пользователь]['статус'] = основное_меню[статусы[пользователь]['статус']]
        просмотр(статусы, пользователь)
    else:
        send_msg(пользователь, 'Сейчас ты находишься в главном меню. Отступать больше некуда. Ха-ха.')
        просмотр(статусы, пользователь)


def вперед(статусы, пользователь, request):
    лажа = 0
    for i in основное_меню_реверс[статусы[пользователь]['статус']]:
        if request == коды[i]:
            if i in основное_меню_реверс.keys():
                статусы[пользователь]['mode'] = ''
                статусы[пользователь]['статус'] = i
                просмотр(статусы, пользователь)
                лажа = 0
                break
            else:
                if i in словари:
                    статусы[пользователь]['статус'] = i
                    статусы[пользователь]['dict'] = словари[i]
                    send_msg(пользователь, f"Ты в списке определений, выбери режим взаимодействия с ним: 1 - переводчик, 2 - термин по значению, 3 - значение по термину.")
                    лажа = 0
                    break
                else:
                    send_msg(пользователь, f"Извини, этот раздел еще в разработке.")
                    лажа = 0
                    break
        else:
            лажа = 1
    if лажа == 1:
        send_msg(пользователь, 'Мне кажется, такого варианта не было.')


def просмотр(статусы, пользователь):
    статус_в_словах = коды[статусы[пользователь]['статус']]
    send_msg(пользователь, f'Сейчас ты на {статус_в_словах}')
    send_msg(пользователь, 'Ты можешь перейти на:')
    for i in основное_меню_реверс[статусы[пользователь]['статус']]:
        i = коды[i]
        msg = i
        send_msg(пользователь, msg)