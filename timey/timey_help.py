from util import boxprinter as bp
from util.util import clear_terminal


def basic_help():
    clear_terminal()

    bp.print_box_sl("Welcome to Timeys help page!")
    bp.print_box_ml([
        "Commands: ",
        "> help or h - opens this page",
        " > start $session_name - starts new session",
        " > stop - stops current session",
        " > info - get an overview of your projects",
        " > info_day $YYYY-MM-DD(opt.) - stats of the specified date. If not specified, the current date will be used.",
    ], appending=1)

    input("Hit Enter to return to menu")
