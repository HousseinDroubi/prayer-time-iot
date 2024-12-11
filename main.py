import packages.general as general
import packages.file_system as file_system

def __init__():
    last_azan = general.getLastAzanTime()
    if last_azan is None:
        return None
    random_number = general.getRandomNumberFromFile(file_system.INFO_FILE_PATH)
    quran_time = general.getQuranTime(random_number,last_azan.get("azan_time"))
    print(quran_time)

__init__()