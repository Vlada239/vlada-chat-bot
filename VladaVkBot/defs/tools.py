from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll
from random import randint
from dicts.dictionaries import *
from dicts.dictionaries import основное_меню

VK_TOKEN = 'a47436d8894f49e81a488838f5ad9d9e56718655410b974ded4d48739f1ac128e19e12209fd8fd1e47b9f'
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)


def send_msg(user_id, text):
		vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': randint(1e16, 1e18)})


def начало(элемент):
	if элемент in основное_меню.keys():
		return False
	else:
		return True


def конец(элемент):
	if элемент in основное_меню_реверс.keys():
		return False
	else:
		return True


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