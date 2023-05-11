
# This script connects to a MySQL database and executes a query to select all rows from a table called "yourtable" where the "status" column is set to "approved". 
# It then fetches all rows of the result and writes them to a CSV file called "approved.csv" in the current directory. 
# The script uses the csv module to write the data to the CSV file and closes the cursor and database connection once it is done.

import mysql.connector
import csv

# establish connection to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="password",
  database="cwtask1"
)

# create a cursor to execute queries
cursor = mydb.cursor()

# execute the query
query = "SELECT * FROM yourtable WHERE status = 'approved'"
cursor.execute(query)

# fetch all rows of the result
result = cursor.fetchall()

# create a .csv file and write the data to it
with open('approved.csv', 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile)
  
  # write the header row
  header = ['Time', 'Status', 'Amount']
  csvwriter.writerow(header)
  
  # iterate over the rows and write them to the .csv file
  for row in result:
    csvwriter.writerow(row)

# close the cursor and the database connection
cursor.close()
mydb.close()
