#!usr/bin/python

import time
from apcaccess import status as apc

def updateUPSData():
    return apc.parse(apc.get(host='0.0.0.0'), strip_units=True)

def printAll():
    for item in ups_data:
        print (item, ups_data[item])

def calculateWatts():
    ups_data = updateUPSData()
    power = float(ups_data.get('NOMPOWER'))
    load = float(ups_data.get('LOADPCT'))
    return power * load * 0.01

def timeAndWatts():
    watts = calculateWatts()
    timeOfWattsCall = round(time.time(), 2)
    return timeOfWattsCall, watts

def main():
    while(True):
        #print ( "watts: {:.1f}".format(calculateWatts()) )
        print (timeAndWatts())
        time.sleep(10)

if __name__ == "__main__":
    main()


