import os

def clear_terminal():
    """Clears the terminal screen."""
    # Check if the operating system is Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Or if it's a Unix-like system (Linux, macOS, etc.)
    else:
        _ = os.system('clear')
