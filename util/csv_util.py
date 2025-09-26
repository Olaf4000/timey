import csv
import datetime

time_filename = 'time.csv'

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
