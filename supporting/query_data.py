"""
Randomly query database table to generate metrics
"""
import random
from time import sleep

import mysql.connector
from mysql.connector import Error

def query(conn):
    """
    Send random query to the database
    """

    cursor = conn.cursor()
    cursor.execute('select * from test')
    records = cursor.fetchall()
#    for row in records:
#        print("Id = ", row[0])
#        print("Name = ", row[1])
    cursor.close()

def main():
    """
    Main function to this script
    """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='setest',
                                       user='datadog',
                                       password='datadog')
        while True:
            query(conn)
            sleep(random.randint(1, 2000) / float(1000))

    except Error as mysqle:
        print ("Error while connecting to MySQL", mysqle)

    finally:
        if conn and conn.is_connected():
            conn.close()
            print "MySQL connection is closed"

if __name__ == '__main__':
    main()
