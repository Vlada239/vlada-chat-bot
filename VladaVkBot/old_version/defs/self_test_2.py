from old_version.defs.tools import *
from old_version.additional_tools.dictionaries import *
import random

def self_test_2(event, request, userStates, course, term):
	if request == 'дай':
		if course[event.user_id] == '8':
			dict = terms_8
		elif course[event.user_id] == '9':
			dict = terms_9
		elif course[event.user_id] == '10':
			dict = terms_10
		term[event.user_id], definition = random.choice(list(dict.items()))
		send_msg(event.user_id, definition)
		userStates[event.user_id] = ['answer_self_test_2', 'self_test_2']
	elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id,
				'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
		userStates[event.user_id] = ['self_test_div', 'terms']
	else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_2, напиши "выход")')