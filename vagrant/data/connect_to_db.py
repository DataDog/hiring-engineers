import psycopg2
import time
from random import randint

hostname = 'localhost'
username = 'dummy'
password = 'dummy'
database = 'dummy'

while 1:
    print('Opening Connection')
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    con_num = randint(1,20)
    for i in range(con_num):
        print('Run a select')
        cur.execute('SELECT * FROM dummy')
        time.sleep(5*i)
    print('Closing Connection')
    con.close()