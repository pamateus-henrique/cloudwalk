# This script connects to a MySQL database and retrieves the latest summary time from the summary table. 
# It then selects transactions that haven't been summarized yet from the requests table, groups them by status and minute, and inserts the summarized data into the summary table. 
# Finally, it closes the database connection.


import mysql.connector
from datetime import datetime, timedelta

# Connect to the database
mydb = mysql.connector.connect(
    host="hostname",
    user="username",
    password="password",
    database="cwtask1"
)

# Get the current time and the last time a row was inserted into the summary table
cursor = mydb.cursor()
cursor.execute("SELECT MAX(time) FROM summary")
result = cursor.fetchone()
last_summary_time = result[0] if result[0] else datetime.min
current_time = datetime.now()

# Select the transactions that haven't been summarized yet
cursor.execute("""
    SELECT status, DATE_FORMAT(time, '%Y-%m-%d %H:%i:00') AS time, COUNT(*) AS amount
    FROM requests
    WHERE time > %s
    GROUP BY status, DATE_FORMAT(time, '%Y-%m-%d %H:%i:00')
""", (last_summary_time,))

# Consume the results of the first query
result = cursor.fetchall()

# Insert the summarized data into the summary table
for (status, time, amount) in result:
    print(status)
    print(time)
    print(amount)
    cursor.execute("""
        INSERT INTO summary (status, time, amount)
        VALUES (%s, %s, %s)
    """, (status, time, amount))
    mydb.commit()

# Close the database connection
mydb.close()
