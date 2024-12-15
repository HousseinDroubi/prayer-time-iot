import sys
sys.path.append('/home/pi-user/lcd')
sys.path.append('/home/pi-user/pydub')

import packages.general as general
import packages.file_system as file_system
import packages.date_time as date_time
import time
import drivers
import threading

display = drivers.Lcd()
def __init__():
    general.initialization()

def mainProgram():
    while True:
        last_azan = general.getLastAzanTime()
        print(f"azan_time is {last_azan.get("azan_time")}")
        if last_azan is None:
            general.showTimes(display,is_error=True)
            return None
        random_number = general.getRandomNumberFromFile(file_system.INFO_FILE_PATH)
        print(f"random_number is {random_number}")
        quran_time = general.getQuranTime(random_number,last_azan.get("azan_time"))
        print(f"quran_time is {quran_time}")

        general.showTimes(display,quran_time,last_azan.get("azan_time"))

        # Time is the same as quran time
        if date_time.compareCurrentTimeWith(quran_time) == 0:
            if not last_azan.get("is_sobuh"):
                file_system.playSound(random_number=random_number)
            date_time.waitUntil(last_azan.get("azan_time"))
            file_system.playSound(None,True)
        # Time is before quran time
        elif date_time.compareCurrentTimeWith(quran_time)==-1:
            if not last_azan.get("is_sobuh"):
                date_time.waitUntil(quran_time)
                file_system.playSound(random_number=random_number)
            date_time.waitUntil(last_azan.get("azan_time"))
            file_system.playSound(None,True)
        # Time is after quran time
        else:
            # Time is after quran time and the same as azan time
            if date_time.compareCurrentTimeWith(last_azan.get("azan_time"))==0:
                file_system.playSound(None,True)
            # Time is after quran time and before azan time
            elif date_time.compareCurrentTimeWith(last_azan.get("azan_time"))==-1:
                date_time.waitUntil(last_azan.get("azan_time"))
                file_system.playSound(None,True)
            # Time is after quran time and after azan time
            else:
                time_to_wait = date_time.getSecondsFromMeghrebToSobuh(sobuh_azan_time=last_azan.get("azan_time"))
                print(f"Waiting {time_to_wait//3600} hours or {time_to_wait//60} minutes or {time_to_wait}")
                time.sleep(time_to_wait)
            time.sleep(1)

def micProgram():
    while True:
        is_switch_opened = general.scanSwitch()
        if is_switch_opened:
            general.turnOnLED()
            general.turnOnIzaa()
        else:
            general.turnOffLED()
            general.turnOffIzaa()
        time.sleep(0.3)

__init__()

try:
    main_thread = threading.Thread(target=mainProgram)
    mic_thread = threading.Thread(target=micProgram)
    main_thread.start()
    mic_thread.start()
except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    display.lcd_clear()
    general.cleanUp()

