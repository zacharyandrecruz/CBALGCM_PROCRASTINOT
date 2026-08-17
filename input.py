"""
CBALGCM Project — Input Handlers
---------------------------------------------
Handles all 4 raw user inputs feeding the FSM's boolean/mood transitions.
"""

from datetime import datetime

ERROR = -1  

VALID_MOODS = {1, 2, 3, 4}

# Accepted representations
TRUE_VALUES = {True, 1, "1", "y", "yes", "true"}
FALSE_VALUES = {False, 0, "0", "n", "no", "false"}


# ---------------------------------------------------------------------------
# Seperate datetime collection 
# ---------------------------------------------------------------------------

def collect_deadline_datetime():
    """
    Returns:
        datetime: the deadline as a datetime object.
    """
    while True:
        try:
            year = int(input("Deadline year (e.g. 2026): "))
            month = int(input("Deadline month (1-12): "))
            day = int(input("Deadline day (1-31): "))
            hour = int(input("Deadline hour (0-23): "))
            minute = int(input("Deadline minute (0-59): "))

            return datetime(year, month, day, hour, minute)

        except ValueError as e:
            print(f"Invalid date/time ({e}). Please try again.\n")


# ---------------------------------------------------------------------------
# 2nd boolean input
# ---------------------------------------------------------------------------

def get_time_left_days(deadline_datetime, current_datetime=None):
    """
    Calculates the number of days remaining until the deadline.
    """
    if not isinstance(deadline_datetime, datetime):
        raise TypeError(
            f"deadline_datetime must be a datetime object, got {type(deadline_datetime).__name__}"
        )

    if current_datetime is None:
        current_datetime = datetime.now()

    delta = deadline_datetime - current_datetime
    return delta.total_seconds() / 86400


def is_time_left_greater(deadline_datetime, task_length_days, current_datetime=None):
    """
    2nd boolean input - is time until deadline > time it takes to do the task?
    
    """
    
    if isinstance(task_length_days, bool) or not isinstance(task_length_days, (int, float)):
        return ERROR
    if task_length_days < 0:
        return ERROR

    try:
        time_left_days = get_time_left_days(deadline_datetime, current_datetime)
    except TypeError:
        return ERROR

    return 1 if time_left_days > task_length_days else 0


# ---------------------------------------------------------------------------
# 1st and 3rd boolean inputs
# ---------------------------------------------------------------------------

def _normalize_yes_no(value):
    """
    converts yes/no inputs into 1, 0, or ERROR.

    Args:
        value: bool, int, or str representing a yes/no answer.

    Returns:
        int: 1  = yes
             0  = no
            -1  = error
    """
    if isinstance(value, str):
        value = value.strip().lower()

    if value in TRUE_VALUES:
        return 1
    if value in FALSE_VALUES:
        return 0
    return ERROR


def is_delegatable(value):
    """
    Returns:
        int: 1  = yes
             0  = no
            -1  = error
    """
    return _normalize_yes_no(value)


def has_significant_grade_impact(value):
    """
    Args:
        value: bool, int (0/1), or str ("yes"/"no", "y"/"n", "1"/"0") answer
            to "does this task have a significant impact on your grade?"

    Returns:
        int: 1  = yes
             0  = no
            -1  = error
    """
    return _normalize_yes_no(value)


# ---------------------------------------------------------------------------
# Mood input
# ---------------------------------------------------------------------------

def get_mood(value):
    """
    Returns:
        int = the mood value (1-4) if valid, 
        -1  = error
    """
    if isinstance(value, str):
        value = value.strip()
        if not value.isdigit():
            return ERROR
        value = int(value)

    if isinstance(value, bool) or not isinstance(value, int):
        return ERROR

    if value not in VALID_MOODS:
        return ERROR

    return value