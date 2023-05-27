file = open("terms_8.txt")
on_string = file.read().split("\n")[:-1]
dict_fin = dict(путь="длина траектории", траектория="воображаемая линия, вдоль которой движется тело")

for item in on_string:
	key = item.split(" - ")[0]
	value = item.split(" - ")[1:]
	if value != "пока хз":
		dict_fin[key] = value

file.close()
print(dict_fin)