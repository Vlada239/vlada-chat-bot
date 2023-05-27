from old_version.defs.tools import *

def geometry(event, request, userStates): #этого еще нет, поэтому изивняемся и уходим в меню
	send_msg(event.user_id, 'Извини, геометрии меня ещё не обучили. Может, спросишь что-нибудь ещё?')
	userStates[event.user_id] = ['home', 'home']
