from old_version.defs.tools import *

def physics(event, request, userStates, course): #делим физику на классы
	if request == '10' or request == '9' or request == '8':
		send_msg(event.user_id,
			'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
		course[event.user_id] = request
		userStates[event.user_id] = ['physics_2', 'physics']
	else :
		send_msg(event.user_id, 'Извини, я не знаю такого класса.')  # отнекиваемся от всего остального и идём в меню
		userStates[event.user_id] = ['home', 'home']
