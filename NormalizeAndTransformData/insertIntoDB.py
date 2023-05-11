# This script loads a CSV file named "yourcsv.csv" into a pandas dataframe and then inserts the data into a MySQL table named "yourtable". 
# The script connects to a MySQL database with the given credentials, splits the datetime string in the 'time' column into separate date and time columns, 
# converts the date and time strings to datetime objects, and inserts the data into the MySQL table. 
# Once the data has been inserted, the script commits the changes to the database and closes the cursor and connection.



import pandas as pd
import pymysql

# Connect to MySQL database
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='password',
                             database='database')

# Load CSV file into pandas dataframe
df = pd.read_csv('yourcsv.csv', header=None, names=['time', 'status', 'amount'])

# Split datetime string and convert to datetime object
df['time'] = pd.to_datetime(df['time'].str.split(',', expand=True)[0], format="%Y-%m-%d %H:%M:%S")

# Insert data into MySQL table
cursor = connection.cursor()
for index, row in df.iterrows():
    sql = "INSERT INTO yourtable (time, status, amount) VALUES (%s, %s, %s)"
    cursor.execute(sql, (row['time'], row['status'], row['amount']))

connection.commit()
cursor.close()
connection.close()
