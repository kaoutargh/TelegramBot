import datetime
import pytz

def get_ukraine_time():
    ukraine_timezone = pytz.timezone('Europe/Kiev')
    ukraine_time = datetime.datetime.now(ukraine_timezone)
    return ukraine_time
 

def is_weekend():
    today = datetime.date.today()
    return today.weekday() in [5, 6]

