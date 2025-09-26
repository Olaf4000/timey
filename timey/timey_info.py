import datetime
import os

import pandas as pd
from dotenv import load_dotenv

from util import boxprinter as bp
from util.util import clear_terminal

load_dotenv()
time_filename = os.getenv('TIMEY_TIME_FILE_PATH')


def aggregate_df_with_duration(df):
    df = df.sort_values("timestamp").reset_index(drop=True)
    pairs = df.pivot(index="description", columns="type", values="timestamp").reset_index()
    pairs["duration"] = pairs["end"] - pairs["start"]
    return pairs


def info_menu(title_text):
    bp.print_box_ml(title_text)


def generate_progress_bar(bar_length, percent_completed):
    bar_length -= 9

    if percent_completed >= 100:
        output_string = "["
        for i in range(bar_length):
            output_string += os.getenv("BAR_CHARACTER_1")
        output_string += "] "
        output_string += f"{str(round(percent_completed))}%"
        return output_string

    completed_section = round(bar_length * (percent_completed / 100))

    output_string = "["

    for i in range(completed_section):
        output_string += os.getenv("BAR_CHARACTER_1")

    for i in range(bar_length - completed_section):
        output_string += os.getenv("BAR_CHARACTER_2")

    output_string += "] "
    if percent_completed < 100:
        output_string += " "
        output_string += f"{str(round(percent_completed))}%"
    elif percent_completed < 10:
        output_string += " "
        output_string += f"{str(round(percent_completed))}%"
    else:
        output_string += f"{str(round(percent_completed))}%"

    return output_string


def get_worked_minutes_of_day(date):
    try:
        df = pd.read_csv(time_filename)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        mask = df["timestamp"].dt.date == pd.to_datetime(date).date()
        df_filtered_to_day = df.loc[mask]
        df_aggregated = aggregate_df_with_duration(df_filtered_to_day)

        return df_aggregated["duration"].sum().total_seconds() / 60

    except:
        return 0


def get_vis_hours_and_minutes(minutes):
    return [round(minutes // 60), round(minutes % 60)]


def info_day(date=datetime.datetime.now().date()):
    worked_minutes = get_worked_minutes_of_day(date)
    workday_completion = round((worked_minutes / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)

    vis_worked_hours = get_vis_hours_and_minutes(worked_minutes)[0]
    vis_worked_minutes = get_vis_hours_and_minutes(worked_minutes)[1]

    # visuals
    clear_terminal()
    info_menu(["Workday statistics - Day", f"Date: {date}"])
    bp.print_box_ml([
        f"You worked: {vis_worked_hours}h and {vis_worked_minutes}m of {int(os.getenv('WORKDAY_LENGTH')) / 60}h",
        generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")), workday_completion)
    ],
        appending=1)

    input("Hit Enter to return to menu")


def info_week(date=datetime.datetime.now().date()):
    weekdays = [(date - datetime.timedelta(days=date.weekday())) + datetime.timedelta(days=i) for i in
                range(5)]  # determines the dates for the weekdays of the specified week

    weekly_worked_minutes = 0
    for d in weekdays:
        weekly_worked_minutes += get_worked_minutes_of_day(d)

    workweek_completion = round((weekly_worked_minutes / int(os.getenv("WORKWEEK_LENGTH"))) * 100, 2)

    vis_worked_hours = get_vis_hours_and_minutes(weekly_worked_minutes)[0]
    vis_worked_minutes = get_vis_hours_and_minutes(weekly_worked_minutes)[1]

    # visuals
    clear_terminal()

    info_menu(["Workday statistics - Week", f"Date: From {weekdays[0]} to {weekdays[-1]}"])

    bp.print_box_ml([
        f"You worked: {vis_worked_hours}h and {vis_worked_minutes}m of {int(os.getenv('WORKWEEK_LENGTH')) / 60}h",
        generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")), workweek_completion),
        " ",
        "Mon: " + generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[0]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Tue: " + generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[1]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Wed: " + generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[2]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Thu: " + generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[3]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Fri: " + generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[4]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
    ], appending=1)

    input("Hit Enter to return to menu")
