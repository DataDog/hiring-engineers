#!/usr/bin/python
import schedule
import time
import psycopg2
import random
from configparser import ConfigParser # module to read our config file

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser() # create our parser
    parser.read(filename) # parse database.ini
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1] # populate our db config object
    else:
        raise Exception('section {0} not found in {1}'.format(section, filename))
    return db

count = 1

def connect():
    conn = None
    try:
        # read in our config obj
        params = config()
        conn = psycopg2.connect(**params) # connect to our db
        # create our db cursor
        cur = conn.cursor()
        rnd = random.randint(1,1001) # number to insert as our value
        rows = random.randint(1,11) # amount of rows to insert
        global count # so we can use count as a global variable
        if (count == 50):
            rows = 200 # at our 50th call to this function let's add A LOT of rows
        # insert a random nmber into our numbers table
        for i in range(rows):
            cur.execute("INSERT INTO numbers VALUES (%s)", (rnd,))
        count += 1 # increment our counter
        conn.commit() # commit our transaction
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback() # rollback since we've had an error
        print(error)
    finally:
        if conn is not None:
            conn.close() # close our connection
            print('Database connection closed.')

schedule.every(10).seconds.do(connect)

# only run if we're not importing this into a different module
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
