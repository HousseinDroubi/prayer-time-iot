import random
import os

INFO_FILE_PATH = "info.txt"

# get random number
def generateRandomNumber(start,end):
	print("Getting random number")
	return random.randint(start, end)

# clear file contents
def clearFile(path):
	with open(path,'w') as file:
		print(f"clearing file {path}")
		pass

# create file
def createFile(path):
	print(f"Creating file {path}")
	clearFile(path)
		
def saveIntoFfile(path,contents):
	with open(path,'w') as file:
		file.write(contents)
		
# check if file existed
def isFileExisted(path):
	print(f"Checking if {path} existed")
	return os.path.exists(path)
	
	
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
	if not isFileExisted(file_path):
		createFile(file_path)
		random_number = generateRandomNumber(1,19)
		saveIntoFfile(file_path,convertDictionaryToString({"is_broadcast_on":False,"random_number":random_number}))
		return convertIntegerToString(random_number)
	random_number = convertStringToDictionary(readFirstLineFromFile(file_path)).get("random_number")	
	print(random_number)
