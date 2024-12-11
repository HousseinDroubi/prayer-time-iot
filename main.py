import packages.general as general
import packages.file_system as file_system

def __init__():
    last_azan = general.getLastAzanTime()
    print(f"azan_time is {last_azan.get("azan_time")}")
    if last_azan is None:
        return None
    random_number = general.getRandomNumberFromFile(file_system.INFO_FILE_PATH)
    print(f"random_number is {random_number}")
    quran_time = general.getQuranTime(random_number,last_azan.get("azan_time"))
    print(f"quran_time is {quran_time}")

__init__()