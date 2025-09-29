import csv
import datetime
import os

from dotenv import load_dotenv

load_dotenv()
time_filename = os.getenv('TIMEY_TIME_FILE_PATH')


def write_time_entry(type, description):
    data = [datetime.datetime.now(), type, description]
    file = time_filename

    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def read_last_entry():
    import csv

    file_name = time_filename
    last_row = None

    with open(file_name, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

        if rows:
            last_row = rows[-1]

    return last_row


def remove_last_entry():
    # Read all rows from the CSV
    with open(time_filename, 'r', newline='', encoding='utf-8') as infile:
        reader = list(csv.reader(infile))

    # Remove the last row if there is at least one
    if reader:
        reader = reader[:-1]

    # Write back to a new CSV file
    with open(time_filename, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(reader)
