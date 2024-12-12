from datetime import datetime,timedelta
import packages.general as general
import time

# Get today with dd/mm/yyyy
def getTodayDate():
    return datetime.today().strftime('%d/%m/%Y')

# Get current time with hh:mm in 24-hours format
def getCurrentTime():
    return datetime.now().strftime("%H:%M")

# Compare today with other day and return -1 if today is greater, 1 if other day is greater and 0 if there both are equals
def compareTodayWith(day):
    today = datetime.strptime(getTodayDate(), '%d/%m/%Y')
    day = datetime.strptime(day, '%d/%m/%Y')
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
    time_diff = (target_time - now).total_seconds()
    if(time_diff<0):
        return
    time.sleep(time_diff)