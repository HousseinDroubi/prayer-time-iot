from datetime import datetime,timedelta
import packages.general as general
import time

# Get today with dd/mm/yyyy
def getTodayDate():
    return datetime.today().strftime('%d/%m/%Y')

# Get current time with hh:mm in 24-hours format
def getCurrentTime(is_with_seconds=False):
    if is_with_seconds:
        return datetime.now().strftime("%H:%M:%S")
    return datetime.now().strftime("%H:%M")

# Compare today with other day and return -1 if today is greater, 1 if other day is greater and 0 if there both are equals
def compareDateWith(date,today = None):
    if(not today):
        today = datetime.strptime(getTodayDate(), '%d/%m/%Y')
    else:
        today = datetime.strptime(today,"%d/%m/%Y") 
    day = datetime.strptime(date, '%d/%m/%Y')
    if today>day:
        return 1
    elif day>today:
        return -1
    else:
        return 0

# Compare current time with other time and return -1 if current time is greater, 1 if other time is greater and 0 if there both are equals
def compareCurrentTimeWith(time):
    current_time = datetime.strptime(getCurrentTime(), '%H:%M').time()
    time = datetime.strptime(time, '%H:%M').time()
    if current_time>time:
        return 1
    elif time>current_time:
        return -1
    else:
        return 0
    
# get how many days there is between two dates
def getNumberOfDaysBetweenTwoDates(date_1,date_2):
    date_1_obj = datetime.strptime(date_1, '%d/%m/%Y')
    date_2_obj = datetime.strptime(date_2, '%d/%m/%Y')
    date_diff = date_2_obj - date_1_obj
    return date_diff.days

def removeSecondsFromTime(seconds,time):
    time = datetime.strptime(general.convertIntegerToString(time), "%H:%M")
    time = time - timedelta(seconds=seconds)
    return time.strftime("%H:%M")

# wait function
def waitUntil(wait_until_time):
    now = datetime.now()
    target_time = datetime.strptime(wait_until_time,"%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if isSummerTime():
        target_time = target_time + timedelta(hours=1)
    time_diff = (target_time - now).total_seconds()
    if(time_diff<0):
        return
    print(f"Waiting {time_diff//3600} hours or {time_diff//60} minutes or {time_diff}")
    time.sleep(time_diff)

def getSecondsFromMeghrebToSobuh(sobuh_azan_time):
    current_time = datetime.now()
    given_time = datetime.strptime(sobuh_azan_time, "%H:%M")
    given_time = given_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
    if given_time <= current_time:
        given_time += timedelta(days=1)
    time_difference = given_time - current_time
    seconds_difference = time_difference.total_seconds()
    return seconds_difference

# Here, we called is ramadan tomorrow, because when next day is ramadan we need to wait 
# to time before imsak
def isRamadan(date):
    start_of_ramadan = "01/02/2025"
    end_of_ramadan = "30/03/2025"
    return compareDateWith(start_of_ramadan,today=date)!=-1 and compareDateWith(end_of_ramadan,today=date)!=1

def isSummerTime():
    start_of_summer_time = "01/02/2025"
    end_of_summer_time = "25/10/2025"

    return compareDateWith(start_of_summer_time)!=-1 and compareDateWith(end_of_summer_time)!=1