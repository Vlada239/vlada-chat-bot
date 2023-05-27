from old_version.defs.tools import *

def literature(event, request, userStates): #этого еще нет, поэтому изивняемся и уходим в меню
	send_msg(event.user_id, 'Извини, литературе меня ещё не обучили. Может, спросишь что-нибудь ещё?')
	userStates[event.user_id] = ['home', 'home']
