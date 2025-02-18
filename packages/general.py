import random
import json
import packages.file_system as fs 
import packages.date_time as date_time 
# import RPi.GPIO as GPIO
import time

# clean up gpio pins
def cleanUp():
	# GPIO.cleanup()
		print("Cleaning GPIO")

# toggle LED
def turnLED(is_to_on=True):
	if is_to_on:
		# GPIO.output(16,GPIO.HIGH)
		print("Turning on Led")
	else:
		# GPIO.output(16,GPIO.LOW)
		print("Turning off Led")

# scan switch
def scanSwitch():
	return False
	# return not GPIO.input(18)

# toggle izaa 
def turnIzaa(is_from_mic=True,is_to_on=True):
	time.sleep(0.3)
	if is_from_mic:
		if is_to_on:
			print("Turn on Izaa from main program")
			# GPIO.output(37,GPIO.HIGH) # Open relay from main program
		else:
			print("Turn off Izaa from main program")
			# GPIO.output(37,GPIO.LOW)# Close relay from main program
	else:
		if is_to_on:
			print("Turn on Izaa from mic program")
			# GPIO.output(36,GPIO.HIGH) # Open relay from mic program
		else:
			print("Turn off Izaa from mic program")
			# GPIO.output(36,GPIO.LOW) # Close relay from mic program

def showTimes(display,quran_time,azan_time,is_sobuh_now=False,is_error = False):
	if is_error:
		print("Showing Something went wrong")
		# display.lcd_display_string(" Something went ",1)
		# display.lcd_display_string("      wrong     ",2)
		return
	if is_sobuh_now:
		print("----------------------")
		# display.lcd_display_string(f" -------------- ", 1)
	else:	
		print(f"Quran at: {quran_time}")
		# display.lcd_display_string(f"Quran at: {quran_time}", 1)
	# display.lcd_display_string(f" Azan at: {azan_time} ", 2)
	print(f" Azan at: {azan_time} ")

# get random number
def generateRandomNumber(start,end):
	return random.randint(start, end)
	
# Conversions
#Convert from dictionary to string to save inside json file
def convertDictionaryToString(dictionary):
	return json.dumps(dictionary,indent=2)

def convertIntegerToString(number):
	return str(number)

def getRandomNumberFromFile():
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
		# If today is greater than first day in json
		if date_time.compareDateWith(today_times.get("date"))==1:
			fs.removeFirstDay(all_times)
		# If today is the same as first day in json
		elif date_time.compareDateWith(today_times.get("date"))==0:
			# If current time is the same as sobuh or less than it
			if date_time.compareCurrentTimeWith(today_times.get("sobuh"))!=1:
				return {"azan_time":today_times.get("sobuh"),"date":today_times.get("date"),"ten_minutes_before_imsak":today_times.get("ten_minutes_before_imsak"),"is_sobuh":True}
			# If current time is the same as dohur or less than it
			elif date_time.compareCurrentTimeWith(today_times.get("dohur"))!=1:
				return {"azan_time":today_times.get("dohur"),"date":today_times.get("date"),"ten_minutes_before_imsak":today_times.get("ten_minutes_before_imsak"),"is_sobuh":False}
			# If current time is the same as meghreb or less than it
			elif date_time.compareCurrentTimeWith(today_times.get("meghreb"))!=1:
				return {"azan_time":today_times.get("meghreb"),"date":today_times.get("date"),"ten_minutes_before_imsak":today_times.get("ten_minutes_before_imsak"),"is_sobuh":False}
			else:
				# If current time is the greater than meghreb and only one today left in json which must be deleted
				if(len(all_times)==1):
					fs.removeFirstDay(all_times)
					return None
				# If current time is the greater than meghreb and today with other days left in json, so only today must be deleted and must return second day's sobuh
				else:
					today_times = all_times[1]
					fs.removeFirstDay(all_times)
					return {"azan_time":today_times.get("sobuh"),"date":today_times.get("date"),"ten_minutes_before_imsak":today_times.get("ten_minutes_before_imsak"),"is_sobuh":True}
		# If today is less than first day in json
		else:
			# If there's only the as difference between today and first day in json is "one", means that today is deleted from json and must return second day's sobuh
			if date_time.getNumberOfDaysBetweenTwoDates(date_time.getTodayDate(),all_times[0].get("date"))==1:
				today_times = all_times[0]
				return {"azan_time":today_times.get("sobuh"),"date":today_times.get("date"),"ten_minutes_before_imsak":today_times.get("ten_minutes_before_imsak"),"is_sobuh":True}
			# If there are many days difference between today and first day in json
			return None
		
def getQuranTime(random_number,azan_time):
	duration = fs.getSoundDuration(random_number)
	quran_time = date_time.removeSecondsFromTime(duration,azan_time)
	return quran_time
