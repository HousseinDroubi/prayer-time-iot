import os
import json
import math
import packages.general as general
from pydub.utils import mediainfo
from pydub import AudioSegment
from pydub.playback import play
import RPi.GPIO as GPIO
import time

INFO_FILE_PATH = "info.json"
TIMES_FILE_PATH = "times.json"

# remove first day from times file

def removeFirstDay(all_times):
	all_times.pop(0)
	all_times = general.convertDictionaryToString(all_times)
	saveIntoFfile(TIMES_FILE_PATH,all_times)

# clear file contents
def clearFile(path):
	with open(path,'w'):
		pass

# create file
def createFile(path):
	clearFile(path)
		
def saveIntoFfile(path,contents):
	with open(path,'w') as file:
		file.write(contents)
		
# Check if file existed
def isFileExisted(path):
	return os.path.exists(path)

# Read all data from a file
def readAllDataFromFile(path):
	with open(path, 'r') as file:
		data = json.load(file)
	return data

# Get sound duration
def getSoundDuration(random_number):
	file_path = f'quran/quran_{random_number}.mp3'
	audio_info = mediainfo(file_path)
	return math.ceil(float(audio_info['duration'])) + 10

# Play sound
def playSound(random_number,is_adan=False):
	GPIO.output(37,GPIO.HIGH) # Open relay
	time.sleep(5)
	update_info = readAllDataFromFile(INFO_FILE_PATH)
	update_info["is_broadcast_on"]=True
	saveIntoFfile(INFO_FILE_PATH,general.convertDictionaryToString(update_info))
	if(is_adan):
		sound = AudioSegment.from_file("./adan/adan.mp3")
	else:
		sound = AudioSegment.from_file(f"./quran/quran_{random_number}.mp3")
	play(sound)
	time.sleep(1)
	GPIO.output(37,GPIO.LOW)# Close relay
	update_info["is_broadcast_on"]=False
	saveIntoFfile(INFO_FILE_PATH,general.convertDictionaryToString(update_info))

