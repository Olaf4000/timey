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
