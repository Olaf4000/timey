import argparse
import datetime

from dotenv import load_dotenv

from timey import timey_base, timey_info, timey_help
from util import boxprinter as bp
from util import csv_util as cu
from util import util
from util.util import clear_terminal

load_dotenv()

exit_flag = 0
last_output = []

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", type=str)
args = parser.parse_args()

skip_user_input = False

if args.cmd:
    skip_user_input = True

while exit_flag == 0:
    util.clear_terminal()

    bp.print_box_ml(["Welcome to Timey!", "Version: 0.1"])

    # printing latest entry info
    current_session_entry = cu.read_last_entry()

    if current_session_entry[1] == "start":
        current_session = current_session_entry[2]

        bp.print_box_ml([f"Current session: ",
                         f"> Name: {current_session}",
                         f"> Start time: {current_session_entry[0]}"
                         ], appending=1)

    else:
        bp.print_box_sl("No current session", appending=1)

    if last_output:
        bp.print_box_ml(last_output, appending=1)

    last_output = []

    # user input
    if not skip_user_input:
        print("i> Please enter a command:")
        user_input = input("> ")
    else:
        user_input = args.cmd
        skip_user_input = False

    user_input_arr = user_input.split()

    if len(user_input_arr) == 0:
        # last_output.append("No command specified")
        print("!> No command specified")

    elif user_input_arr[0] == "help" or user_input_arr[0] == "h":
        try:
            timey_help.basic_help()

        except:
            print("!> Failed to enter help page!")
            last_output.append("Failed to enter help page!")

    elif user_input_arr[0] == "start":
        try:
            last_output.append(f"Started session {user_input_arr[1]}!")
            timey_base.start_session(user_input_arr[1])

        except:
            print("!> Error while starting the session!")
            last_output.append("Error while starting the session!")

    elif user_input_arr[0] == "end":
        try:
            timey_base.end_session()
            last_output.append(f"Ended session!")

        except:
            print("!> Error while ending the session!")
            last_output.append("Error while ending the session!")

    elif user_input_arr[0] == "restart":
        try:
            timey_base.restart_session()
            last_output.append(f"Restarted session!")

        except:
            print("!> Error while restarting the session!")
            last_output.append("Error while restarting the session!")

    # info
    elif user_input_arr[0] == "info":
        try:
            timey_info.info()

        except:
            last_output.append("Error with info!")
            print("!> Error with info!")

    # info day
    elif user_input_arr[0] == "info_day":
        try:
            try:
                timey_info.info_day(user_input_arr[1])

            except:
                timey_info.info_day()

        except:
            last_output.append("Error with info_day!")
            print("!> Error with info_day!")

    # info week
    elif user_input_arr[0] == "info_week":
        try:
            try:
                timey_info.info_week(datetime.datetime.strptime(user_input_arr[1], "%Y-%m-%d").date())

            except:
                timey_info.info_week()

        except:
            last_output.append("Error with info_week!")
            print("!> Error with info_week!")

    elif user_input_arr[0] == "quit" or user_input_arr[0] == "q":
        print("i> Exiting ...")
        exit_flag = 1
        clear_terminal()
