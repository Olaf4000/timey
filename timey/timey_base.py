from util import csv_util as cu


def start_session(description):
    last_entry = cu.read_last_entry()

    if last_entry[1] == "start":
        raise ValueError("Can not start a session. There is a active session!")

    cu.write_time_entry("start", description)
    print(f"i> Started session {description}!")


def end_session():
    last_entry = cu.read_last_entry()

    if last_entry[1] == "end":
        print("!> There is no active session to end")
        return

    cu.write_time_entry("end", last_entry[2])
    print(f"i> Ended session {last_entry[2]}!")


def restart_session():
    last_entry = cu.read_last_entry()

    if last_entry[1] == "end":
        cu.remove_last_entry()

    else:
        print("!> There is no session to restart")
        raise ValueError("There is no session to restart")


def switch_session(description):
    last_entry = cu.read_last_entry()

    if last_entry[1] == "end":
        raise ValueError("There is no session active session to switch from")

    else:
        end_session()
        start_session(description)
