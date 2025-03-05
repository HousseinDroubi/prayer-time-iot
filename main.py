import sys
sys.path.append('/home/pi-user/lcd')
sys.path.append('/home/pi-user/pydub')

import packages.general as general
import packages.file_system as file_system
import packages.date_time as date_time
import time

import drivers
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,GPIO.LOW)
display = drivers.Lcd()

time.sleep(1)

def main():
    while True:
        last_azan = general.getLastAzanTime()
        if last_azan is None:
            general.showTimes(display=display,quran_time=None,azan_time=None,imsak_time=None,is_sobuh_now=False,is_ramadan=False,is_error=True)
            return None
        is_sobuh_now = last_azan.get("is_sobuh")
        azan_time=last_azan.get("azan_time")
        random_number = general.getRandomNumberFromFile()
        quran_time = general.getQuranTime(random_number,azan_time)

        if(date_time.isRamadan(last_azan.get("date")) and last_azan.get("is_sobuh")):
            # Get imsak time
            imsak_time = last_azan.get("imsak")
            
            # Get 22 mins before imsak
            twenty_two_minutes_before_imsak = date_time.removeSecondsFromTime(120,last_azan.get("twenty_minutes_before_imsak"))
            
            # Get 10 mins before imsak
            ten_minutes_before_imsak = last_azan.get("ten_minutes_before_imsak")

            general.showTimes(display=display,quran_time=None,azan_time=azan_time,imsak_time=imsak_time,is_sobuh_now=None,is_ramadan=True,is_error=False)
            
            # Get the appropriate random number
            while True:
                random_number = general.getRandomNumberFromFile()
                # Get quran time with taking into consideration the random number
                sound_duration = file_system.getQuranSoundDuration(random_number) // 60
                # Accept quran duration if it's equal to 7
                if sound_duration == 7:
                    break
            

            if date_time.getNumberOfDaysBetweenTwoDates(date_1=date_time.getTodayDate(),date_2=last_azan.get("date")) == 1 or date_time.compareCurrentTimeWith(twenty_two_minutes_before_imsak) != 1:
                
                # If time is not the same as 22 min before imsak, then wait until 22 min before imsak
                if date_time.compareCurrentTimeWith(twenty_two_minutes_before_imsak) == -1:
                    date_time.waitUntil(twenty_two_minutes_before_imsak)

                # Below means that the current time is before midnight
                elif date_time.getNumberOfDaysBetweenTwoDates(date_1=date_time.getTodayDate(),date_2=last_azan.get("date")) == 1:
                    time_to_wait = date_time.getSecondsStartingBeforeMidnightTo(goal_time=twenty_two_minutes_before_imsak)
                    print(f"Waiting {time_to_wait//3600} hours or {time_to_wait//60} minutes or {time_to_wait}")
                    time.sleep(time_to_wait)
                
                file_system.playSound(random_number=random_number,is_adan_and_quran=None,
                    azan_time=None,is_sobuh_now=None,
                    ramadan={
                        "voice_before_twenty_two_min_from_imsak_time":True,
                        "ten_minutes_before_imsak_time":ten_minutes_before_imsak,
                        "voice_before_ten_min_from_imsak_time":True,
                        "imsak_music":True,
                        "imsak_time":imsak_time,
                        "voice_before_quran_time":True,
                        "azan_time":azan_time
                    })

            # This time is after 22 minutes before imsak
            # Check if time is before or equal 10 minutes before imsak
            elif date_time.compareCurrentTimeWith(ten_minutes_before_imsak) !=1:
                
                # If time is not the same as 10 min before imsak, then wait until 10 min before imsak
                if(date_time.compareCurrentTimeWith(ten_minutes_before_imsak) == -1):
                    date_time.waitUntil(ten_minutes_before_imsak)
                file_system.playSound(random_number=random_number,is_adan_and_quran=None,
                    azan_time=None,is_sobuh_now=None,
                    ramadan={
                        "voice_before_twenty_two_min_from_imsak_time":False,
                        "ten_minutes_before_imsak_time":None,
                        "voice_before_ten_min_from_imsak_time":True,
                        "imsak_music":True,
                        "imsak_time":imsak_time,
                        "voice_before_quran_time":True,
                        "azan_time":azan_time
                    })
            # This time is after 10 minutes before imsak
            # Check if time is before or equal imsak time
            elif date_time.compareCurrentTimeWith(imsak_time)!=1:
                # If time is not the same as imsak time, then wait until imsak time
                if date_time.compareCurrentTimeWith(imsak_time)==-1:
                    date_time.waitUntil(imsak_time)
                file_system.playSound(random_number=random_number,is_adan_and_quran=None,
                    azan_time=None,is_sobuh_now=None,
                    ramadan={
                        "voice_before_twenty_two_min_from_imsak_time":False,
                        "ten_minutes_before_imsak_time":None,
                        "voice_before_ten_min_from_imsak_time":False,
                        "imsak_music":False,
                        "imsak_time":None,
                        "voice_before_quran_time":True,
                        "azan_time":azan_time
                    })
            # Check if time is after imsak time
            # Check if time is before or equal quran time
            elif date_time.compareCurrentTimeWith(quran_time) != 1:
                # If time is not the same as quran time, then wait until quran time
                if date_time.compareCurrentTimeWith(quran_time)==-1:
                    date_time.waitUntil(quran_time)
                file_system.playSound(random_number=random_number,is_adan_and_quran=True,azan_time=None,is_sobuh_now=True,ramadan=None)

            # Check if time is after quran time
            else:
                # Check if time is before or equal azan time
                if date_time.compareCurrentTimeWith(azan_time)==-1:
                    date_time.waitUntil(azan_time)
                # If time is not the same as azan time, then wait until azan time
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=True,ramadan=None)
            continue

        print(f"quran_time is {quran_time}")
        print(f"random_number is {random_number}")
        print(f'azan_time is {azan_time}')

        #show times
        general.showTimes(display=display,quran_time=quran_time,azan_time=azan_time,imsak_time=None,is_sobuh_now=is_sobuh_now,is_ramadan=False,is_error=False)
        
        # Time is either at quran time or before it
        if date_time.compareCurrentTimeWith(quran_time) != 1:
            # Dohur or meghreb times
            if not is_sobuh_now:
                if date_time.compareCurrentTimeWith(quran_time) == -1:
                    date_time.waitUntil(quran_time)
                file_system.playSound(random_number=random_number,is_adan_and_quran=True,azan_time=azan_time,is_sobuh_now=is_sobuh_now)
            # Sobuh time
            else:
                date_time.waitUntil(azan_time)
                file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)

        # Time is either at azan time or before it
        elif date_time.compareCurrentTimeWith(azan_time)!=1:

            # Time is after quran time and before azan time
            if date_time.compareCurrentTimeWith(azan_time)==-1:
                date_time.waitUntil(azan_time)
            file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=is_sobuh_now)#Only Azan

        # Time is after quran time and after azan time which is after meghreb time
        else:
            time_to_wait = date_time.getSecondsStartingBeforeMidnightTo(goal_time=azan_time)
            print(f"Waiting {time_to_wait//3600} hours or {time_to_wait//60} minutes or {time_to_wait}")
            time.sleep(time_to_wait)
            file_system.playSound(random_number=None,is_adan_and_quran=False,azan_time=None,is_sobuh_now=True)#Only Azan
        time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    display.lcd_clear()
    general.cleanUp()

