import os
import json
import math
import packages.general as general
from pydub.utils import mediainfo
from pydub import AudioSegment
from pydub.playback import play
import time
import packages.date_time as dt
import vlc

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# env variables
# Ramdan timing
START_DUAA_VOICE = int(os.getenv('START_DUAA_VOICE'))
END_DUAA_VOICE = int(os.getenv('END_DUAA_VOICE'))
# Imsak Music
START_IMSAK_MUSIC = int(os.getenv('START_IMSAK_MUSIC'))
END_IMSAK_MUSIC = int(os.getenv('END_IMSAK_MUSIC'))
# Azan Music
START_AZAN_SOUND = int(os.getenv('START_AZAN_SOUND'))
END_AZAN_SOUND = int(os.getenv('END_AZAN_SOUND'))

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
	file_path = f'./sounds/quran/quran_{random_number}.mp3'
	audio_info = mediainfo(file_path)
	return math.ceil(float(audio_info['duration'])) + 10

# Play azan, here we need a random number for azan when function called then call playFile
def playAzan(is_sobuh_now=False):
	random_number_for_azan = general.generateRandomNumber(START_AZAN_SOUND,END_AZAN_SOUND)
	file_path = f"./sounds/azan/azan_{random_number_for_azan}.mp3"
	playFile(file_path=file_path,is_sobuh_now=is_sobuh_now)

# Play azan, here we need a random number for quran to specify path function called then call
# playFile
def playQuran(random_number,is_sobuh_now=False):
	file_path = f"./sounds/quran/quran_{random_number}.mp3"
	playFile(file_path=file_path,is_sobuh_now=is_sobuh_now)
	
# Play sound
def playSound(random_number,is_adan_and_quran=False,azan_time=None,is_sobuh_now=False,ramadan=None):
	general.turnIzaa()
	time.sleep(1)
	if ramadan:
		if ramadan.get("voice_before_twenty_two_min_from_imsak_time"):
			random_number_for_voice_before_imsak = general.generateRandomNumber(START_DUAA_VOICE,END_DUAA_VOICE)
			file_path = f"./sounds/ramadan/voices/before_imsak/20_min/voice_{random_number_for_voice_before_imsak}.mp3"
			playFile(file_path=file_path)
			time.sleep(1)
			random_number_for_imsak_sound = general.generateRandomNumber(START_IMSAK_MUSIC,END_IMSAK_MUSIC)
			file_path = f"./sounds/ramadan/sounds/sound_{random_number_for_imsak_sound}.mp3"			
			playFile(file_path=file_path)
			dt.waitUntil(ramadan.get("ten_minutes_before_imsak_time"))
		
		if ramadan.get("voice_before_ten_min_from_imsak_time"):
			file_path = f"./sounds/ramadan/voices/before_imsak/10_min/voice.mp3"
			playFile(file_path=file_path)
			time.sleep(1)

		if ramadan.get("imsak_music"):
			random_number_for_imsak_sound = general.generateRandomNumber(START_IMSAK_MUSIC,END_IMSAK_MUSIC)
			file_path = f"./sounds/ramadan/sounds/sound_{random_number_for_imsak_sound}.mp3"
			playFile(file_path=file_path)
			dt.waitUntil(ramadan.get("imsak_time"))
		
		if ramadan.get("voice_before_quran_time"):
			file_path = f"./sounds/ramadan/voices/before_imsak/0_min/voice.mp3"
			playFile(file_path=file_path)
			time.sleep(1)
			playQuran(random_number=random_number,is_sobuh_now=True)
			dt.waitUntil(ramadan.get("azan_time"))
			playAzan(is_sobuh_now=True)

	else:
		if is_adan_and_quran:
			playQuran(random_number=random_number,is_sobuh_now = is_sobuh_now)
			dt.waitUntil(azan_time)
		playAzan(is_sobuh_now=is_sobuh_now)
	time.sleep(1)
	general.turnIzaa(is_to_on=False)

# Play sound from file, needed only path and if is_sobuh to decrease volume
def playFile(file_path,is_sobuh_now=False):
	try:
		sound = AudioSegment.from_file(file_path)
		if is_sobuh_now:
			sound = sound - 3
		play(sound)
	except:
		player = vlc.MediaPlayer(file_path)
		player.play()
		time.sleep(0.5) # This to let the python-vlc work
		while player.is_playing():
			continue