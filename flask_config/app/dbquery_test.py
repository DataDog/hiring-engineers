import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(user='datadog', password='datadog',
                              host='mysql1', port='3306')


    sql_select_Query = "SELECT * FROM classicmodels.city_stats"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in city_stats is: ", cursor.rowcount)

    print("\nPrinting each laptop record")
    for row in records:
        print("Id = ", row[0], )
        print("City = ", row[1])
        print("Rank = ", row[2])
        print("Population  = ", row[3], "\n")

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("MySQL connection is closed")



