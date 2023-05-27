from old_version.defs.tools import *

def terms(event, request, userStates):
	if request == 'ф':  # обучающие режимы, переходим в соответсвующие функции
		send_msg(event.user_id,
				'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
		userStates[event.user_id] = ['self_test_div', 'terms']
	elif request == 'обучение':  # по сути переводчик
		send_msg(event.user_id, 'Введи термин.')
		userStates[event.user_id] = ['memorize_terms', 'terms']
	elif request == 'словарь':  # если хотим просто посмотреть все термины - ссылка на диск. (Там можно оставить коммент)
		send_msg(event.user_id, 'https://drive.google.com/file/d/1_pjDINbaJFo2Tt5ONqNSWj7OJvwg28hV/view?usp=sharing')
	elif request == 'выход':  # нам надоели термины, хотим билеты/ выйти вообще
		send_msg(event.user_id, 'Теперь ты в режиме физики.')
		send_msg(event.user_id,
				'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
		userStates[event.user_id] = ['physics_2', 'physics']
	else:  # больше мы ничего не ожидаем, предлагаем выйти из режима, если человек просто застрял
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима термины, напиши "выход")')