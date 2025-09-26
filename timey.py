from util import boxprinter as bp
from util import csv_util as cu
from util import util

from timey import timey_base, timey_info

textbox_width = 50
exit_flag = 0
last_output = []

while exit_flag == 0:
    util.clear_terminal()

    bp.print_box_ml(textbox_width, ["Welcome to Timey!", "Version: 0.1"])

    # printing latest entry info
    current_session_entry = cu.read_last_entry()

    if current_session_entry[1] == "start":
        current_session = current_session_entry[2]

        bp.print_box_ml(textbox_width, [f"Current session: ", 
                                        f"> Name: {current_session}", 
                                        f"> Start time: {current_session_entry[0]}"
                                        ], appending=1)

    else:
        bp.print_box_sl(textbox_width, "No current session", appending=1)

    if last_output != []:
        bp.print_box_ml(textbox_width, last_output, appending=1)


    last_output = []
    
    #user input
    print("> Please enter a command:")
    user_input = input("> ")
    user_input_arr = user_input.split()

    if len(user_input_arr) == 0:
        last_output.append("No command specified")
        print("!> No command specified")

    elif user_input_arr[0] == "help":
        print("help")

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

    elif user_input_arr[0] == "info_day":
        try:
            timey_info.info_day()

        except:
            last_output.append("Error!")
            print("!> Error!")
    
    elif user_input_arr[0] == "quit" or user_input_arr[0] == "q":
        print("i> Exiting ...")
        exit_flag = 1
            