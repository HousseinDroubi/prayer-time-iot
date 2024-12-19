import sys
sys.path.append('/home/pi-user/lcd')
sys.path.append('/home/pi-user/pydub')

import packages.general as general
import packages.file_system as file_system
import packages.date_time as date_time
import time
import drivers
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(16,GPIO.OUT) # This is for mic led
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) # This is for reading switch
GPIO.output(16,GPIO.LOW)
GPIO.output(36,GPIO.LOW)
GPIO.output(37,GPIO.LOW)
display = drivers.Lcd()

time.sleep(3)

def mainProgram():
    while True:
        last_azan = general.getLastAzanTime()
        print(f'azan_time is {last_azan.get("azan_time")}')
        if last_azan is None:
            general.showTimes(display,is_error=True)
            return None
        random_number = general.getRandomNumberFromFile()
        print(f"random_number is {random_number}")
        quran_time = general.getQuranTime(random_number,last_azan.get("azan_time"))
        print(f"quran_time is {quran_time}")

        general.showTimes(display,quran_time,last_azan.get("azan_time"))

        # Time is the same as quran time
        if date_time.compareCurrentTimeWith(quran_time) == 0:
            # Dohur or meghreb times
            if not last_azan.get("is_sobuh"):
                file_system.playSound(random_number=random_number,is_adan_and_quran=True)
                print(1)
            # Sobuh time
            else:
                date_time.waitUntil(last_azan.get("azan_time"))
                file_system.playSound(None,False)
                print(2)
        # Time is before quran time
        elif date_time.compareCurrentTimeWith(quran_time)==-1:
            # Dohur or meghreb times
            if not last_azan.get("is_sobuh"):
                date_time.waitUntil(quran_time)
                file_system.playSound(random_number=random_number,is_adan_and_quran=True)
                print(3)
            # Sobuh time
            else:
                date_time.waitUntil(last_azan.get("azan_time"))
                file_system.playSound(None,False)
                print(4)
        # Time is after quran time
        else:
            # Time is after quran time and the same as azan time
            if date_time.compareCurrentTimeWith(last_azan.get("azan_time"))==0:
                file_system.playSound(None,False) #Only Azan
                print(5)
            # Time is after quran time and before azan time
            elif date_time.compareCurrentTimeWith(last_azan.get("azan_time"))==-1:
                date_time.waitUntil(last_azan.get("azan_time"))
                file_system.playSound(None,False) #Only Azan
                print(6)
            # Time is after quran time and after azan time whcih is after meghreb time
            else:
                time_to_wait = date_time.getSecondsFromMeghrebToSobuh(sobuh_azan_time=last_azan.get("azan_time"))
                print(f"Waiting {time_to_wait//3600} hours or {time_to_wait//60} minutes or {time_to_wait}")
                time.sleep(time_to_wait)
                file_system.playSound(None,False)
                print(7)
            time.sleep(1)

def micProgram():
    while True:
        is_switch_opened = general.scanSwitch()
        if is_switch_opened:
            general.turnLED()
            general.turnIzaa()
        else:
            general.turnLED(is_to_on=False)
            general.turnIzaa(is_to_on=False)
        time.sleep(0.3)

try:
    main_thread = threading.Thread(target=mainProgram)
    mic_thread = threading.Thread(target=micProgram)
    main_thread.start()
    mic_thread.start()
except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    display.lcd_clear()
    general.cleanUp()

