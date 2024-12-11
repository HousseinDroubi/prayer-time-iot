from datetime import datetime

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