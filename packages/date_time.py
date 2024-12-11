from datetime import datetime

# Get today with dd/mm/yyyy
def getTodayDate():
    return datetime.today().strftime('%d/%m/%Y')


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



