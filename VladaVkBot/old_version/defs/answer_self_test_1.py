from old_version.defs.tools import *

def answer_self_test_1(event, request, userStates, definition):
	if request == 'ответ':
		send_msg(event.user_id, definition[event.user_id])
		send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
		userStates[event.user_id] = ['self_test_1', 'self_test_div']
	else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')