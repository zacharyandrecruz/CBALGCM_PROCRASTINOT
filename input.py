"""
CBALGCM Project — Input Handlers
---------------------------------------------
Handles all 4 raw user inputs feeding the FSM's boolean/mood transitions.

1st boolean input: can this task be delegated / is this task a group work?
    Output: 1 if yes, 0 if no, -1 if error

2nd boolean input: is time until deadline > time it takes to do the task?
    Deadline is collected via collect_deadline_datetime() (prompts for year,
    month, day, hour, minute separately and returns a datetime object).
    Task length is given in days.
    Output: 1 if time_left > time_required  (Not Urgent)
            0 if time_left <= time_required (Urgent)
           -1 if error (not a datetime object, bad task length, etc.)

3rd boolean input: does this task have a significant impact on your grade?
    Output: 1 if yes, 0 if no, -1 if error

Mood input: user's current mood/energy level
    1 = motivated
    2 = easy tasks only plz
    3 = super tired
    4 = im deadge
    Output: 1-4 if valid, -1 if error

Convention: -1 means something went wrong upstream (bad/unexpected input) and
the task should NOT be passed into the FSM yet.

(Sigma = {0,1,2,3,4}).
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

    Args:
        deadline_datetime (datetime): The deadline, e.g. from collect_deadline_datetime().
        current_datetime (datetime, optional): Defaults to now if not provided.

    Returns:
        float: days remaining until deadline (can be negative if overdue).

    Raises:
        TypeError: if deadline_datetime is not a datetime object.
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

    Args:
        deadline_datetime (datetime): The task's deadline, e.g. from
            collect_deadline_datetime().
        task_length_days (float): Estimated days required to complete the task.
        current_datetime (datetime, optional): Defaults to now if not provided.

    Returns:
        int: 1  if time_left > task_length_days (Not Urgent)
             0  if time_left <= task_length_days (Urgent)
            -1  if an error occured
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
    1st boolean input: can this task be delegated / is it group work?

    Args:
        value: bool, int (0/1), or str ("yes"/"no", "y"/"n", "1"/"0") answer
            to "can this task be delegated / is this task a group work?"

    Returns:
        int: 1  = yes
             0  = no
            -1  = error
    """
    return _normalize_yes_no(value)


def has_significant_grade_impact(value):
    """
    3rd boolean input: does this task have a significant impact on your grade?

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
    Mood input: direct user selection, no calculation needed.

    1 = motivated
    2 = kinda tired
    3 = super tired
    4 = im deadge

    Args:
        value: int or str expected to be one of 1, 2, 3, 4.

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