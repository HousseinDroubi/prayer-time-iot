import sys
sys.path.append('/home/pi-user/lcd')
sys.path.append('/home/pi-user/pydub')

import packages.general as general
import packages.file_system as file_system
import packages.date_time as date_time
import time
# import drivers
import threading
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(36,GPIO.OUT)
# GPIO.setup(37,GPIO.OUT)
# GPIO.setup(16,GPIO.OUT) # This is for mic led
# GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) # This is for reading switch
# GPIO.output(16,GPIO.LOW)
# GPIO.output(36,GPIO.LOW)
# GPIO.output(37,GPIO.LOW)
# display = drivers.Lcd()

time.sleep(3)

def mainProgram():
    while True:
        last_azan = general.getLastAzanTime()
        if last_azan is None:
            #TODO: Remove display = None and put display = display
            general.showTimes(display=None,quran_time=None,azan_time=None,imsak_time=None,is_sobuh_now=False,is_ramadan=False,is_error=True)
            return None
        is_sobuh_now = last_azan.get("is_sobuh")
        azan_time=last_azan.get("azan_time")

        if(date_time.isRamadan(last_azan.get("date")) and last_azan.get("is_sobuh")):
            # TODO: remove display = None and put display = display 
            general.showTimes(display=None,quran_time=None,azan_time=azan_time,imsak_time=last_azan.get("ten_minutes_before_imsak"),is_sobuh_now=None,is_ramadan=True,is_error=False)
            # Get the appropriate random number
            while True:
                random_number = general.getRandomNumberFromFile(1,19)
                sound_duration = file_system.getQuranSoundDuration(random_number) // 60
                # Accept quran duration if it's equal to 7 or 8
                if(sound_duration==7 or sound_duration==8):
                    break
            # Get quran time with taking into consideration the random number
            quran_time = general.getQuranTime(random_number,azan_time)
            
            # It's Quran time
            # TODO: Start comparing 
                
        random_number = general.getRandomNumberFromFile()
        quran_time = general.getQuranTime(random_number,azan_time)

        print(f"quran_time is {quran_time}")
        print(f"random_number is {random_number}")
        print(f'azan_time is {azan_time}')

        #show times
        #TODO: Remove display = None and put display = display 
        general.showTimes(display=None,quran_time=quran_time,azan_time=azan_time,imsak_time=None,is_sobuh_now=is_sobuh_now,is_ramadan=False,is_error=False)
        
        # Time is the same as quran time
        if date_time.compareCurrentTimeWith(quran_time) == 0:
            # Dohur or meghreb times
            if not is_sobuh_now:
                file_system.playSound(random_number=random_number,is_adan_and_quran=True,azan_time=azan_time,is_sobuh_now=is_sobuh_now)
            # Sobuh time
            else:
                date_time.waitUntil(azan_time)
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)
        # Time is before quran time
        elif date_time.compareCurrentTimeWith(quran_time)==-1:
            # Dohur or meghreb times
            if not is_sobuh_now:
                date_time.waitUntil(quran_time)
                file_system.playSound(random_number=random_number,is_adan_and_quran=True,azan_time=azan_time,is_sobuh_now=is_sobuh_now)
            # Sobuh time
            else:
                date_time.waitUntil(azan_time)
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)
        # Time is after quran time
        else:
            # Time is after quran time and the same as azan time
            if date_time.compareCurrentTimeWith(azan_time)==0:
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)#Only Azan
            # Time is after quran time and before azan time
            elif date_time.compareCurrentTimeWith(azan_time)==-1:
                date_time.waitUntil(azan_time)
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)#Only Azan
            # Time is after quran time and after azan time whcih is after meghreb time
            else:
                time_to_wait = date_time.getSecondsFromMeghrebToSobuh(sobuh_azan_time=azan_time)
                print(f"Waiting {time_to_wait//3600} hours or {time_to_wait//60} minutes or {time_to_wait}")
                time.sleep(time_to_wait)
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=True)#Only Azan
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

