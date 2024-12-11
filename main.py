import packages.general as general
import packages.file_system as file_system

def __init__():
    last_azan = general.getLastAzanTime()
    if last_azan is None:
        return None
    random_number = general.getRandomNumberFromFile(file_system.INFO_FILE_PATH)
    print(last_azan)
    print(random_number)

__init__()