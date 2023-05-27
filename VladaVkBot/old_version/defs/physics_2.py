from old_version.defs.tools import *
from random import randint
from vk_api import VkApi

VK_TOKEN = 'a47436d8894f49e81a488838f5ad9d9e56718655410b974ded4d48739f1ac128e19e12209fd8fd1e47b9f'
vk_session = VkApi(token=VK_TOKEN)

def physics_2(event, request, userStates):
	if request == 'термины' :  # режим терминов, всего, где фигурируют определения, и что не билеты
		send_msg(event.user_id,
			'Если ты хочешь проверить свои знания, то набери "ф", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')  # делимся на режимы
		userStates[event.user_id] = ['terms', 'physics_2']

	elif request == 'билеты' :
		'''когда будут билеты нужно будет вынести всё это в отдельную функцию tickets()'''
		vk_session.method('messages.send', {'user_id' : event.user_id, 'random_id' : randint(1e16, 1e18),
										'attachment' : 'photo-196586329_457239129'})

	elif request == 'выход' :
		send_msg(event.user_id, 'Теперь ты в меню.')
		send_msg(event.user_id,
			'Если хочешь узнать погоду в любом из городов мира, напиши слово "погода". Если тебя интересует информация по учебе, напиши "учеба".')
		userStates[event.user_id] = ['home', 'home']

	else :
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима физики, напиши "выход")')
