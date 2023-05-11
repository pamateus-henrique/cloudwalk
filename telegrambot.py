# This script connects to a MySQL database and executes four predefined queries with a delay of 10 seconds between each one. 
# It checks if the queries return any rows and, if so, sends a message to a specified Telegram chat using the Telegram API. 
# The script also prints the executed query to the console.


import telegram
import asyncio
import time
import mysql.connector

# Define the queries to execute
queries = [
    "SELECT t1.* FROM cwtask1.summary t1 JOIN cwtask1.summary t2 ON t1.status = t2.status AND t1.time = t2.time + INTERVAL 1 MINUTE WHERE t1.status = 'denied' AND t1.amount >= t2.amount * 2 AND t1.amount - t2.amount >= 10 AND t1.time >= NOW() - INTERVAL 5 MINUTE",
    "SELECT t1.* FROM cwtask1.summary t1 JOIN cwtask1.summary t2 ON t1.status = t2.status AND t1.time = t2.time + INTERVAL 1 MINUTE WHERE t1.status = 'approved' AND t1.amount >= t2.amount * 2 AND t1.amount - t2.amount >= 10 AND t1.time >= NOW() - INTERVAL 5 MINUTE",
    "SELECT t1.* FROM cwtask1.summary t1 JOIN cwtask1.summary t2 ON t1.status = t2.status AND t1.time = t2.time + INTERVAL 1 MINUTE WHERE t1.status = 'reversed' AND t1.amount >= t2.amount * 2 AND t1.amount - t2.amount >= 10 AND t1.time >= NOW() - INTERVAL 5 MINUTE",
    "SELECT t1.* FROM cwtask1.summary t1 JOIN cwtask1.summary t2 ON t1.status = t2.status AND t1.time = t2.time + INTERVAL 1 MINUTE WHERE t1.status = 'refunded' AND t1.amount >= t2.amount * 2 AND t1.amount - t2.amount >= 10 AND t1.time >= NOW() - INTERVAL 5 MINUTE"
]

# Replace YOUR_TOKEN with the token you received from BotFather
token = 'YOUR_TOKEN'

# Replace YOUR_CHAT_ID with your Telegram chat ID (e.g. 930042393 for the number you provided)
chat_id = 'YOUR_CHAT_ID'

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="cwtask1"
)

# Loop through the queries and execute them with a delay of 3 minutes between each one
while True:
    for query in queries:
        print(f"Executing query: {query}")
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        time.sleep(10)

        # If the query returned more than 0 rows, send a message to Telegram
        if len(rows) > 0:
            status = None
            if "status = 'denied'" in query:
                status = 'denied'
            elif "status = 'approved'" in query:
                status = 'approved'
            elif "status = 'reversed'" in query:
                status = 'reversed'
            elif "status = 'refunded'" in query:
                status = 'refunded'

            if status is not None:
                message = f"An anomaly in the {status} transactions has been found! check it at your Grafana dashboard!"
                bot = telegram.Bot(token=token)
                asyncio.run(bot.send_message(chat_id=chat_id, text=message))
    time.sleep(180)
