import random
import packages.file_system as fs 

# get random number
def generateRandomNumber(start,end):
	print("Getting random number")
	return random.randint(start, end)
	
# Conversions

#Convert from dictionary to string
def convertDictionaryToString(dictionary):
	return str(dictionary)

def convertStringToDictionary(string):
	return eval(string)

def convertIntegerToString(number):
	return str(number)

def readFirstLineFromFile(path):
	with open(path, 'r') as file:
		data = file.readline()
	return data

def getRandomNumberFromFile(file_path):
	if not fs.isFileExisted(file_path):
		fs.createFile(file_path)
		random_number = generateRandomNumber(1,19)
		fs.saveIntoFfile(file_path,convertDictionaryToString({"is_broadcast_on":False,"random_number":random_number}))
		return convertIntegerToString(random_number)
	random_number = convertStringToDictionary(readFirstLineFromFile(file_path)).get("random_number")	
	return convertIntegerToString(random_number)