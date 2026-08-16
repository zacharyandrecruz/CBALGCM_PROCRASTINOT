"""
CBALGCM Project — Main 
---------------------------------------------

Flow:
    1. Ask mood once, at startup.
    2. Load tasklist with that mood (priorities calculated for existing tasks).
    3. Menu loop: add task / remove task / view tasks / quit.
"""

import databaseManager
from input import (
    collect_deadline_datetime,
    is_delegatable,
    has_significant_grade_impact,
    get_mood,
)

ERROR = -1

CATEGORY_LABELS = {
    0: "Do Now (High Priority)",
    1: "Do Now (Low Priority)",
    5: "Ask For Help",
    2: "Schedule",
    4: "Delegate",
    3: "Can Procrastinate",
    ERROR: "Unclassified",
}

# Fixed display order for view_tasks_flow
CATEGORY_ORDER = [0, 1, 5, 2, 4, 3, ERROR]


def ask_mood_at_startup():
    """
    Prompts for mood at program startup

    Returns:
        int: mood value 1-4.
    """
    while True:
        raw = input(
            "How are you feeling right now?\n"
            "  1 = motivated\n"
            "  2 = kinda tired\n"
            "  3 = super tired\n"
            "  4 = burnt out\n"
            "Enter a number (1-4): "
        )
        mood = get_mood(raw)
        if mood == ERROR:
            print("Please enter a number from 1 to 4.\n") #  Re-prompts on invalid input.
            continue
        return mood


def ask_task_name():
    """
    Prompts for a task name

    Returns:
        str: the task name.
    """
    while True:
        name = input("Task name: ").strip()
        if not name:
            print("Task name can't be empty.\n") # Re-prompts if left blank.
            continue
        return name


def ask_estimated_time():
    """
    Prompts for how long the task is estimated to take, in days.

    Returns:
        float: estimated time to complete the task, in days.
    """
    while True:
        raw = input("Estimated time to complete this task (in days): ")
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a number.\n")
            continue
        if value < 0:
            print("Estimated time can't be negative.\n")
            continue
        return value


def ask_yes_no(prompt, handler):
    """
    Yes/no prompt loop for is_delegatable() / has_significant_grade_impact().
    Re-prompts until a valid yes/no answer is given.

    Returns:
        int: 1 or 0.
    """
    while True:
        raw = input(f"{prompt} (yes/no): ")
        result = handler(raw)
        if result == ERROR:
            print("Please answer yes or no.\n")
            continue
        return result


def add_task_flow(dm, mood):
    """
    Collects all fields for a new task and adds it to the database.
    """
    print("\n--- Add Task ---")
    name = ask_task_name()
    deadline = collect_deadline_datetime()
    estimated_time = ask_estimated_time()
    delegatable = bool(ask_yes_no("Can this task be delegated / is it group work?", is_delegatable))
    grade_impact = bool(ask_yes_no("Does this task have a significant impact on your grade?", has_significant_grade_impact))

    dm.add_task(name, deadline, estimated_time, delegatable, grade_impact, mood)
    print(f"'{name}' added.\n")


def remove_task_flow(dm):
    """
    Lists current tasks and removes the one the user picks by number.
    """
    print("\n--- Remove Task ---")
    if not dm.tasklist:
        print("No tasks to remove.\n")
        return

    for i, task in enumerate(dm.tasklist):
        print(f"{i + 1}. {task.name}")

    while True:
        raw = input("Enter the number of the task to remove (or 0 to cancel): ")
        try:
            choice = int(raw)
        except ValueError:
            print("Please enter a number.\n")
            continue

        if choice == 0:
            print("Cancelled.\n")
            return
        if 1 <= choice <= len(dm.tasklist):
            removed = dm.tasklist[choice - 1]
            dm.remove_task(removed)
            print(f"'{removed.name}' removed.\n")
            return
        print("That number doesn't match a task. Try again.\n")


def view_tasks_flow(dm):
    """
    Prints tasks grouped by category (final FSM state).
    """
    print("\n--- View Tasks ---")
    if not dm.tasklist:
        print("No tasks to show.\n")
        return

    grouped = {}
    for i, task in enumerate(dm.tasklist):

        category = dm.taskprioritylist[i] if i < len(dm.taskprioritylist) else ERROR
        grouped.setdefault(category, []).append(task)
        ordered_categories = CATEGORY_ORDER + [c for c in grouped if c not in CATEGORY_ORDER]
        
    for category in ordered_categories:
        tasks = grouped.get(category)
        if not tasks:
            continue
        label = CATEGORY_LABELS.get(category, f"Unknown ({category})")
        print(f"\n{label}:")
        for task in tasks:
            print(f"  - {task.name} (due {task.date})")
    print()


def main():
    dm = databaseManager.DatabaseManager()

    mood = ask_mood_at_startup()
    dm.load_tasklist(mood)

    while True:
        print("\n=== CBALGCM Task Manager ===")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. View tasks")
        print("4. Quit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_task_flow(dm, mood)
        elif choice == "2":
            remove_task_flow(dm)
        elif choice == "3":
            view_tasks_flow(dm)
        elif choice == "4":
            dm.save_tasklist()
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()