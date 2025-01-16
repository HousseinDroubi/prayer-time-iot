import os
import json
import math
import packages.general as general
from pydub.utils import mediainfo
from pydub import AudioSegment
from pydub.playback import play
import RPi.GPIO as GPIO
import time
import packages.date_time as dt

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
	print(f"file_path is {file_path}")
	audio_info = mediainfo(file_path)
	print(f"audio_info is {audio_info}")
	return math.ceil(float(audio_info['duration'])) + 10

# Play azan
def playAzan(is_sobuh_now=False):
	random_number_for_azan = general.generateRandomNumber(1,3)
	sound = AudioSegment.from_file(f"./azan/azan_{random_number_for_azan}.mp3")
	if is_sobuh_now:
		sound = sound - 3
	play(sound)

# Play quran
def playQuran(random_number):
	sound = AudioSegment.from_file(f"./quran/quran_{random_number}.mp3")
	play(sound)
	
# Play sound
def playSound(random_number,is_adan_and_quran=False,azan_time=None,is_sobuh_now=False):
	general.turnIzaa(is_from_mic=False)
	time.sleep(5)
	if not is_adan_and_quran:
		playAzan(is_sobuh_now=is_sobuh_now)
	else:
		playQuran(random_number=random_number)
		dt.waitUntil(azan_time)
		playAzan(is_sobuh_now=is_sobuh_now)
	time.sleep(1)
	general.turnIzaa(is_from_mic=False,is_to_on=False)
