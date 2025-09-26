import math

def print_line_bar(width):
    print("+", end="")
    
    for i in range(width):
        print("-", end="")

    print("+")

def print_empty_bar(width):
    print("|", end="")
    
    for i in range(width):
        print(" ", end="")

    print("|")

def print_text_bar(width, text):
    if (len(text) > (width - 2)):
        text = text[:(width - 2)]

    print("|", end="")
    
    print(" " + text, end="")
    for i in range((width - 2) - len(text)):
        print(" ", end="")

    print(" |")

def print_box_sl(width, text, appending = 0):
    chunks = [text[i:i + width - 2] for i in range(0, len(text), (width - 2))]

    if appending == 0:
        print_line_bar(width)

    print_empty_bar(width)

    for c in chunks:
        print_text_bar(width, c)

    print_empty_bar(width)
    print_line_bar(width)

def print_box_ml(width, text, appending = 0):
    all_chunks = []
    
    for t in text:
        chunks = [t[i:i + width - 2] for i in range(0, len(t), (width - 2))]
        all_chunks.append(chunks)

    if appending == 0:
        print_line_bar(width)

    print_empty_bar(width)

    for ac in all_chunks:
        for c in ac:
            print_text_bar(width, c)
        

    print_empty_bar(width)
    print_line_bar(width)
