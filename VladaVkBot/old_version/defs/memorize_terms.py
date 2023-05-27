from old_version.defs.tools import *
from old_version.additional_tools.dictionaries import *

def memorize_terms(event, request, userStates, course):
	if course[event.user_id] == '8':
		dict = terms_8
	elif course[event.user_id] == '9':
		dict = terms_9
	elif course[event.user_id] == '10':
		dict = terms_10
	if request in dict:  # смотрим есть ли у нас это в словаре, если есть, то даем соответсвующее опр-ие
		send_msg(event.user_id, dict[request])
	elif request == 'выход':  # если нам надоест этот переводчик, вернемся к распределению режимов изучения терминов
		send_msg(event.user_id, 'Теперь ты в режиме термины.')
		send_msg(event.user_id,
				'Если ты хочешь проверить свои знания, то набери "ф", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		userStates[event.user_id] = ['terms', 'physics_2']
	else:  # теримна нет в словаре или пользователь запутался - предлагаем выйти из режима, если он просто застрял
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима обучения, напиши "выход")')