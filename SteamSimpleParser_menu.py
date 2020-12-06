"""
Эта программа написана для определения стоимости некоторых вещей из торговой площадки Steam по минимальной рыночной цене продажи предмета.

Для добавления интересующих вас предметов следуйте аналогии: ['Название предмета (как вам угодно)', 'его индивидуальная ссылка на ТП Steam', 'Количество (обязательно укажите!)', 'Цена закупки']
После, внесите этот список параметров в список списков 'urls'

Обратите внимание, что если вы хотите добавить вещь из другой игры (текущая программа для CS-GO 'appid=730') вам необходимо указать номер игры в переменной 'appid'!
Программа предусмотрена для работы с одним appid в текущий момент!

Обратите внимание, что маркет определяет комиссию для каждой игры отдельно (комиссия игры + площадки Steam). На примере CS-GO комиссия указана в переменной 'comission'!

Также, обратите внимание, что при слишком частых запросах с одного IP, STEAM их блокирует, поэтому если программу часто лишают доступа, уменьшите список вещей или подождите!
"""
import json, time, requests
import random
from prettytable import PrettyTable



urls1 = [
['2018-Boston-Returning', 'Boston%202018%20Returning%20Challengers%20Autograph%20Capsule', 29, 8.11], 
['2019-Katowice-Legends', 'Katowice%202019%20Legends%20Autograph%20Capsule', 3, 6],
['2019-Katowice-Returning', 'Katowice%202019%20Returning%20Challengers%20Autograph%20Capsule', 2, 6],
['2019-Katowice-Minor', 'Katowice%202019%20Minor%20Challengers%20Autograph%20Capsule', 1, 6],
['2019-Berlin-Legends', 'Berlin%202019%20Legends%20Autograph%20Capsule', 30, 6],
['2019-Berlin-Returning', 'Berlin%202019%20Returning%20Challengers%20Autograph%20Capsule', 13, 6],
]

urls2 = [
['\'The Doctor\' Romanov', '%27The%20Doctor%27%20Romanov%20%7C%20Sabre', 4, 115], 
['3rd Commando Company', '3rd%20Commando%20Company%20%7C%20KSK', 1, 58], 
['Seal Team 6 Soldier', 'Seal%20Team%206%20Soldier%20%7C%20NSWC%20SEAL', 2, 44], 
['Slingshot', 'Slingshot%20%7C%20Phoenix', 2, 15.40], 
['Prof. Shahmat', 'Prof.%20Shahmat%20%7C%20Elite%20Crew', 3, 15.25],
['Osiris', 'Osiris%20%7C%20Elite%20Crew', 2, 12.26],
['Ground Rebel', 'Ground%20Rebel%20%20%7C%20Elite%20Crew', 7, 9],
['Soldier', 'Soldier%20%7C%20Phoenix', 5, 9.40],
]

urls3 = [
['Sticker Combine Helmet', 'Sticker%20%7C%20Combine%20Helmet', 35, 6],
['Sticker Holo Combine Helmet', 'Sticker%20%7C%20Combine%20Helmet%20%28Holo%29', 3, 20.33],
]

urls4 = [
['P250 X-RAY', 'P250%20%7C%20X-Ray%20%28Factory%20New%29', 1, 13.62],
['USP FlashBack', 'USP-S%20%7C%20Flashback%20%28Factory%20New%29', 1, 33.23],
['USP Cyrex', 'USP-S%20%7C%20Cyrex%20%28Minimal%20Wear%29', 1, 58.94],
['AWP Phobos', 'AWP%20%7C%20Phobos%20%28Factory%20New%29', 1, 48],
]

x = PrettyTable()
x.field_names = ['Название предмета', 'Кол-во', 'Покупка', 'Текущая', 'Прибыль ед.', 'Сумма', 'Прибыль']

def main(urls):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

	appid = 730
	comission = 0.869584416
	overall = 0
	payed = 0
	try:
		c=0
		curr=0
		for i in urls:
			try:
				r = requests.get(f'http://steamcommunity.com/market/priceoverview/?market_hash_name={i[1]}&appid={appid}&currency=18', headers=headers)
				variable = json.loads(r.text)

				price = round((float(variable['lowest_price'].strip('₴\u20b4').replace(',', '.'))*comission), 2)
				overall += price*i[2]
				payed += i[2]*i[3]

				x.add_row([i[0], i[2], i[3], price, round(price - i[3], 2), round(i[2]*price, 2), round((i[2]*price)-(i[2]*i[3]), 2)])

				time.sleep(random.randint(5, 10))
			except KeyError:
				print('Проверены не все предметы, т.к. стим не дает доступ в связи со слишком частыми запросами!\n')
				break
			while c < 1:
				r = requests.get(f'http://steamcommunity.com/market/priceoverview/?market_hash_name={i[1]}&appid={appid}&currency=1', headers=headers)
				variable = json.loads(r.text)
				price_usd = round((float(variable['lowest_price'].strip('$'))*comission), 2)
				curr += (price/price_usd)
				c += 1

		print(x)
		print(f'\n Цена всех предметов с вычетом комиссии Steam: ₴{round(overall, 2)} или ${round((overall/curr), 2)}\n')
		print(f' Потрачено суммарно на закупку: ₴{round(payed, 2)} или ${round((payed/curr), 2)}')
		print(f' Чистая прибыль с вычетом комиссии Steam: ₴{round(overall-payed, 2)} или ${round(((overall-payed)/curr), 2)}')
		print(f' Коеффициент приумножения капитала: X{round(overall/payed, 2)}')
		print(f' Внутренний курс доллара: ₴{round(curr, 2)}')
		input('\n Нажмите ENTER чтобы выйти!')

	except TypeError:
		input('Steam отказал в доступе программе!')
	except BaseException:
		input('Отсутсвует интернет!')

def sub():
	a = input('Выбор группы предметов: \n  1. Капсулы \n  2. Агенты \n  3. Стикеры \n  4. Стволы последние \n  5. Все вместе \n Введите номер группы: ')
	if int(a) == 1:
		main(urls1)
	elif int(a) == 2:
		main(urls2)
	elif int(a) == 3:
		main(urls3)
	elif int(a) == 4:
		main(urls4)
	elif int(a) == 5:
		main((urls1 + urls2 + urls3 + urls4))
	else:
		print('\nНеверно задан номер группы!\n')
		sub()

sub()