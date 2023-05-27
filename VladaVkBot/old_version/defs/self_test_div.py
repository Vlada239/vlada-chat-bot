from old_version.defs.tools import *

def self_test_div(event, request, userStates):
	if request == 'самопроверка_1':  # вспоминаем определения чего-либо
		send_msg(event.user_id, 'Чтобы получить термин, напиши "дай".')
		userStates[event.user_id] = ['self_test_1', 'terms']
	elif request == 'самопроверка_2':  # вспоминаем чье определение мы прочитали
		send_msg(event.user_id, 'Чтобы получить определение, напиши "дай".')
		userStates[event.user_id] = ['self_test_2', 'terms']
	elif request == 'выход':  # надоела самопроверка, возвращаемся к терминам
		send_msg(event.user_id, 'Теперь ты в режиме термины.')
		send_msg(event.user_id,
				'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		userStates[event.user_id] = ['terms', 'physics_2']
	else:  # пользователь запутался или пишет чего не надо - предлагаем вернуться к режиму терминов
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки, напиши "выход")')