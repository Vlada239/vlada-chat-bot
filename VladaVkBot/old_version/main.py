from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from old_version.defs.home import *
from old_version.defs.weather import *
from old_version.defs.physics import *
from old_version.defs.literature import *
from old_version.defs.geometry import *
from old_version.defs.physics_2 import *
from old_version.defs.terms import *
from old_version.defs.memorize_terms import *
from old_version.defs.self_test_div import *
from old_version.defs.self_test_1 import *
from old_version.defs.self_test_2 import *
from old_version.defs.answer_self_test_1 import *
from old_version.defs.answer_self_test_2 import *
VK_TOKEN = 'a47436d8894f49e81a488838f5ad9d9e56718655410b974ded4d48739f1ac128e19e12209fd8fd1e47b9f'
API_KEY = 'e769f0fe046f901526994f29b5bc6f8e'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)
userStates = {}
course = {}
term = {}
definition = {}


for event in longpoll.listen(): #слушаем собеседника
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:

		if not (event.user_id in userStates):
			userStates[event.user_id] = ['home', 'home']

		request = event.text.lower() #пихаем ответ в переменную и отделываемся от регистра

		if userStates[event.user_id][0] == 'home':
			home(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'weather':
			weather(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'physics': #делим на классы
			physics(event, request, userStates, course)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'geometry':
			geometry(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'literature':
			literature(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'physics_2': #делим на термины и билеты
			physics_2(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'terms': #делим термины на самопроверку, обучение и словарь
			terms(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'memorize_terms':
			memorize_terms(event, request, userStates, course)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'self_test_div': #делим на режимы самопроверки
			self_test_div(event, request, userStates)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'self_test_1':
			self_test_1(event, request, userStates, course, definition)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'self_test_2':
			self_test_2(event, request, userStates, course, term)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'answer_self_test_1':
			answer_self_test_1(event, request, userStates, definition)
			print(request, userStates)
		elif userStates[event.user_id][0] == 'answer_self_test_2':
			answer_self_test_2(event, request, userStates, term)
			print(request, userStates)