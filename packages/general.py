import random
import json
import packages.file_system as fs 
import packages.date_time as date_time 
import RPi.GPIO as GPIO
import time

# clean up gpio pins
def cleanUp():
	GPIO.cleanup()

# Turn on LED
def turnLED(is_to_on=True):
	if is_to_on:
		GPIO.output(16,GPIO.HIGH)
	else:
		GPIO.output(16,GPIO.LOW)

# scan switch
def scanSwitch():
	return not GPIO.input(18)

def turnIzaa(is_from_mic=True,is_to_on=True):
	time.sleep(0.3)
	if is_from_mic:
		if is_to_on:
			GPIO.output(37,GPIO.HIGH) # Open relay from main program
		else:
			GPIO.output(37,GPIO.LOW)# Close relay from main program
	else:
		if is_to_on:
			GPIO.output(36,GPIO.HIGH) # Open relay from mic program
		else:
			GPIO.output(36,GPIO.LOW)

def showTimes(display,quran_time,azan_time,is_error = False):
	if is_error:
		display.lcd_display_string(" Something went ",1)
		display.lcd_display_string("      wrong     ",2)
		return
	display.lcd_display_string(f"Quran at: {quran_time}", 1)
	display.lcd_display_string(f" Azan at: {azan_time} ", 2)

# get random number
def generateRandomNumber(start,end):
	return random.randint(start, end)
	
# Conversions
#Convert from dictionary to string to save inside json file
def convertDictionaryToString(dictionary):
	return json.dumps(dictionary,indent=2)

def convertIntegerToString(number):
	return str(number)

def getRandomNumberFromFile(file_path):
	random_number = generateRandomNumber(1,19)
	return convertIntegerToString(random_number)

def getLastAzanTime():
	if not fs.isFileExisted(fs.TIMES_FILE_PATH):
		return None
	while True:
		all_times = fs.readAllDataFromFile(fs.TIMES_FILE_PATH)
		if len(all_times)==0:
			return None
		today_times = all_times[0]
		if date_time.compareTodayWith(today_times.get("date"))==1:
			fs.removeFirstDay(all_times)
		elif date_time.compareTodayWith(today_times.get("date"))==0:
			if date_time.compareCurrentTimeWith(today_times.get("sobuh"))!=1:
				return {"azan_time":today_times.get("sobuh"),"is_sobuh":True}
			elif date_time.compareCurrentTimeWith(today_times.get("dohur"))!=1:
				return {"azan_time":today_times.get("dohur"),"is_sobuh":False}
			elif date_time.compareCurrentTimeWith(today_times.get("meghreb"))!=1:
				return {"azan_time":today_times.get("meghreb"),"is_sobuh":False}
			else:
				if(len(all_times)==1):
					fs.removeFirstDay(all_times)
					return None
				else:
					today_times = all_times[1]
					fs.removeFirstDay(all_times)
					return {"azan_time":today_times.get("sobuh"),"is_sobuh":True}
		else:
			if date_time.getNumberOfDaysBetweenTwoDates(date_time.getTodayDate(),all_times[0].get("date"))==1:
				today_times = all_times[0]
				return {"azan_time":today_times.get("sobuh"),"is_sobuh":True}
			return None
		
def getQuranTime(random_number,azan_time):
	duration = fs.getSoundDuration(random_number)
	quran_time = date_time.removeSecondsFromTime(duration,azan_time)
	return quran_time
