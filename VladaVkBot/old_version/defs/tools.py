from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from random import randint
from bs4 import BeautifulSoup

VK_TOKEN = 'a47436d8894f49e81a488838f5ad9d9e56718655410b974ded4d48739f1ac128e19e12209fd8fd1e47b9f'
API_KEY = 'e769f0fe046f901526994f29b5bc6f8e'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)

def lev_distance(a, b): #Calculates the Levenshtein distance between a and b
	n, m = len(a), len(b)
	if n > m:
		# Make sure n <= m, to use O(min(n, m)) space
		a, b = b, a
		n, m = m, n

	current_row = range(n + 1)  # Keep current and previous row, not entire matrix
	for i in range(1, m + 1):
		previous_row, current_row = current_row, [i] + [0] * n
		for j in range(1, n + 1):
			add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
			if a[j - 1] != b[i - 1]:
				change += 1
			current_row[j] = min(add, delete, change)

	return current_row[n]

def check_word_matching(word, keys, maxL = 2): # checking words matching by Levenshtein distance
	for key in keys:
		if lev_distance(word, key) <= maxL:
			return True

	return False

def get_user_name(user_id): # https://vk.com/dev/users.get
	r = vk_session.method('users.get', {'v':'5.71', 'access_token' : VK_TOKEN, 'user_ids' : user_id})
	return r[0]['first_name']

def get_current_temperature(town): # вытаскиваем температуру города с сайта, если 404, то возвращаем строку, что города нет
	params = {'q':town, 'appid':API_KEY, 'units':'metric', 'mode':'json'}
	r = requests.get(WEATHER_URL, params)
	if r.status_code == 404:
		return 'Такого города не существует'
	data = r.json()
	return data['main']['temp']

def extract_image_url(town): # формируем ссылку на картинку (города) из википедии
	url = 'https://ru.wikipedia.org/wiki/'
	r = requests.get(url + town)
	soup = BeautifulSoup(r.text, 'lxml')
	body = soup.find(id='bodyContent')
	img = body.find('img')
	path = 'https:' + img['src']
	return path

def get_image(url):
	image_url = extract_image_url(url)
	image = requests.get(image_url, stream=True)
	photo = upload.photo_messages(photos=image.raw)[0]
	attachments = []
	attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

	return attachments;

def send_msg(user_id, text, attachments = ''):  # https://vk.com/dev/messages.send
	vk_session.method('messages.send', {
		'user_id': user_id, 
		'message': text,
		'attachment':','.join(attachments),
		'random_id':randint(1e16, 1e18)
	})

def send_image_by_url(user_id, url): # упрощаем отправку картинок по ссылке, получаемой функцией extract_image_url
	send_msg(user_id, '', get_image(url))

