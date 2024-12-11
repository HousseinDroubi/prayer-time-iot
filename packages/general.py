import random
import json
import packages.file_system as fs 
import packages.date_time as date_time 

# get random number
def generateRandomNumber(start,end):
	print("Getting random number")
	return random.randint(start, end)
	
# Conversions
#Convert from dictionary to string to save inside json file
def convertDictionaryToString(dictionary):
	return json.dumps(dictionary,indent=2)

def convertIntegerToString(number):
	return str(number)

def getRandomNumberFromFile(file_path):
	if not fs.isFileExisted(file_path):
		fs.createFile(file_path)
		random_number = generateRandomNumber(1,19)
		fs.saveIntoFfile(file_path,convertDictionaryToString({"is_broadcast_on":False,"random_number":random_number}))
		return convertIntegerToString(random_number)
	random_number = fs.readAllDataFromFile(file_path).get("random_number")	
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
		else:
			if date_time.compareCurrentTimeWith(today_times.get("sobuh"))!=1:
				return {"azan_time":today_times.get("sobuh"),"is_sobuh":True}
			elif date_time.compareCurrentTimeWith(today_times.get("dohur"))!=1:
				return {"azan_time":today_times.get("dohur"),"is_sobuh":False}
			elif date_time.compareCurrentTimeWith(today_times.get("meghreb"))!=1:
				return {"azan_time":today_times.get("meghreb"),"is_sobuh":False}
			else:
				fs.removeFirstDay(all_times)