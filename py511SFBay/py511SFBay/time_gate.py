###  When enabled, the timegate should display the data only during the times

## Person has two lists, home list and work list
## Home list shows up in the morning when leaving
## Work list shows up in the evening when leaving


# Setup prompts you to create lists
# Default Home list
# Default Work list
# Add morning times
# Add evening times
# Ending setup should set timer for next day
# Next Day displays morning list 
# When time exceeds the morning time, timer set for evening, and display shut down
#

# this runs a program the next day at a set time
from datetime import datetime
from threading import Timer

x=datetime.today()
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def hello_world():
    print "hello world"
    #...

t = Timer(secs, hello_world)
t.start()

# This checks to see if the date is between two times, and then runs a program
import datetime

day_of_week = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
time = datetime.datetime.now().time()

if day_of_week < 5 and (time > datetime.time(8) and time < datetime.time(14,15)):
    do_something()