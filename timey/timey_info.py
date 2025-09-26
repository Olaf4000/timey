import datetime
import os

from dotenv import load_dotenv

from timey import timey_util
from util import boxprinter as bp
from util.util import clear_terminal

load_dotenv()
time_filename = os.getenv('TIMEY_TIME_FILE_PATH')

import pandas as pd


def info_menu(title_text):
    bp.print_box_ml(title_text)


def get_worked_minutes_of_day(date):
    try:
        df = pd.read_csv(time_filename)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        mask = df["timestamp"].dt.date == pd.to_datetime(date).date()
        df_filtered_to_day = df.loc[mask]
        df_aggregated = timey_util.aggregate_df_with_duration(df_filtered_to_day)

        return df_aggregated["duration"].sum().total_seconds() / 60

    except:
        return 0


def get_vis_hours_and_minutes(minutes):
    return [round(minutes // 60), round(minutes % 60)]


# Menu pages

def info_drill_down(description):
    df = pd.read_csv(time_filename)
    df_filtered = df[df["description"] == description]
    df_combined = timey_util.pair_start_end(df_filtered)

    clear_terminal()

    info_menu([f"Drill down for project: {description}"])

    bp.print_box_ml(
        ["Sessions: "] +
        timey_util.pair_df_to_list(df_combined)
        , appending=1)

    input("Hit Enter to return to menu")


def info():
    exit_flag = False

    df = pd.read_csv(time_filename)
    aggregated_df = timey_util.aggregate_df_with_duration(df)
    unique_descriptions = aggregated_df["description"].unique().tolist()

    box_text = ["Projects:"]

    for description in unique_descriptions:
        dur = aggregated_df.loc[
            aggregated_df["description"] == description, "duration"
        ].iloc[0]

        if pd.notna(dur):
            dur_str = str(dur.round("S"))
        else:
            dur_str = "n/a"

        box_text.append(" > " + str(description) + ": " + dur_str)

    # running vars
    last_output = []

    # visuals
    while not exit_flag:
        clear_terminal()

        info_menu(["Project overview"])

        bp.print_box_ml(box_text, appending=1)

        if len(last_output) != 0:
            bp.print_box_ml(last_output, appending=1)

        last_output = []

        print("i> Enter project name to see more. \n   Or Hit Enter to return to the menu!")
        user_input = input(">")
        user_input_arr = user_input.split()

        if len(user_input_arr) == 0:
            exit_flag = True
            return
        elif len(user_input_arr) > 0:
            if user_input_arr[0] in unique_descriptions:
                info_drill_down(user_input_arr[0])
            else:
                last_output.append(f"There is no project called {user_input_arr[0]}")


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
        timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")), workday_completion)
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
        timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")), workweek_completion),
        " ",
        "Mon: " + timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[0]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Tue: " + timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[1]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Wed: " + timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[2]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Thu: " + timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[3]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
        "Fri: " + timey_util.generate_progress_bar(int(os.getenv("TEXTBOX_WIDTH")) - 5, round(
            (get_worked_minutes_of_day(weekdays[4]) / int(os.getenv("WORKDAY_LENGTH"))) * 100, 2)),
    ], appending=1)

    input("Hit Enter to return to menu")
