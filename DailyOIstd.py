import shutil
import datetime, time
from dateutil.relativedelta import relativedelta, TH

def next_thursdayAt17():
    today = datetime.date.today()
    ref_date = datetime.datetime(today.year, today.month, today.day, 17)
    _next_thursdayAt17 = ref_date + relativedelta(weekday=TH)
    #print ("_next_thursdayAt17=", _next_thursdayAt17)
    str_thursdayAt17 = _next_thursdayAt17.strftime("%Y-%m-%d-%H")
    unix_thursdayAt17 = time.mktime(datetime.datetime.strptime(str_thursdayAt17, "%Y-%m-%d-%H").timetuple())
    Str_unix_thursdayAt17 = str(int(unix_thursdayAt17))
    #print ("Str_unix_thursdayAt17=", Str_unix_thursdayAt17)
    return Str_unix_thursdayAt17


def archive(file_name):
    _archive_name = file_name + datetime.datetime.now().strftime("%Y%m%d-%H%M%S" )
    try:
        shutil.copyfile(file_name, _archive_name)
    except EnvironmentError:
        print ("Fatal Error on: ", file_name )



# ######################## Main ########################
if __name__ == '__main__':
    archive("zbab.csv")
