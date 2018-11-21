import sys, os


###### Top exported function ##################################################
def print_split(text, style="simple", width=120, c="*"):
    if style == "simple":
        split_simple(text, width, c="*")
    else:
        split_simple(text, width, c="*")

###### Different style ########################################################
def split_simple(text, width=120, c="*"):
    print_line(width, c)
    print_content_line(text, width, c="*")
    print_line(width, c)

###### Common Functions #######################################################
def print_line(width=80, c="*"):
    print(c * width)

def print_content_line(text, width=120, c="*"):
    l = len(text)
    if l == 0:
        return
    
    # Print char only if width >= len of text more than 4 
    if width >= (l + 4):
        head_space = int((width -2 - l)/2) # minus 2 means one char at head and tail
        # just padding with width - len - 2 chars - head space
        line = c + " " * head_space + text + " " * (width-l-2-head_space) + c 
        print(line)
    else:
        print(text)
