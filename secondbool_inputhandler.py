"""
CBALGCM Project — Input Handlers
---------------------------------------------
Handles all 4 raw user inputs feeding the FSM's boolean/mood transitions.

1st boolean input: can this task be delegated / is this task a group work?
    Output: 1 if yes, 0 if no, -1 if error

2nd boolean input: is time until deadline > time it takes to do the task?
    Output: 1 if time_left > time_required  (Not Urgent)
            0 if time_left <= time_required (Urgent)
           -1 if error (bad date format, bad task length, etc.)

3rd boolean input: does this task have a significant impact on your grade?
    Output: 1 if yes, 0 if no, -1 if error

Mood input: user's current mood/energy level
    1 = motivated
    2 = kinda tired 
    3 = tired
    4 = im dead
    Output: 1-4 if valid, -1 if error

Convention: -1 means something went wrong upstream (bad/unexpected input) and
the task should NOT be passed into the FSM yet.

(Sigma = {0,1,2,3,4}).
"""

from datetime import datetime

ERROR = -1 

VALID_MOODS = {1, 2, 3, 4}

TRUE_VALUES = {True, 1, "1", "y", "yes", "true"}
FALSE_VALUES = {False, 0, "0", "n", "no", "false"}


# ---------------------------------------------------------------------------
# 2nd boolean input
# ---------------------------------------------------------------------------

def get_time_left_hours(deadline_datetime, current_datetime=None):
    """
    Calculates the number of hours remaining until the deadline.

    Args:
        deadline_datetime (datetime | str): The deadline. If a string, it should
            be in ISO format, e.g. "2026-08-20 23:59".
        current_datetime (datetime, optional): Defaults to current time if not provided.

    Returns:
        float: hours remaining until deadline (can be negative if overdue).
        ValueError: if deadline_datetime is a string that isn't valid ISO format,
            or if it isn't a str/datetime at all.
    """
    if isinstance(deadline_datetime, str):
        deadline_datetime = datetime.fromisoformat(deadline_datetime)  # raises ValueError if malformed
    elif not isinstance(deadline_datetime, datetime):
        raise ValueError(
            f"deadline_datetime must be a str or datetime, got {type(deadline_datetime).__name__}"
        )

    if current_datetime is None:
        current_datetime = datetime.now()

    delta = deadline_datetime - current_datetime
    return delta.total_seconds() / 3600


def is_time_left_greater(deadline_datetime, task_length_hours, current_datetime=None):
    """
    2nd boolean input

    Args:
        deadline_datetime (datetime | str): The task's deadline.
        task_length_hours (float): Estimated hours required to complete the task.
        current_datetime (datetime, optional): Defaults to now if not provided.

    Returns:
        int: 1  if time_left > task_length_hours (Not Urgent)
             0  if time_left <= task_length_hours (Urgent)
            -1  if an error occurred
    """
    if isinstance(task_length_hours, bool) or not isinstance(task_length_hours, (int, float)):
        return ERROR
    if task_length_hours < 0:
        return ERROR

    try:
        time_left_hours = get_time_left_hours(deadline_datetime, current_datetime)
    except (ValueError, TypeError):
        # ValueError -> bad date format (e.g. datetime.fromisoformat couldn't parse it)
        # TypeError  -> subtracting incompatible types, etc.
        return ERROR

    return 1 if time_left_hours > task_length_hours else 0


# ---------------------------------------------------------------------------
# 1st and 3rd boolean inputs
# ---------------------------------------------------------------------------

def _normalize_yes_no(value):
    """
    converts a variety of yes/no inputs into 1, 0, or ERROR.

    Args:
        value: bool, int, or str representing a yes/no answer.

    Returns:
        int: yes = 1 
             no = 0 
             error = - 1
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
        int: yes = 1 
             no = 0 
             error = - 1
    """
    return _normalize_yes_no(value)


def has_significant_grade_impact(value):
    """
    3rd boolean input: does this task have a significant impact on your grade?

    Args:
        value: bool, int (0/1), or str ("yes"/"no", "y"/"n", "1"/"0") answer
            to "does this task have a significant impact on your grade?"

    Returns:
        int: yes = 1 
             no = 0 
             error = - 1
          
    """
    return _normalize_yes_no(value)


# ---------------------------------------------------------------------------
# Mood input
# ---------------------------------------------------------------------------

def get_mood(value):
    """
    Mood input: direct user selection, no calculation needed.

    1 = motivated
    2 = easy tasks only plz
    3 = super tired
    4 = im deadge

    Args:
        value: int or str expected to be one of 1, 2, 3, 4.

    Returns:
        int: the mood value (1-4) if valid, -1 if the value isn't 1-4.
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

    """ 

For testing 

if __name__ == "__main__":
    # quick manual tests
    print("-- is_time_left_greater --")
    print(f"valid input           -> {is_time_left_greater('2026-08-15 10:30', 6)}")
    print(f"bad date format       -> {is_time_left_greater('August 15th 2026', 6)}")
    print(f"bad task length type  -> {is_time_left_greater('2026-08-15 10:30', 'six')}")
    print(f"negative task length  -> {is_time_left_greater('2026-08-15 10:30', -3)}")

    print("\n-- is_delegatable --")
    print(f"'yes'   -> {is_delegatable('yes')}")
    print(f"0       -> {is_delegatable(0)}")
    print(f"'maybe' -> {is_delegatable('maybe')}")

    print("\n-- has_significant_grade_impact --")
    print(f"True    -> {has_significant_grade_impact(True)}")
    print(f"'n'     -> {has_significant_grade_impact('n')}")
    print(f"5       -> {has_significant_grade_impact(5)}")

    print("\n-- get_mood --")
    print(f"1       -> {get_mood(1)}")
    print(f"'3'     -> {get_mood('3')}")
    print(f"5       -> {get_mood(5)}")
    print(f"'burnt' -> {get_mood('burnt')}")


    """
