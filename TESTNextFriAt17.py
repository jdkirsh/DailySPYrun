import datetime, time
from dateutil.relativedelta import relativedelta, TH

def next_thursdayAt17():
    today = datetime.date.today()
    ref_date = datetime.datetime(today.year, today.month, today.day, 17)
    _next_thursdayAt17 = ref_date + relativedelta(weekday=TH)
    print ("_next_thursdayAt17=", _next_thursdayAt17)
    str_thursdayAt17 = _next_thursdayAt17.strftime("%Y-%m-%d-%H")
    unix_thursdayAt17 = time.mktime(datetime.datetime.strptime(str_thursdayAt17, "%Y-%m-%d-%H").timetuple())
    Str_unix_thursdayAt17 = str(int(unix_thursdayAt17))
    print ("Str_unix_thursdayAt17=", Str_unix_thursdayAt17)
    return Str_unix_thursdayAt17



def nextFriAt17():
    today = datetime.date.today()
    todayAt17 = datetime.datetime(today.year, today.month, today.day, 17)
    nextFridayAt17 = todayAt17 + datetime.timedelta(11 - today.isoweekday())

    print ("nextFridayAt17="), nextFridayAt17
    str_fridayAt17 = nextFridayAt17.strftime("%Y-%m-%d-%H")
    unix_fridayAt17 = time.mktime(datetime.datetime.strptime(str_fridayAt17, "%Y-%m-%d-%H").timetuple())
    next_Friday = str(int(unix_fridayAt17))
    print "next_Friday=", next_Friday
    return next_Friday


# ######################## Main ########################
if __name__ == '__main__':
    #nextFriAt17()

    next_thursdayAt17()

    print ("From Web:", time.ctime(int("1476403200")) )

    # print ( time.strftime("%D %H:%M", time.localtime(int("1284101485"))) )
