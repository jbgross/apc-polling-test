#!usr/bin/python

import os # ... tbd
import time # wait for 1 min with sleep(60)
import sqlite3 # database
# to get apcaccess use -> pip install apcaccess
from apcaccess import status as apc


def remove_irrelevant_data(data, remove_keys):
    for key in remove_keys:
        data.pop(key, None)

def output_key_values(data):
    for key in data:
        print key, data[key], type(data[key])

def calculate_watts(data):
    return float(data.get('NOMPOWER')) * 0.01 * float(data.get('LOADPCT', 0.0))

def create_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("""CREATE TABLE entries (
            algo text,
            watts real)""")
    conn.commit()

    return conn, c

def main():
    local_host = '0.0.0.0' # this is the default

    unnecessary_keys = [
            'DATE', 
            'HOSTNAME', 
            'VERSION', 
            'UPSNAME', 
            'CABLE', 
            'DRIVER', 
            'UPSMODE', 
            'STARTTIME', 
            'MODEL', 
            'ALARMDEL', 
            'SEFTEST', 
            'STATFLAG', 
            'SERIALNO', 
            'BATTDATE', 
            'FIRMWARE', 
            'END APC'
    ]

    # make db (conn) and get cursor (c)
    conn, c = create_db()
    
    time_elapsed = 0
    ups_update_time = 10
    time_start = time.time()
    
    while time_elapsed < 600:
        # retrieve data from ups
        ups_data = apc.parse(apc.get(host=local_host), strip_units=True)
        retrieve_data_time = time.time()
        
        remove_irrelevant_data(ups_data, unnecessary_keys)
        watts = calculate_watts(ups_data)

        c.execute("INSERT INTO entries VALUES (?,?)", ("algo1", watts))
        conn.commit()

        time_end = time.time()
        time_elapsed = time_end - time_start
        #print watts, time_elapsed
        print ups_data.get('NOMPOWER'), ups_data.get('LOADPCT')
        
        time_bef_wait = time.time()
        time.sleep(ups_update_time - (time_bef_wait - retrieve_data_time) )

    c.execute("SELECT * FROM entries WHERE algo=?", ("algo1",))
    print(c.fetchall())

if __name__ == '__main__':
    main()
