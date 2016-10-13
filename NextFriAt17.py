import datetime, time


def nextFriAt17():
    today = datetime.date.today()
    todayAt17 = datetime.datetime(today.year, today.month, today.day, 17)
    nextFridayAt17 = todayAt17 + datetime.timedelta(11 - today.isoweekday())

    #print ("nextFridayAt17="), nextFridayAt17
    str_fridayAt17 = nextFridayAt17.strftime("%Y-%m-%d-%H")
    unix_fridayAt17 = time.mktime(datetime.datetime.strptime(str_fridayAt17, "%Y-%m-%d-%H").timetuple())
    next_Friday = str(int(unix_fridayAt17))
    return next_Friday
