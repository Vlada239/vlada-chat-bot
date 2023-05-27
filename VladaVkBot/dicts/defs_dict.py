from dicts.dictionaries import *


def коды_создание():
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\меню_стандарт.txt", "r", encoding='utf-8')
    коды = {'0': 'меню'}
    onstring = file.read().split("\n")
    i = 1
    for item in onstring:
        first = item.split(" $&$ ")[0].strip()
        коды[str(i)] = first
        i += 1
    return коды


def основное_меню():
    коды = коды_создание()
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\меню_стандарт.txt", "r", encoding='utf-8')
    основное_меню = {}
    onstring = file.read().split("\n")
    j = 1

    def get_key(d, value, граница):
        i = 0
        j = 0
        for k, v in d.items():
            if v == value:
                j = i
                i = k
                if int(i) >= граница:
                    return str(j)
        return str(i)

    for item in onstring:
        second = item.split(" $&$ ")[1].strip()
        word = get_key(коды, second, j)
        основное_меню[str(j)] = word
        j += 1
    return основное_меню


def словарь_литература():
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\словарь_литература.txt", "r", encoding='utf-8')
    onstring = file.read().split("\n")
    slov = {}
    for item in onstring:
        key = item.split(" $&$ ")[0].lower()
        value = item.split(" $&$ ")[1:]
        slov[key] = value
    file.close()
    return slov


def история_8_даты():
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\словарь_история_8_даты.txt", "r", encoding='utf-8')
    onstring = file.read().split("\n")
    slov = {}
    for item in onstring:
        key = item.split(" $&$ ")[0].lower()
        value = item.split(" $&$ ")[1:]
        slov[key] = value
    file.close()
    return slov


def история_9_даты():
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\словарь_история_9_даты.txt", "r", encoding='utf-8')
    onstring = file.read().split("\n")
    slov = {}
    for item in onstring:
        key = item.split(" $&$ ")[0].lower()
        value = item.split(" $&$ ")[1:]
        slov[key] = value
    file.close()
    return slov

def физика_термины_10():
    file = open(r"C:\Users\Fml23\OneDrive\Документы\GitHub\SonjaVkBot\files\словарь_физика_10.txt", "r", encoding='utf-8')
    onstring = file.read().split("\n")
    slov = {}
    for item in onstring:
        key = item.split(" $&$ ")[0].lower()
        value = item.split(" $&$ ")[1:]
        slov[key] = value
    file.close()
    return slov


def reverse(dict):
    dict2 = {}
    for k, v in dict.items():
        dict2[v] = dict2.get(v, [])
        dict2[v].append(k)
    return dict2
