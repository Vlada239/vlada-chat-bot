from old_version.defs.tools import *
import random

def answer_self_test_2(event, request, userStates, term):
	arr_right = ['photo-196586329_457239131', 'photo-196586329_457239130']
	arr_wrong = ['photo-196586329_457239133', 'photo-196586329_457239132']
	if request == term[event.user_id]:  # нам ответили правильно
		send_msg(event.user_id, 'умничка')
		picture = random.choice(arr_right)  # отправляем картинку с рандомным довольным котом, выбирая ссылку из словаря с ссылками
		vk_session.method('messages.send',
						{'user_id': event.user_id, 'random_id': randint(1e16, 1e18), 'attachment': picture})
		send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
		userStates[event.user_id] = ['self_test_2', 'self_test_div']
	else:
		send_msg(event.user_id, 'неверно')
		picture = random.choice(arr_wrong)  # отправляем картинку с недовольным котом, выбирая ссылку из словаря с ссылками
		vk_session.method('messages.send',
						{'user_id': event.user_id, 'random_id': randint(1e16, 1e18), 'attachment': picture})
		send_msg(event.user_id, f"правильный ответ: {term[event.user_id]}")
		send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
		userStates[event.user_id] = ['self_test_2', 'self_test_div']