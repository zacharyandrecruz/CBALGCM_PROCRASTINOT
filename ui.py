"""
CBALGCM Project — UI / Display Layer
---------------------------------------------
All color, banner, and screen-formatting code lives here so main.py can stay
focused on the actual task-management flow.

"""

import os

# On Windows, cmd.exe needs VT100/ANSI processing enabled -- calling
# os.system("") has the side effect of turning this on, with no visible
# output and no extra packages needed. Does nothing on Mac/Linux.
if os.name == "nt":
    os.system("")


# ---------------------------------------------------------------------------
# ANSI color codes
# ---------------------------------------------------------------------------

RESET = "\x1b[0m"
BRIGHT = "\x1b[1m"

RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
CYAN = "\x1b[36m"
WHITE = "\x1b[37m"
LIGHTRED = "\x1b[91m"
LIGHTYELLOW = "\x1b[93m"
GRAY = "\x1b[90m"



FONT = {
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
}

BANNER_TEXT = "PROCRASTINOT"


def render_text(text, spacing=1):
    """
    Args:
        text (str): letters to render (must exist in FONT).
        spacing (int): number of blank columns between letters.

    Returns:
        str: multi-line block-font rendering of text.
    """
    rows = ["" for _ in range(5)]
    for ch in text:
        glyph = FONT[ch]
        for i in range(5):
            rows[i] += glyph[i] + (" " * spacing)
    return "\n".join(rows)


def print_banner():
    print(CYAN + BRIGHT + render_text(BANNER_TEXT) + RESET)
    print(GREEN + BRIGHT + "An app developed to keep track of different task for you to do in priority of what you need!" + RESET + "\n")


# ---------------------------------------------------------------------------
# Screen / section helpers
# ---------------------------------------------------------------------------

def clear_screen():
    """
    Clears the terminal.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_section_header(title):
    print(CYAN + BRIGHT + f"\n--- {title} ---\n" + RESET)


def print_menu_title(title):
    print(CYAN + BRIGHT + f"\n=== {title} ===" + RESET)


def prompt(question):
    """
    Input prompt with "?" prefix
    
    """
    return input(GREEN + BRIGHT + "? " + RESET + WHITE + question + RESET + " ")


def print_menu_option(number, label):
    print(YELLOW + f"  {number}. " + WHITE + label + RESET)


def print_error(message):
    print(RED + message + RESET)


def print_success(message):
    print(GREEN + message + RESET)


def print_info(message):
    print(WHITE + message + RESET)


# ---------------------------------------------------------------------------
# Category colors (view_tasks_flow)
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    0: RED,           # Do Now (High Priority)
    1: LIGHTRED,       # Do Now (Low Priority)
    5: CYAN,           # Ask For Help
    2: YELLOW,         # Schedule
    4: LIGHTYELLOW,    # Delegate
    3: GREEN,          # Can Procrastinate
    -1: GRAY,          # Error Found
}


def print_category_header(label, category):
    color = CATEGORY_COLORS.get(category, WHITE)
    print(color + BRIGHT + f"\n{label}:" + RESET)
    return color


TASK_TYPE_LABELS = {0: "Submit by", 1: "Prepare for"}


def print_task_line(task, color):
    formatted_date = task.date.strftime("%b %d, %Y at %I:%M %p")
    verb = TASK_TYPE_LABELS.get(getattr(task, "type", 0), "Due")
    print(color + f"  - {task.name} ({verb} {formatted_date})" + RESET)