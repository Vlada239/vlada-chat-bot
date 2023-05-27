from old_version.defs.tools import *

def home(event, request, userStates):
	if check_word_matching(request, {'привет', 'начать', 'хай', 'здравствуй', 'хаюшки'}): #приветствие
		name = get_user_name(event.user_id)
		'''надо бы имена поменять на наши id'''
		if name == 'Ян' or name == 'Yan':
			send_msg(event.user_id, 'Повинуюсь, создатель')
		elif name == 'Влада' or name == 'Vlada':
			send_msg(event.user_id, 'Повинуюсь, создательница')
		elif name == 'Соня' or name == 'Sonya':
			send_msg(event.user_id, 'Чего изволитъ желать прекрасная дама?')
		else:
			send_msg(event.user_id, f'Привет, {name}!')
		send_msg(event.user_id, 'Если хочешь узнать погоду в любом из городов мира, напиши "погода". Если тебя интересует информация по учебе, напиши "учеба".')

	elif check_word_matching(request, {'пока', 'хватит'}): #на случай очень вежливого пользователя
		send_msg(event.user_id, 'Пока!')

	elif check_word_matching(request, {'погода'}): #переходим в функцию определения погоды
		send_msg(event.user_id, 'Введи название города.')
		userStates[event.user_id] = ['weather', 'home']

	elif check_word_matching(request, {'учёба', 'учиться', 'обучение'}):  # даём пояснения по делению на учебные предметы
		send_msg(event.user_id, 'Напиши номер предмета, по которому хочешь получить информацию:')
		send_msg(event.user_id, '(Я шар в физике, геометрии и литературе)')

	elif check_word_matching(request, {'физика', 'физон'}):  # делим физику на классы
		send_msg(event.user_id, 'Напиши, по какому классу ты хочешь получить информацию.')
		userStates[event.user_id] = ['physics', 'home']

	elif check_word_matching(request, {'геометрия', 'геомка', 'математика', 'матеша'}):  # уходим в геометрию
		userStates[event.user_id] = ['geometry', 'home']

	elif check_word_matching(request, {'литература', 'литра'}):  # уходим в литру
		userStates[event.user_id] = ['literature', 'home']

	else:
		send_msg(event.user_id, 'Извини, этому меня ещё не обучили. Может, спросишь что-нибудь ещё?')  # защита от невнимательных
