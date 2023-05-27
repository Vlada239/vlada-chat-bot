#начинать читать снизу (после слов начало (меню)), дальше можно подниматься и смотреть непонятные функции.
from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from bs4 import BeautifulSoup
import bs4
import requests
import random
 
 
VK_TOKEN = '***'
API_KEY = '***'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)
 
 
def get_current_temperature(town): #вытаскиваем температуру города с сайта, если 404, то возвращаем строку, что города нет
	params = {'q':town, 'appid':API_KEY, 'units':'metric', 'mode':'json'}
	r = requests.get(WEATHER_URL, params)
	if r.status_code == 404:
	  return 'Такого города не существует'
	data = r.json()
	return data['main']['temp']
 
 
def send_msg(user_id, text):  # https://vk.com/dev/messages.send
	vk_session.method('messages.send', {'user_id': user_id, 'message': text,
								'random_id':randint(1e16, 1e18)})
   
def get_user_name(user_id): # https://vk.com/dev/users.get
	r = vk_session.method('users.get', {'v':'5.71', 'access_token' : VK_TOKEN, 'user_ids' : user_id})
	return r[0]['first_name']
 
 
def extract_image_url(town): #формируем ссылку на картинку (города) из википедии
	url = 'https://ru.wikipedia.org/wiki/'
	r = requests.get(url + town)
	soup = BeautifulSoup(r.text, 'lxml')
	body = soup.find(id='bodyContent')
	img = body.find('img')
	path = 'https:' + img['src']
	return path
 
 
def send_image(user_id, town): #упрощаем отправку картинок по ссылке, получаемой функцией выше
	attachments = []
	image_url = extract_image_url(town)
	image = requests.get(image_url, stream=True)
	photo = upload.photo_messages(photos=image.raw)[0]
	print(image.raw)
	attachments.append(
		'photo{}_{}'.format(photo['owner_id'], photo['id'])
	)
	vk_session.method('messages.send',{
		'user_id':user_id,
		'attachment':','.join(attachments),'random_id':randint(1e16, 1e18)
	})
 
 
def самопроверка_8(): #см самопрверка_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'самопроверка_1':
		send_msg(event.user_id, 'Чтобы получить термин, напиши "дай".')
		самопроверка_1_8()
	  elif request == 'самопроверка_2':
		send_msg(event.user_id, 'Чтобы получить определение, напиши "дай".')
		самопроверка_2_8()
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме термины.')
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки, напиши "выход")')
 
 
def самопроверка_9(): #см самопрверка_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'самопроверка_1':
		send_msg(event.user_id, 'Чтобы получить термин, напиши "дай".')
		самопроверка_1_9()
	  elif request == 'самопроверка_2':
		send_msg(event.user_id, 'Чтобы получить определение, напиши "дай".')
		самопроверка_2_9()
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме термины.')
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки, напиши "выход")')
 
 
def самопроверка_10(): #деление на варианты самопрверки
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower() #слушаем
	  if request == 'самопроверка_1': #вспоминаем определения чего-либо
		send_msg(event.user_id, 'Чтобы получить термин, напиши "дай".')
		самопроверка_1_10()
	  elif request == 'самопроверка_2': #вспоминаем чье определение мы прочитали
		send_msg(event.user_id, 'Чтобы получить определение, напиши "дай".')
		самопроверка_2_10()
	  elif request == 'выход': #надоела самопроверка, возвращаемся к терминам
		send_msg(event.user_id, 'Теперь ты в режиме термины.')
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		break
	  else: #польозователь запутался или пишет чего не надо - предлагаем вернуться к режиму терминов
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки, напиши "выход")')
 
 
def самопроверка_2_9(): #см самопрверка_2_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай':
		термин, определение = random.choice(list(определения_физика_9.items()))
		send_msg(event.user_id, определение)
		for event in longpoll.listen():
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == термин:
			  send_msg(event.user_id, 'умничка')
			  картинка = random.choice(умничка)
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
			else:
			  send_msg(event.user_id, 'неверно')
			  картинка = random.choice(не_умничка)
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, f"правильный ответ: {термин}")
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_2, напиши "выход")')
 
 
def самопроверка_1_9(): #см самопрверка_1_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай':
		термин, определение = random.choice(list(определения_физика_9.items()))
		send_msg(event.user_id, термин)
		send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
		for event in longpoll.listen():
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == 'ответ':
			  send_msg(event.user_id, определение)
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
			else:
			  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
			  send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"') #самопроверка_1 = вспомни определение; самопроверка_2 = узнай термин
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_1, напиши "выход")')
 
 
def самопроверка_2_8(): #см самопрверка_2_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай':
		термин, определение = random.choice(list(определения_физика_8.items()))
		send_msg(event.user_id, определение)
		for event in longpoll.listen():
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == термин:
			  send_msg(event.user_id, 'умничка')
			  картинка = random.choice(умничка)
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
			else:
			  send_msg(event.user_id, 'неверно')
			  картинка = random.choice(не_умничка)
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, f"правильный ответ: {термин}")
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_2, напиши "выход")')
 
 
def самопроверка_1_8(): #см самопрверка_1_10
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай':
		термин, определение = random.choice(list(определения_физика_8.items()))
		send_msg(event.user_id, термин)
		send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
		for event in longpoll.listen():
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == 'ответ':
			  send_msg(event.user_id, определение)
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break
			else:
			  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
			  send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"') #самопроверка_1 = вспомни определение; самопроверка_2 = узнай термин
		break
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_1, напиши "выход")')
 
 
def самопроверка_2_10(): #пользователь получает определение, он должен написать определение чего он только что прочитал
  for event in longpoll.listen(): #слушаем
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай': #человек просит его спросить
		термин, определение = random.choice(list(определения_физика_10.items())) #рандомайзер выбирает определение из словаря и запоминает его термин (название физ. объекта/явления итд) в переменную
		send_msg(event.user_id, определение)
		for event in longpoll.listen(): #слушаем
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == термин: #нам ответили правильно
			  send_msg(event.user_id, 'умничка')
			  картинка = random.choice(умничка) #отправляем картинку с рандомным довольным котом, выбирая ссылку из словаря с ссылками
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break #возвращаемся к началу функции и слушаем
			else:
			  send_msg(event.user_id, 'неверно')
			  картинка = random.choice(не_умничка)  #отправляем картинку с недовольным котом, выбирая ссылку из словаря с ссылками
			  vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': картинка})
			  send_msg(event.user_id, f"правильный ответ: {термин}")
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break #возвращаемся к началу функции и слушаем
	  elif request == 'выход': #надоело вспоминать теримны, идем к делению на варианты самопроверки
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
		break #возвращаемся к делению на варианты самопроверки
	  else: #нам написали хрень или пользователь просто запутался - предлагаем выйти из режима
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_2, напиши "выход")')
 
 
def самопроверка_1_10(): #человек получает рандомный термин (путь,масса итп), про себя проговаривает, по команде "ответ" получает опр-е
  for event in longpoll.listen(): #слушаем
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'дай': #пользователь просит его спросить
		термин, определение = random.choice(list(определения_физика_10.items())) #рандомайзер выбирает термин (название физ. объекта/явления итд) из словаря и запоминает его определение в переменную
		send_msg(event.user_id, термин)
		send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".') #поясняем что делать
		for event in longpoll.listen(): #ждем ответа от человека
		 if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == 'ответ': #он написал единственную ожидаемую от него команду - выводим ответ
			  send_msg(event.user_id, определение)
			  send_msg(event.user_id, 'Чтобы получить следующий термин, напиши "дай".')
			  break #возвращаемся к началу этой функции (ждем "дай")
			else: #защита от невнимательных
			  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
			  send_msg(event.user_id, 'Если хочешь прочитать правильное определение, напиши "ответ".')
	  elif request == 'выход': #надоело вспоминать определения, идем к делению на варианты самопроверки
		send_msg(event.user_id, 'Теперь ты в режиме самопроверки.')
		send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"') #самопроверка_1 = вспомни определение; самопроверка_2 = узнай термин
		break
	  else: #нам написали хрень или пользователь просто запутался - предлагаем выйти из режима
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима самопроверки_1, напиши "выход")')
 
 
def physics_10():
 for event in longpoll.listen(): #слушаем человека
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'термины':  #режим терминов, всего, где фигурируют определения, и что не билеты
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')  #делимся на режимы
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:  #слушаем человека
			  request = event.text.lower()
			  if request == 'самопроверка':  #обучающие режимы, переходим в соответсвующие функции
				send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
				самопроверка_10()
			  elif request == 'обучение':  #по сути переводчик
				send_msg(event.user_id, 'Введи термин.')
				for event in longpoll.listen():
				  if event.type == VkEventType.MESSAGE_NEW and event.to_me:  #слушаем человека
					request = event.text.lower()
					термин = request
					if термин in определения_физика_10:  #смотрим есть ли у нас это в словаре, если есть, то даем соответсвующее опр-ие
					  send_msg(event.user_id, определения_физика_10[термин])
					elif термин == 'выход':  #если нам надоест этот переводчик, вернемся к распределению режимов изучения терминов
					  send_msg(event.user_id, 'Теперь ты в режиме термины.')
					  send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
					  break
					else:  #теримна нет в словаре или пользователь запутался - предлагаем выйти из режима, если он просто застрял
					  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
					  send_msg(event.user_id, '(Если хочешь выйти из режима обучения, напиши "выход")')
			  elif request == 'словарь':  #если хотим просто посмотреть все термины - ссылка на диск. (Там можно оставить коммент)
				send_msg(event.user_id, 'https://drive.google.com/file/d/1_pjDINbaJFo2Tt5ONqNSWj7OJvwg28hV/view?usp=sharing')
			  elif request == 'выход':  #нам надоели термины, хотим билеты/ выйти вообще
				send_msg(event.user_id, 'Теперь ты в режиме физики.')
				send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
				break  #возвращаемся к физике (делению на термины/билеты)
			  else:  #больше мы ничего не ожидаем, предлагаем выйти из режима, если человек просто застрял
				send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
				send_msg(event.user_id, '(Если хочешь выйти из режима термины, напиши "выход")')
 
	  elif request == 'билеты':
		vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': 'photo-196586329_457239129'})
 
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в меню.')
		send_msg(event.user_id, 'Если хочешь узнать погоду в любом из городов мира, напиши слово "погода". Если тебя интересует информация по учебе, напиши "учеба".')
		break
 
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима физики, напиши "выход")')
 
 
 
def physics_9(): #см комментарии к физика_10, тут пока все аналогично
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'термины':
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			  request = event.text.lower()
			  if request == 'самопроверка':
				send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
				самопроверка_9()
			  elif request == 'обучение':
				send_msg(event.user_id, 'Введи термин.')
				for event in longpoll.listen():
				  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
					request = event.text.lower()
					термин = request
					if термин in определения_физика_9:
					  send_msg(event.user_id, определения_физика_9[термин])
					elif термин == 'выход':
					  send_msg(event.user_id, 'Теперь ты в режиме термины.')
					  send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
					  break
					else:
					  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
					  send_msg(event.user_id, '(Если хочешь выйти из режима обучения, напиши "выход")')
			  elif request == 'словарь':
				send_msg(event.user_id, 'пока нету')
			  elif request == 'выход':
				send_msg(event.user_id, 'Теперь ты в режиме физики.')
				send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
				break
			  else:
				send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
				send_msg(event.user_id, '(Если хочешь выйти из режима термины, напиши "выход")')
 
	  elif request == 'билеты':
		vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': 'photo-196586329_457239129'})
 
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в меню.')
		send_msg(event.user_id, 'Если хочешь узнать погоду в любом из городов мира, напиши слово "погода". Если тебя интересует информация по учебе, напиши "учеба".')
		break
 
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима физики, напиши "выход")')
 
 
def physics_8(): #см комментарии к физика_10, тут пока все аналогично
  for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  if request == 'термины':
		send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			  request = event.text.lower()
			  if request == 'самопроверка':
				send_msg(event.user_id, 'Если хочешь самостоятельно проверить свои знания, введи "самопроверка_1", а если хочешь определять термин по его определению, то "самопроверка_2"')
				самопроверка_9()
			  elif request == 'обучение':
				send_msg(event.user_id, 'Введи термин.')
				for event in longpoll.listen():
				  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
					request = event.text.lower()
					термин = request
					if термин in определения_физика_8:
					  send_msg(event.user_id, определения_физика_8[термин])
					elif термин == 'выход':
					  send_msg(event.user_id, 'Теперь ты в режиме термины.')
					  send_msg(event.user_id, 'Если ты хочешь проверить свои знания, то набери "самопроверка", а если повторить определения, то "обучение". Также, если ты хочешь увидеть полный список терминов с их определениями, напиши "словарь".')
					  break
					else:
					  send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
					  send_msg(event.user_id, '(Если хочешь выйти из режима обучения, напиши "выход")')
			  elif request == 'словарь':
				send_msg(event.user_id, 'пока нету')
			  elif request == 'выход':
				send_msg(event.user_id, 'Теперь ты в режиме физики.')
				send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
				break
			  else:
				send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
				send_msg(event.user_id, '(Если хочешь выйти из режима термины, напиши "выход")')
 
	  elif request == 'билеты':
		vk_session.method('messages.send', {'user_id': event.user_id,'random_id': randint(1e16, 1e18), 'attachment': 'photo-196586329_457239129'})
 
	  elif request == 'выход':
		send_msg(event.user_id, 'Теперь ты в меню.')
		send_msg(event.user_id, 'Если хочешь узнать погоду в любом из городов мира, напиши слово "погода". Если тебя интересует информация по учебе, напиши "учеба".')
		break
 
	  else:
		send_msg(event.user_id, 'Извини, этого я пока не знаю. Может, спросишь что-нибудь ещё?')
		send_msg(event.user_id, '(Если хочешь выйти из режима физики, напиши "выход")')
 
 
def literature(): #этого еще нет, поэтому изивняемся и уходим в меню
  send_msg(event.user_id, 'Извини, литературе меня ещё не обучили. Может, спросишь что-нибудь ещё?')
 
 
def geometry(): #этого еще нет, поэтому изивняемся и уходим в меню
  send_msg(event.user_id, 'Извини, геометрии меня ещё не обучили. Может, спросишь что-нибудь ещё?')
 
 
def погода(): #работаем с погодой
  for event in longpoll.listen(): #слушаем собеседника
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower()
	  town = request
	  if town == 'санкт-петербург' or town == 'санкт петербург' or town == 'питер' or town == 'ленинград' or town == 'спб':
		#тк мы из питера, то разумно разрешить разговорные названия города. С спб работаем отдельно
		town1 = 'петербург'
		temperature = get_current_temperature('санкт-петербург') #вытаскиваем погоду из нужного сайта
		sign = 1 if temperature > 0 else 0 #смотрим больше-меньше нуля
		message = f'Погода в городе {town}:\n {"+"*sign}{temperature}\N{DEGREE SIGN}C' #красиво пишем погоду
		send_msg(event.user_id, message)
		send_image(event.user_id, town1) #берем из википедии картинку
		break #уходим в меню
 
	  else: #если это не питер
		temperature = get_current_temperature(town)
		if temperature == 'Такого города не существует': #тк это не питер, этого города мб и нет, проверяем ответ сайта
		  message = f'Я не знаю такого города. Попробуй ввести другой город'
		  send_msg(event.user_id, message)
		else:
		  sign = 1 if temperature > 0 else 0 #если есть, аналогично предыдущему
		  message = f'Погода в городе {town.title()}:\n {"+"*sign}{temperature}\N{DEGREE SIGN}C'
		  send_msg(event.user_id, message)
		  send_image(event.user_id, town)
		  break #уходим в меню
 
														 #НАЧАЛО (МЕНЮ)
 
for event in longpoll.listen(): #слушаем собеседника
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
	  request = event.text.lower() #пихаем ответ в переменную и отделываемся от регистра
	  if request == 'привет' or request == 'начать': #приветствие
		  name = get_user_name(event.user_id)
		  send_msg(event.user_id, f'Привет, {name}!')
		  send_msg(event.user_id, 'Если хочешь узнать погоду в любом из городов мира, напиши слово "погода". Если тебя интересует информация по учебе, напиши "учеба".')

	  elif request == 'пока': #на случай очень вежливого пользователя
		send_msg(event.user_id, 'Пока!')

	  elif request == 'погода': #переходим в функцию определения погоды
		send_msg(event.user_id, 'Введи название города.')
		погода()
 
	  elif 'учеба' in request: #даём пояснения по делению на учебные предметы
		send_msg(event.user_id, 'Напиши номер предмета, по которому хочешь получить информацию:')
		send_msg(event.user_id, '1 - физика')
		send_msg(event.user_id, '2 - геометрия')
		send_msg(event.user_id, '3 - литература ')
 
	  elif request == '1': #делим физику на классы
		send_msg(event.user_id, 'Напиши, по какому классу ты хочешь получить информацию.')
		for event in longpoll.listen():
		  if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			request = event.text.lower()
			if request == '10': #переход в физика_10
			  send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
			  physics_10()
			  break #после окончания работы в физика_10 возвращаемся в меню
			elif request == '9':
			  send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
			  physics_9()
			  break
			elif request == '8':
			  send_msg(event.user_id, 'Если ты хочешь повторить определения, напиши "термины", если хочешь учить билеты, то введи "билеты".')
			  physics_8()
			  break
			else:
			  send_msg(event.user_id, 'Извини, я не знаю такого класса.') #отнекиваемся от всего остального и идём в меню
 
 
	  elif request == '2': #уходим в геометрию
		geometry()
 
	  elif request == '3': #уходим в литру
		literature()
 
	  else:
		send_msg(event.user_id, 'Извини, этому меня ещё не обучили. Может, спросишь что-нибудь ещё?') #защита от невнимательных
