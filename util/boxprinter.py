import os

from dotenv import load_dotenv

load_dotenv()

width = int(os.getenv("TEXTBOX_WIDTH"))


def print_line_bar():
    print("+", end="")

    for i in range(width):
        print("-", end="")

    print("+")


def print_empty_bar():
    print("|", end="")

    for i in range(width):
        print(" ", end="")

    print("|")


def print_text_bar(text):
    if len(text) > (width - 2):
        text = text[:(width - 2)]

    print("|", end="")

    print(" " + text, end="")
    for i in range((width - 2) - len(text)):
        print(" ", end="")

    print(" |")


def print_box_sl(text, appending=0):
    chunks = [text[i:i + width - 2] for i in range(0, len(text), (width - 2))]

    if appending == 0:
        print_line_bar()

    print_empty_bar()

    for c in chunks:
        print_text_bar(c)

    print_empty_bar()
    print_line_bar()


def print_box_ml(text, appending=0):
    all_chunks = []

    for t in text:
        chunks = [t[i:i + width - 2] for i in range(0, len(t), (width - 2))]
        all_chunks.append(chunks)

    if appending == 0:
        print_line_bar()

    print_empty_bar()

    for ac in all_chunks:
        for c in ac:
            print_text_bar(c)

    print_empty_bar()
    print_line_bar()
