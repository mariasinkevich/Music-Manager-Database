import sqlite3 as sq
from sqlite3 import Error
import time
import hashlib


def start_dialogue (curs):
	print ("Добро пожаловать в менеджер музыкальных групп!")
	print ("Кем вы являетесь?")
	print ("1 - Администратор")
	print ("2 - Менеджер")
	a = int(input())
	if a==1:
		admin_dialogue(curs)
	elif a==2:
		manager_dialogue(curs)
	else:
		print ("Вы ввели неправильное число, попробуйте заново")
		start_dialogue (curs)

def admin_dialogue(curs):
	print("Введите пароль, чтобы получить доступ к действиям администратора")
	p = "happynewyear2023"
	padm = input()
	if hash(p) != hash(padm):
		print("Вы ввели неправильный пароль, попробуйте ещё раз")
		admin_dialogue(curs)
	print("Выберите действие")
	print("1 - Ввод новой группы")
	print("2 - Изменение положения группы в хит-параде")
	print("3 - Удаление информации об исполнителе, покинувшем группу")
	choice = int(input())
	if choice == 1:
		adm1(curs)
	elif choice == 2:
		adm2(curs)
	elif choice == 3:
		adm3(curs)
	else:
		print ("Вы ввели неправильное число, попробуйте заново")
		admin_dialogue(curs)
	
		

def manager_dialogue(curs):
	print("Выберите действие")
	print("1 - Узнать год образования и страну группы")
	print("2 - Узнать репертуар наиболее популярной группы")
	print("3 - Узнать автора текста, композитора и дату создания песни")
	print("4 - Узнать место и продолжительность гастролей группы")
	print("5 - Узнать цену билета на концерт группы")
	print("6 - Узнать состав исполнителей группы, их возраст и амплуа")
	print("7 - Получить справку о лучших группах в хит-параде")
	print("8 - Получить отчёт о гастролях групп")
	choice = int(input())
	if choice == 1:
		manage1(curs)
	elif choice == 2:
		manage2(curs)
	elif choice == 3:
		manage3(curs)
	elif choice == 4:
		manage4(curs)
	elif choice == 5:
		manage5(curs)
	elif choice == 6:
		manage6(curs)
	elif choice == 7:
		manage7(curs)
	elif choice == 8:
		manage8(curs)
	else:
		print ("Вы ввели неправильное число, попробуйте заново")
		manager_dialogue(curs)
	

def adm1(curs):
	try:
		print("Введите название группы, год её создания, страну и место в хит-параде")
		start = curs.execute ('SELECT groupid FROM AboutGroups').fetchall()
		name = input()
		year = int(input())
		if year > 2022 or year < 1950:
			print ("Вы ввели неправильный год")
			adm1(curs)
		country = input()
		position = int(input())
		if position < 1:
			print ("Вы ввели неправильное место в хит-параде")
			adm1(curs)
		groupid = len (start) + 1
		curs.execute("""INSERT INTO AboutGroups(groupid, groupname, createyear, groupcountry, hitposition) VALUES (:groupid,\
		:groupname, :createyear, :groupcountry,:hitposition)""", {"groupid": groupid, "groupname": name, "createyear": year,\
		"groupcountry": country, "hitposition": position})
		con.commit() 
		end = curs.execute ('SELECT groupid FROM AboutGroups').fetchall()
		changeid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname":name}).fetchone()
		if len(end)==len(start)+1: 
			print ("Информация о группе успешно добавлена")
		if position <= len(start):
			for i in range (len(end)):
				g=i+1
				pos = curs.execute('SELECT hitposition FROM AboutGroups WHERE groupid=:groupid', {"groupid":g}).fetchone()
				if pos[0] >= position and g!= changeid[0]:
					newpos = pos[0] + 1
					curs.execute('UPDATE AboutGroups SET hitposition=:hitposition WHERE groupid=:groupid',\
					{"hitposition":newpos, "groupid":i+1})
				con.commit()
		print("Введите количество песен в репертуаре новой группы")
		start = curs.execute ('SELECT groupid FROM GroupRepertory').fetchall()
		b = int(input())
		for i in range (b):
			print("Введите номер репертуара, название песни, композитора, автора песни, дату её выхода")
			repid = int(input())
			sname = input()
			scomposer = input()
			sauthor = input()
			sdate = input()
			curs.execute("""INSERT INTO GroupRepertory(groupid, repid, songname, composer, songwriter, createdate) VALUES (:groupid, :repid, :songname,\
			:composer, :songwriter, :createdate)""", {"groupid":groupid, "repid":repid, "songname":sname, "composer":scomposer , "songwriter":sauthor, "createdate":sdate})
		con.commit()
		end = curs.execute ('SELECT groupid FROM GroupRepertory').fetchall()
		if len(end)==len(start)+b: 
			print ("Информация о репертуаре группы успешно добавлена")
		print("Введите количество туров новой группы")
		start = curs.execute ('SELECT tourgroupid FROM GroupTours').fetchall()
		b = int(input())
		for i in range (b):
			print("Введите номер реперутара, название тура, базовую стоимость билета, дату начала тура, дату конца тура и место")
			tourrepid = int(input())
			tname = input()
			tprice = int(input())
			tsdate = input()
			tfdate = input()
			tplace = input()
			curs.execute("""INSERT INTO GroupTours(tourgroupid, tourrepid, tourname, ticketprice, startdate, finishdate, tourplace)\
			VALUES (:tourgroupid, :tourrepid, :tourname, :ticketprice, :startdate, :finishdate, :tourplace)""",\
			{"tourgroupid":groupid, "tourrepid":tourrepid, "tourname":tname, "ticketprice":tprice, "startdate":tsdate,\
			"finishdate":tfdate, "tourplace":tplace})
		con.commit()
		end = curs.execute ('SELECT tourgroupid FROM GroupTours').fetchall()
		if len(end)==len(start)+b:
			print ("Информация о гастролях группы успешно добавлена")

		print("Введите количество участников новой группы")
		start = curs.execute ('SELECT groupid FROM GroupTeam').fetchall()
		b = int(input())
		for i in range (b):
			print("Введите имя участника группы, его роль в группе и возраст")
			tman = input()
			trole = input()
			tage = int(input())
			curs.execute("""INSERT INTO GroupTeam(groupid, teamman, teamrole, age) VALUES (:groupid, :teamman, :teamrole, :age)""",\
			{"groupid":groupid, "teamman":tman, "teamrole":trole, "age":tage})
		con.commit()
		end = curs.execute ('SELECT groupid FROM GroupTeam').fetchall()
		if len(end)==len(start)+b:
			print ("Информация о составе группы успешно добавлена")
		print ("Добавление группы и информации о ней окончено")
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		adm1(curs)

def adm2(curs):
	try:
		print ("Введите название группы, место которой вы хотите поменять в хит-параде")
		start = curs.execute ('SELECT groupid FROM AboutGroups').fetchall()
		name = input()
		pr = curs.execute('SELECT groupname, hitposition FROM AboutGroups WHERE groupname=:groupname', {"groupname":name}).fetchone()
		changeid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname":name}).fetchone()
		print ("Ниже вы можете увидеть, какое место в хит-параде группа занимает сейчас")
		rowsnames = 'Группа', 'Место в хит-параде'
		print("{:<30}{:<30}".format(*rowsnames))
		print("{:<30}{:<30}".format(*pr))
		print ("Введите новое место группы в хит-параде")
		newposition = input()
		curs.execute('UPDATE AboutGroups SET hitposition=:hitposition WHERE groupname=:groupname',\
		{"hitposition":newposition, "groupname":name})
		con.commit()
		pr2 = curs.execute('SELECT groupname, hitposition FROM AboutGroups WHERE groupname=:groupname', {"groupname":name}).fetchone()
		tourgroupid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname":name}).fetchone()
		if pr[1] != pr2[1]: 
			print ("Место в хит-параде изменено успешно")
		else: 
			print("Введите номер места, который будет отличаться от нынешнего")
			adm2(curs)
		tourgroupid = tourgroupid[0]
		startprice = curs.execute('SELECT ticketprice FROM GroupTours WHERE tourgroupid=:tourgroupid',\
		{"tourgroupid":tourgroupid}).fetchone()
		for i in range (len(start)):
			g=i+1
			pos = curs.execute('SELECT hitposition FROM AboutGroups WHERE groupid=:groupid', {"groupid":g}).fetchone()
			if pos[0] == newposition and g!= changeid[0]:
				newpos = pos[0] + 1
				curs.execute('UPDATE AboutGroups SET hitposition=:hitposition WHERE groupid=:groupid',\
				{"hitposition":newpos, "groupid":g})
			con.commit()
		if pr2[1] < pr[1]:
			finishprice = startprice[0]*1.5
			curs.execute('UPDATE GroupTours SET ticketprice=:finishprice WHERE tourgroupid=:tourgroupid',\
			{"tourgroupid":tourgroupid, "finishprice":finishprice})
		con.commit()
		if pr2[1] > pr[1]: 
			finishprice = startprice[0]*0.8
			curs.execute('UPDATE GroupTours SET ticketprice=:finishprice WHERE tourgroupid=:tourgroupid',\
			{"tourgroupid":tourgroupid, "finishprice":finishprice})
		con.commit()
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		adm2(curs)
	

def adm3(curs):
	try:
		print("Введите название группы")
		groupname = input()
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname": groupname}).fetchone()
		groupid = groupid[0]
		start = curs.execute('SELECT teamman FROM GroupTeam WHERE groupid=:groupid', {"groupid": groupid}).fetchall()
		print("Ниже представлен список участников группы")
		for i in start:
			print(i[0])
		print("Введите имя человека, покинувшего группу")
		deleteman = input()
		curs.execute('DELETE FROM GroupTeam WHERE teamman=:deleteman', {"deleteman": deleteman})
		con.commit()
		finish = curs.execute('SELECT teamman FROM GroupTeam WHERE groupid=:groupid', {"groupid": groupid}).fetchall()
		if len(finish)==len(start)-1: 
			print ("Удаление прошло успешно")
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		adm3(curs)

def manage1(curs):
	try:
		print("Введите название группы")
		groupname = input()
		res = curs.execute('SELECT createyear, groupcountry FROM AboutGroups WHERE groupname=:groupname',\
		{"groupname": groupname}).fetchone()
		rowsnames = 'Год создания', 'Страна'
		print("{:<30}{:<30}".format(*rowsnames))
		print("{:<30}{:<30}".format(*res))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage1(curs)

def manage2(curs):
	try:
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE hitposition=1').fetchone()
		groupid = groupid[0]
		res = curs.execute('SELECT songname, composer, songwriter, createdate FROM GroupRepertory\
		WHERE groupid=:groupid', {"groupid": groupid}).fetchall()
		rowsnames = 'Песня', 'Композитор', 'Автор текста', 'Дата создания'
		print("{:<30}{:<30}{:<30}{:<30}".format(*rowsnames))
		for i in res:
			print("{:<30}{:<30}{:<30}{:<30}".format(*i))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage2(curs)

def manage3(curs):
	try:
		print("Введите название песни")
		songname = input()
		res = curs.execute('SELECT composer, songwriter, createdate FROM GroupRepertory\
		WHERE songname=:songname', {"songname": songname}).fetchone()
		rowsnames = 'Композитор', 'Автор текста', 'Дата создания'
		print("{:<30}{:<30}{:<30}".format(*rowsnames))
		print("{:<30}{:<30}{:<30}".format(*res))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage3(curs)

def manage4(curs):
	try:
		print("Введите название группы")
		groupname = input()
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname": groupname}).fetchone()
		groupid = groupid[0]
		res = curs.execute('SELECT tourplace, startdate, finishdate FROM GroupTours\
		WHERE tourgroupid=:groupid', {"groupid": groupid}).fetchall()
		rowsnames = 'Место', 'Дата начала', 'Дата конца'
		print("{:<30}{:<30}{:<30}".format(*rowsnames))
		for i in res:
			print("{:<30}{:<30}{:<30}".format(*i))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage4(curs)


def manage5(curs):
	try:
		print("Введите название группы")
		groupname = input()
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname": groupname}).fetchone()
		groupid = groupid[0]
		res = curs.execute('SELECT tourplace, ticketprice FROM GroupTours WHERE tourgroupid=:groupid', {"groupid": groupid}).fetchall()
		rowsnames = 'Место', 'Цена билета'
		print("{:<30}{:<30}".format(*rowsnames))
		for i in res:
			print("{:<30}{:<30}".format(*i))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage5(curs)

def manage6(curs):
	try:
		print("Введите название группы")
		groupname = input()
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE groupname=:groupname', {"groupname": groupname}).fetchone()
		groupid = groupid[0]
		res = curs.execute('SELECT teamman, teamrole, age FROM GroupTeam\
		WHERE groupid=:groupid', {"groupid": groupid}).fetchall()
		rowsnames = 'Исполнитель', 'Роль в группе', 'Возраст'
		print("{:<30}{:<30}{:<30}".format(*rowsnames))
		for i in res:
			print("{:<30}{:<30}{:<30}".format(*i))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage6(curs)

def manage7(curs):
	try:
		groupid = curs.execute('SELECT groupid FROM AboutGroups WHERE hitposition BETWEEN 1 and 3 ORDER BY hitposition').fetchall()
		rowsnames = 'Группа', 'Год создания', 'Страна', 'Место в хит-параде'
		print("{:<30}{:<30}{:<30}{:<30}".format(*rowsnames))
		for i in groupid:
			groupid = i[0]
			res = curs.execute('SELECT groupname, createyear, groupcountry, hitposition FROM AboutGroups\
			WHERE groupid=:groupid', {"groupid": groupid}).fetchone()
			print("{:<30}{:<30}{:<30}{:<30}".format(*res))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage7(curs)

def manage8(curs):
	try:
		curs.execute('CREATE TABLE IF NOT EXISTS new_table AS SELECT groupid, repid, songname, songwriter FROM GroupRepertory')
		names = curs.execute('SELECT DISTINCT groupname FROM AboutGroups JOIN new_table\
		ON AboutGroups.groupid=new_table.groupid').fetchall()
		tourssongs = curs.execute('SELECT tourgroupid, repid, tourplace, startdate, finishdate, songname, songwriter FROM GroupTours\
		JOIN new_table ON tourrepid=repid AND GroupTours.tourgroupid=new_table.groupid').fetchall()
		names = curs.execute('SELECT groupid, groupname FROM AboutGroups').fetchall()
		rowsnames = 'Название группы', 'Место гастролей', 'Дата начала гастролей', 'Дата конца кастролей',\
		'Песня в репертуаре', 'Автор песни'
		print("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}".format(*rowsnames))
		for i in range (len (tourssongs)):
			for j in range (len(names)):
				if names[j][0] == tourssongs[i][0]:
					output= [0]*6
					output[0] = names[j][1]; output[1] = tourssongs[i][2]; output[2] = tourssongs[i][3]
					output[3] = tourssongs[i][4]; output[4] = tourssongs[i][5]; output[5] = tourssongs[i][6]
					print("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}".format(*output))
	except:
		print("При выполнении запроса произошла ошибка")
		time.sleep(3)
		manage8(curs)


def createandfilltable():
	con=sq.connect("musicmanager.db")
	curs=con.cursor()

	curs.execute("""CREATE TABLE IF NOT EXISTS AboutGroups(
	groupid INTEGER PRIMARY KEY AUTOINCREMENT,
	groupname TEXT,
	createyear INTEGER,
	groupcountry TEXT,
	hitposition INTEGER
	)""")

	sqlgroups = 'INSERT OR IGNORE INTO AboutGroups (groupid, groupname, createyear, groupcountry, hitposition) values(?, ?, ?, ?, ?)'

	AboutGroups = [
		(1, "Arctic Monkeys", 2002, "Великобритания", 1),
		(2, "The Neighborhood", 2011, "США", 3),
		(3, "Imagine Dragons", 2008, "США", 4),
		(4, "Twenty One Pilots", 2009, "США", 5),
		(5, "Alt-J", 2007, "Великобритания", 2),
	]


	curs.execute("""CREATE TABLE IF NOT EXISTS GroupRepertory(
		groupid INTEGER,
		repid INTEGER,
		songname TEXT,
		composer TEXT,
		songwriter TEXT,
		createdate TEXT,
		UNIQUE(groupid, repid, songname, composer, songwriter, createdate)
		)""")

	sqlsongs= 'INSERT OR IGNORE INTO GroupRepertory (groupid, repid, songname, composer, songwriter, createdate) values(?, ?, ?, ?, ?, ?)'

	GroupRepertory = [
		(1, 1, "505", "Ник О'Мэлли", "Алекс Тёрнер", "23.04.2007"),
		(1, 2, "R U Mine?", "Ник О'Мэлли", "Алекс Тёрнер", "27.02.2012"),
		(1, 2, "Do I Wanna Know?", "Ник О'Мэлли", "Алекс Тёрнер", "19.06.2013"),
		(2, 1, "Sweater Weather", "Зак Абелс", "Джесси Рутерфорд", "28.06.2012"),
		(2, 2, "R.I.P. 2 My Youth", "Зак Абелс", "Джесси Рутерфорд", "20.08.2015"),
		(2, 1, "Softcore", "Зак Абелс", "Джесси Рутерфорд", "09.06.2018"),
		(3, 1, "Believer", "Дэн Платцман", "Бэн МакКи", "01.02.2017"),
		(3, 2, "Smoke + Mirrors", "Дэн Платцман", "Бэн МакКи", "17.02.2015"),
		(3, 2, "Demons", "Дэн Платцман", "Бэн МакКи", "28.01.2013"),
		(4, 1, "Heavydirtysoul", "Джош Дан", "Тайлер Джозеф", "17.05.2015"),
		(4, 1, "Goner", "Джош Дан", "Тайлер Джозеф", "17.05.2015"),
		(4, 2, "Stressed Out", "Джош Дан", "Тайлер Джозеф", "28.04.2015"),
		(5, 1, "Breezeblocks", "Том Грин", "Джо Ньюман", "18.05.2012"),
		(5, 1, "Intro", "Том Грин", "Джо Ньюман", "18.05.2012"),
		(5, 2, "Fitzpleasure", "Том Грин", "Джо Ньюман", "18.05.2012"),
	]

	curs.execute("""CREATE TABLE IF NOT EXISTS GroupTours(
		tourgroupid INTEGER,
		tourrepid INTEGER,
		tourname TEXT,
		ticketprice INTEGER,
		startdate TEXT,
		finishdate TEXT,
		tourplace TEXT,
		UNIQUE(tourgroupid, tourrepid, tourname, ticketprice, startdate, finishdate, tourplace)
		)""")

	sqltours = 'INSERT OR IGNORE INTO GroupTours (tourgroupid, tourrepid, tourname, ticketprice, startdate, finishdate, tourplace) values(?, ?, ?, ?, ?, ?, ?)'

	GroupTours = [
		(1, 1, "Arctic Monkeys Russia Tour", 2000, "28.05.2015", "19.08.2015", "Россия"),
		(1, 2, "Arctic Monkeys USA Tour", 1500, "28.06.2016", "19.09.2016", "США"),
		(2, 2, "The Neighborhood USA Tour", 1500, "30.06.2017", "02.09.2017", "США"),
		(2, 1, "The Neighborhood Russia Tour", 2000, "31.07.2018", "14.09.2018", "Россия"),
		(3, 1, "Imagine Dragons USA Tour", 1500, "14.06.2018", "15.09.2018", "США"),
		(3, 2, "Imagine Dragons Russia Tour", 2000, "14.06.2018", "15.09.2018", "Россия"),
		(4, 1, "Twenty One Pilots Russia Tour", 1500, "15.03.2018", "10.04.2018", "Россия"),
		(4, 2, "Twenty One Pilots UK Tour", 1500, "25.02.2016", "15.03.2016", "Великобритания"),
		(5, 2, "Alt-J Russia Tour", 2000, "14.04.2015", "15.07.2015", "Россия"),
		(5, 1, "Alt-J UK Tour", 2000, "18.10.2016", "30.11.2016", "Великобритания")
	]

	curs.execute("""CREATE TABLE IF NOT EXISTS GroupTeam(
		groupid INTEGER,
		teamman TEXT,
		teamrole TEXT,
		age INTEGER,
		UNIQUE(groupid, teamman, teamrole, age)
		)""")

	sqlteam = 'INSERT OR IGNORE INTO GroupTeam (groupid, teamman, teamrole, age) values(?, ?, ?, ?)'

	GroupTeam = [
		(1, "Алекс Тёрнер", "Вокалист", 36),
		(1, "Джейми Кук", "Гитарист", 37),
		(1, "Мэтт Хэлдерс", "Барабанщик", 36),
		(1, "Ник О'Мэлли", "Бас-гитарист", 37),
		(2, "Джесси Резерфорд", "Вокалист", 31),
		(2, "Захари Абелс", "Гитарист", 30),
		(2, "Джереми Фридман", "Гитарист", 31),
		(2, "Майкл Марготт", "Бас-гитарист", 30),
		(3, "Дэн Рейнольдс", "Вокалист", 35),
		(3, "Бен Макки", "Гитарист", 37),
		(3, "Уэйн Сермон", "Гитарист", 38),
		(3, "Ден Плацман", "Барабанщик", 36),
		(4, "Тайлер Джозеф", "Вокалист", 34),
		(4, "Джош Дан", "Барабанщик", 34),
		(5, "Джо Ньюман", "Вокалист", 35),
		(5, "Том Грин", "Барабанщик", 37),
		(5, "Гас Ангер-Гамильтон", "Пианист", 35),
	]

	with con:
		con.executemany(sqlgroups, AboutGroups)
		con.executemany(sqlsongs, GroupRepertory)
		con.executemany(sqltours, GroupTours)
		con.executemany(sqlteam,GroupTeam)
		return con, curs


if __name__ == '__main__':
	con, curs = createandfilltable()
	con.commit()
	start_dialogue (curs)

	con.close()
