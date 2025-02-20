import os
import json
import math
import packages.general as general
from pydub.utils import mediainfo
from pydub import AudioSegment
from pydub.playback import play
# import RPi.GPIO as GPIO
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
def getQuranSoundDuration(random_number):
	file_path = f'./quran/quran_{random_number}.mp3'
	audio_info = mediainfo(file_path)
	return math.ceil(float(audio_info['duration'])) + 10


# Play azan, here we need a random number for azan when function called then call playFile
def playAzan(is_sobuh_now=False):
	random_number_for_azan = general.generateRandomNumber(1,3)
	file_path = f"./azan/azan_{random_number_for_azan}.mp3"
	playFile(file_path=file_path,is_sobuh_now=is_sobuh_now)

# Play azan, here we need a random number for quran to specify path function called then call
# playFile
def playQuran(random_number,is_sobuh_now=False):
	file_path = f"./quran/quran_{random_number}.mp3"
	playFile(file_path=file_path,is_sobuh_now=is_sobuh_now)
	
# Play sound
def playSound(random_number,is_adan_and_quran=False,azan_time=None,is_sobuh_now=False,ramadan=None):
	general.turnIzaa(is_from_mic=False)
	time.sleep(1)
	if ramadan:
		if ramadan.get("voice_before_twelve_min_from_imsak_time"):
			random_number_for_voice_before_imsak = general.generateRandomNumber(1,5)
			file_path = f"./ramadan/voices/before_imsak/voice_{random_number_for_voice_before_imsak}.mp3"
			playFile(file_path=file_path,is_sobuh_now=True)
			dt.waitUntil(ramadan.get("ten_minutes_before_imsak_time"))

		if ramadan.get("imsak_sound_before_imsak_time"):
			random_number_for_imsak_sound = general.generateRandomNumber(1,5)
			file_path = f"./ramadan/sounds/sound_{random_number_for_imsak_sound}.mp3"
			playFile(file_path=file_path,is_sobuh_now=True)
			dt.waitUntil(ramadan.get("imsak_time"))
		
		if ramadan.get("voice_before_quran_time"):
			file_path = f"./ramadan/voices/before_quran/voice.mp3"
			playFile(file_path=file_path,is_sobuh_now=True)
			dt.waitUntil(ramadan.get("quran_time"))
	else:
		if is_adan_and_quran:
			playQuran(random_number=random_number,is_sobuh_now = is_sobuh_now)
			dt.waitUntil(azan_time)
		playAzan(is_sobuh_now=is_sobuh_now)
	time.sleep(1)
	general.turnIzaa(is_from_mic=False,is_to_on=False)

# Play sound from file, needed only path and if is_sobuh to decrease volume
def playFile(file_path,is_sobuh_now=False):
	sound = AudioSegment.from_file(file_path)
	if is_sobuh_now:
		sound = sound - 3
	play(sound)
