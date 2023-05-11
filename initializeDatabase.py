# this script creates all the necessary SQL structure for the case

import mysql.connector

# Connect to MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

# Create cursor object
mycursor = mydb.cursor()

# Execute SQL commands to create tables
mycursor.execute("CREATE DATABASE cwtask1;")
mycursor.execute("USE cwtask1;")
mycursor.execute("""
  CREATE TABLE hourly_data01 (
    id INT PRIMARY KEY,
    date DATE,
    hour INT,
    value FLOAT
  );
""")
mycursor.execute("""
  CREATE TABLE hourly_data02 (
    id INT PRIMARY KEY,
    date DATE,
    hour INT,
    value FLOAT
  );
""")
mycursor.execute("""
  CREATE TABLE transactions01 (
    time TIMESTAMP,
    status VARCHAR(50),
    amount INT
  );
""")
mycursor.execute("""
  CREATE TABLE transactions02 (
    time TIMESTAMP,
    status VARCHAR(50),
    amount INT
  );
""")
mycursor.execute("""
  CREATE TABLE requests (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    cpf VARCHAR(50),
    cvc VARCHAR(50),
    expiration_date VARCHAR(50),
    credit_card_number VARCHAR(50)
  );
""")
mycursor.execute("""
  CREATE TABLE summary (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    time DATETIME NOT NULL,
    status VARCHAR(255) NOT NULL,
    amount INT NOT NULL
  );
""")

# Commit changes and close connection
mydb.commit()
mycursor.close()
mydb.close()
