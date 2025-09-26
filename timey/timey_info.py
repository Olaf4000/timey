import datetime
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()
time_filename = os.getenv('TIMEY_TIME_FILE_PATH')

def info_day(date=datetime.datetime.now().date()):
    df = pd.read_csv("your_file.csv")

    input("Hit Enter to return to menu")