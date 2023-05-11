# This script reads a CSV file named "yourcsv.csv" and normalizes the time column in the file.
# It removes the "h" character from the time value and adds the current date to the time value, creating a timestamp. 
# The normalized data is written to a new CSV file named "yourNormalizedcsv.csv". 
# The output file contains the same data as the input file, but with the time column normalized.

import csv
from datetime import datetime

# Set the date format and current date
date_format = '%Y-%m-%d %H:%M:%S'
current_date = datetime.now().date()

# Define a function to convert the time value to a timestamp
def convert_time(time_str):
    # Remove the "h" character and split the hours and minutes
    hours, minutes = time_str.replace('h', '').split()

    # Concatenate the current date with the hours and minutes, and add ":00" for the seconds
    time_str = f'{current_date} {hours}:{minutes}:00'

    # Parse the datetime string and format it as a timestamp
    time = datetime.strptime(time_str, date_format)
    return time.strftime(date_format)

# Open the input CSV file and create a new CSV file for output
with open('yourcsv.csv', 'r') as input_file, open('yourNormalizedcsv.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate through the rows and convert the time values
    for row in reader:
        if row[0] == 'time':
            # Skip the header row
            continue
        else:
            # Convert the time value to a timestamp
            row[0] = convert_time(row[0])
            writer.writerow(row)