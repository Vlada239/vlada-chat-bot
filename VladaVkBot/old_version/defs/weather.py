from old_version.defs.tools import *

def weather(event, request, userStates):
	town = request
	if check_word_matching(request, {'санкт-петербург', 'спб', 'ленинград', 'петербург', 'питер'}): # тк мы из питера, то разумно разрешить разговорные названия города. С спб работаем отдельно
		town = 'Санкт-Петербург'

	temperature = get_current_temperature(town) # вытаскиваем погоду из нужного сайта
	if temperature == 'Такого города не существует':  # этого города мб и нет, проверяем ответ сайта
		message = f'Я не знаю такого города. Попробуй ввести другой город'
		send_msg(event.user_id, message)
	else:
		sign = 1 if temperature > 0 else 0  # смотрим больше/меньше нуля
		message = f'Погода в городе {town}:\n {"+" * sign}{temperature}\N{DEGREE SIGN}C'  # красиво пишем погоду
		send_msg(event.user_id, message, get_image(town))
		
		userStates[event.user_id] = ['home', 'home']
