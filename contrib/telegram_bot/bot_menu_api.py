#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Main modules
import sys
import time
import datetime
import telepot
#import sqlite3
import requests
from picamera import PiCamera
import calendar
current_year = int(datetime.datetime.now().strftime("%Y"))
current_month = int(datetime.datetime.now().strftime("%m"))

#Modules for buttons
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

#Whitelist with "Username" from Telegram
users = ["Username_1,Username_2"]
#API Token from @BotFather
TOKEN_BOT = "INPUT_TOKEN"
#User and password for administartion Terrarium Pi
login_user_Terrarium_Pi = "admin"
login_password_Terrarium_Pi = "password"

def StampToHuman(TimeForConvert): # Convert any unix timestamp in human form
	human_time = datetime.datetime.fromtimestamp(TimeForConvert).strftime("%d %B %Y %H:%M ")
	return human_time

def handle(msg): #Wait message from user in telegram
	bot = telepot.Bot(TOKEN_BOT)
	user_id = msg["from"]["username"]
	chat_id = msg["chat"]["id"]
	command = msg["text"]

	counter = 0
	dict_switches_id = {}
	dict_switches_name = {}
	for item in requests.get(url = "http://localhost:8090/api/switches").json()["switches"]:
		counter += 1
		dict_switches_id["Switch{0}".format(counter)] = str(item["id"])
		dict_switches_name["Switch{0}".format(counter)] = str(item["name"])

	#counter = 0
	#dict_switches_name = {}
	#for item in requests.get(url = "http://localhost:8090/api/switches").json()["switches"]:
		#counter += 1
		#dict_switches_name["Switch{0}".format(counter)] = str(item["name"])

	print "Got command: %s" % command

#Check whitelist
	if user_id not in users:
		bot.sendMessage(chat_id, "Fuck off")
		return

#Date, time, week number/day of year
	if command == "/time":
		bot.sendMessage(chat_id,
		str(datetime.datetime.now().strftime(
		"Current date and time:\n%d %B %Y %H:%M \nWeek number of year: %W \nDay of year: %j"))
		)
	
#Simple calendar on month
	elif command == '/calendar':
		calendar_print = calendar.LocaleTextCalendar(firstweekday=0, locale = "ru_RU.UTF-8").formatmonth(current_year, current_month, 0, 0).encode("utf8")
		#Print in terminal or in log(nohup.out) if you execute - "nohup BOT.py &"
		print(calendar_print)
		#Send message to user
		bot.sendMessage(chat_id, text = str("<pre>"+calendar_print+"</pre>"), parse_mode = "HTML")

#Main menu
	elif command == "/test" or command == "Return to Main Menu":
		bot.sendMessage(chat_id, "Choose your destiny...",
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text="Summary information")],
		[KeyboardButton(text="Alerts"), KeyboardButton(text="Photo")],
		[KeyboardButton(text="Management"), KeyboardButton(text="Administration")],
		[KeyboardButton(text="Other tools")],
		]
		))
		
#Info about raspberry pi
	elif command == "/status":
		api_req_get_status_rpi = requests.get(url = "http://localhost:8090/api/system").json()
		for_print = str(
		"Terrarium Pi works about ~"+format(api_req_get_status_rpi["uptime"]/60/60, ".1f")+" hours"
		"\nTemperature on board: "+format(api_req_get_status_rpi["temperature"], ".2f")+" C"+
		"\nFree memory is "+format(api_req_get_status_rpi['memory']['free']/1024/1024, ".1f")+" MB"+
		" of total "+format(api_req_get_status_rpi['memory']['total']/1024/1024, ".1f")+" MB"
		)
		
		#Print in terminal or in log(nohup.out) if you execute - "nohup BOT.py &"
		print(for_print)
		#Send message to user
		bot.sendMessage(chat_id,for_print)

#Menu - "Summary information"
	elif command == "Summary information":
		#Variables for this command:
		api_req_get_sensors = requests.get(url = "http://localhost:8090/api/sensors").json()["sensors"]
		api_req_get_doors = requests.get(url = "http://localhost:8090/api/doors").json()["doors"]
		for_print=""
		#Cycle for collect info about sensors:
		for item in api_req_get_sensors:
			for_print += str("On "+item["hardwaretype"]+" "+item["type"]+" is "+format(item["current"], ".2f")+item["indicator"]+"\n")
		#Cycle for alert about "open" door:
		for item in api_req_get_doors:
			if str(item["state"]) == "open":
				for_print += str(item["name"]+" is "+item["state"]+ " !")
		#Print in terminal or in log(nohup.out) if you execute - "nohup BOT.py &"
		print(for_print)
		#Send message to user
		bot.sendMessage(chat_id,for_print)

#Menu - "Alerts"
	elif command == "Alerts" or command == "Update information about alerts":
		#Variables for this command:
		api_req_get_sensors = requests.get(url = "http://localhost:8090/api/sensors").json()["sensors"]
		api_req_get_doors = requests.get(url = "http://localhost:8090/api/doors").json()["doors"]
		for_print=""
		#Cycle for collect info about sensor whose data over "alarm_min" and "alarm_max"
		for item in api_req_get_sensors:
			if str(item["alarm"]) == "True":
				if item["current"] < item["alarm_min"]:
					for_print += str("Too low "+item["type"]+" on "+item["name"]+": "+format(item["current"], ".2f")+" !\n")
				if item["current"] > item["alarm_max"]:
					for_print += str("Too high "+item["type"]+" on "+item["name"]+": "+format(item["current"], ".2f")+" !\n")
		#Cycle for alert about "open" door:
		for item in api_req_get_doors:
			if str(item["state"]) == "open":
				for_print += str(item["name"]+" is "+item["state"]+ " !")
		#Print in terminal or in log(nohup.out) if you execute - "nohup BOT.py &"
		print(for_print)
		#Send message to user
		bot.sendMessage(chat_id,for_print)
		bot.sendMessage(chat_id, "UNDER CONSTRUCTION",
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text="Turn OFF VCC")], #At this point there should be a switch which disconnect main electricity(relay before of socket block)
		[KeyboardButton(text="Update information about alerts")],
		[KeyboardButton(text="Return to Main Menu")],
		]
		))

#Menu - "Photo"
	elif command == "Photo" or command == "Shoot new photo":
		camera = PiCamera()
		camera.resolution = (640, 480)
		camera.annotate_text_size = 22
		camera.annotate_text = str(datetime.datetime.now().strftime(
		"%d %B %Y %H:%M"))
		camera.capture("/home/pi/capt_for_bot.jpg")
		time.sleep(5)
		camera.close()
		bot.sendPhoto(chat_id, photo = open("/home/pi/capt_for_bot.jpg", "rb"),
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text="Shoot new photo")],
		[KeyboardButton(text="Return to Main Menu")],
		]
		))

#Menu - "Management"
	elif command == "Management" or command == "Update information about switches":
		api_req_get_switches = requests.get(url = "http://localhost:8090/api/switches").json()["switches"]
		for_print=""
		for item in api_req_get_switches:
			if str(item["state"]) == "True":
				for_print += str(item["name"]+" is now: ON\n")
			if str(item["state"]) == "False":
				for_print += str(item["name"]+" is now: OFF\n")
		print(for_print)
		#Dictionary of four name and IDs switches for buttons in my variant
		counter = 0
		dict_switches_name = {}
		dict_switches_id = {}
		for item in api_req_get_switches:
			counter += 1
			dict_switches_name["Switch{0}".format(counter)] = str(item["name"])
			dict_switches_id["Switch{0}".format(counter)] = str(item["id"])		
		bot.sendMessage(chat_id,for_print,
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text= str("Toggle "+dict_switches_name.get("Switch1"))), KeyboardButton(text= str("Toggle "+dict_switches_name.get("Switch2")))],
		[KeyboardButton(text= str("Toggle "+dict_switches_name.get("Switch3"))), KeyboardButton(text= str("Toggle "+dict_switches_name.get("Switch4")))],
		[KeyboardButton(text="Update information about switches")],
		[KeyboardButton(text="Return to Main Menu")],
		]
		))

#Toggle switches
	elif command == str("Toggle "+dict_switches_name.get("Switch1")):
		requests.post(url = str("http://localhost:8090/api/switch/toggle/"+dict_switches_id.get("Switch1")), auth=(login_user_Terrarium_Pi, login_password_Terrarium_Pi))
		for_print = requests.get(url = 'http://localhost:8090/api/switches/dict_switches_id.get("Switch1")').json()["switches"][0]["state"]
		print (for_print)
		bot.sendMessage(chat_id, for_print)
		
	elif command == str("Toggle "+dict_switches_name.get("Switch2")):
		requests.post(url = str("http://localhost:8090/api/switch/toggle/"+dict_switches_id.get("Switch2")), auth=(login_user_Terrarium_Pi, login_password_Terrarium_Pi))
		for_print = requests.get(url = 'http://localhost:8090/api/switches/dict_switches_id.get("Switch2")').json()["switches"][0]["state"]
		print (for_print)
		bot.sendMessage(chat_id, for_print)
		
	elif command == str("Toggle "+dict_switches_name.get("Switch3")):
		requests.post(url = str("http://localhost:8090/api/switch/toggle/"+dict_switches_id.get("Switch3")), auth=(login_user_Terrarium_Pi, login_password_Terrarium_Pi))
		for_print = requests.get(url = 'http://localhost:8090/api/switches/dict_switches_id.get("Switch3")').json()["switches"][0]["state"]
		print (for_print)
		bot.sendMessage(chat_id, for_print)
		
	elif command == str("Toggle "+dict_switches_name.get("Switch4")):
		requests.post(url = str("http://localhost:8090/api/switch/toggle/"+dict_switches_id.get("Switch4")), auth=(login_user_Terrarium_Pi, login_password_Terrarium_Pi))
		for_print = requests.get(url = 'http://localhost:8090/api/switches/dict_switches_id.get("Switch4")').json()["switches"][0]["state"]
		print (for_print)
		bot.sendMessage(chat_id, for_print)
		
	elif command == "Administration": #Menu - "Administration"
		bot.sendMessage(chat_id, "In this menu you can add or remove users who can chat with bot \nUNDER CONSTRUCTION",
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text="Add/Remove user")],
		[KeyboardButton(text="Return to Main Menu")],
		]
		))

	elif command == "Other tools":#Menu - "Other tools"
		bot.sendMessage(chat_id, "Some features for yourself\nUNDER CONSTRUCTION",
		reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		[KeyboardButton(text="/time"), KeyboardButton(text="/calendar")],
		[KeyboardButton(text="/status"), KeyboardButton(text="???")],
		[KeyboardButton(text="Return to Main Menu")],
		]
		))

bot = telepot.Bot(TOKEN_BOT)
bot.message_loop(handle)
print "I am listening..."

while 1:
	time.sleep(10)
