from old_version.defs.tools import *
import random
from old_version.additional_tools.dictionaries import *

def self_test_1(event, request, userStates, course, definition):
	if request == 'дай':
		if course[event.user_id] == '8':
			dict = terms_8
		elif course[event.user_id] == '9':
			dict = terms_9
		elif course[event.user_id] == '10':
			dict = terms_10
		term, definition[event.user_id] = random.choice(list(dict.items()))
		send_msg(event.user_id, term)
		send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
		userStates[event.user_id] = ['answer_self_test_1', 'self_test_1']
	elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id,
				'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')  # самопроверка_1 = вспомни определение; самопроверка_2 = узнай термин
		userStates[event.user_id] = ['self_test_div', 'terms']
	else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_1, напиши "выход")')