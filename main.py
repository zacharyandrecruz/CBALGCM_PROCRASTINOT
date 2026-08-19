"""
CBALGCM Project — Main 
---------------------------------------------

Flow:
    1. Show banner, ask mood once, at startup.
    2. Load tasklist with that mood (priorities calculated for existing tasks).
    3. Menu loop: add task / remove task / view tasks / quit.
"""

import databaseManager
import ui
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
    3: "Do Soon",
    ERROR: "Error Found",
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
        ui.print_info(
            "How are you feeling right now?\n"
            "  1 = motivated\n"
            "  2 = kinda tired\n"
            "  3 = super tired\n"
            "  4 = burnt out"
        )
        raw = ui.prompt("Enter a number (1-4):")
        mood = get_mood(raw)
        if mood == ERROR:
            ui.print_error("Please enter a number from 1 to 4.\n")  # Re-prompts on invalid input.
            continue
        return mood


def ask_task_name():
    """
    Prompts for a task name

    Returns:
        str: the task name.
    """
    while True:
        name = ui.prompt("Task name:").strip()
        if not name:
            ui.print_error("Task name can't be empty.\n")  # Re-prompts if left blank.
            continue
        return name


def ask_estimated_time():
    """
    Prompts for how long the task is estimated to take, in days.

    Returns:
        float: estimated time to complete the task, in days.
    """
    while True:
        raw = ui.prompt("Estimated time to complete this task (in days):")
        try:
            value = float(raw)
        except ValueError:
            ui.print_error("Please enter a number.\n")
            continue
        if value < 0:
            ui.print_error("Estimated time can't be negative.\n")
            continue
        return value


def ask_yes_no(question, handler):
    """
    Yes/no prompt loop for is_delegatable() / has_significant_grade_impact().

    Returns:
        int: 1 or 0.
    """
    while True:
        raw = ui.prompt(f"{question} (yes/no):")
        result = handler(raw)
        if result == ERROR:
            ui.print_error("Please answer yes or no.\n")
            continue
        return result


def add_task_flow(dm, mood):
    """
    Collects all fields for a new task and adds it to the database.
    """
    ui.print_section_header("Add Task")
    name = ask_task_name()
    deadline = collect_deadline_datetime()
    estimated_time = ask_estimated_time()
    delegatable = bool(ask_yes_no("Can this task be delegated / is it group work?", is_delegatable))
    grade_impact = bool(ask_yes_no("Does this task have a significant impact on your grade?", has_significant_grade_impact))

    dm.add_task(name, deadline, estimated_time, delegatable, grade_impact, mood)
    ui.print_success(f"'{name}' added.\n")
    ui.prompt("Press Enter to continue...")


def remove_task_flow(dm):
    """
    Lists current tasks and removes the one the user picks by number.
    """
    ui.print_section_header("Remove Task")
    if not dm.tasklist:
        ui.print_info("No tasks to remove.\n")
        ui.prompt("Press Enter to continue...")
        return

    for i, task in enumerate(dm.tasklist):
        ui.print_menu_option(i + 1, task.name)

    while True:
        raw = ui.prompt("Enter the number of the task to remove (or 0 to cancel):")
        try:
            choice = int(raw)
        except ValueError:
            ui.print_error("Please enter a number.\n")
            continue

        if choice == 0:
            ui.print_info("Cancelled.\n")
            ui.prompt("Press Enter to continue...")
            return
        if 1 <= choice <= len(dm.tasklist):
            removed = dm.tasklist[choice - 1]
            dm.remove_task(removed)
            ui.print_success(f"'{removed.name}' removed.\n")
            ui.prompt("Press Enter to continue...")
            return
        ui.print_error("That number doesn't match a task. Try again.\n")


def view_tasks_flow(dm):
    """
    Prints tasks grouped by category.
    """
    ui.print_section_header("View Tasks")
    if not dm.tasklist:
        ui.print_info("No tasks to show.\n")
        ui.prompt("Press Enter to continue...")
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
        color = ui.print_category_header(label, category)
        for task in tasks:
            ui.print_task_line(task, color)
    print()
    ui.prompt("Press Enter to continue...")


def main():
    dm = databaseManager.DatabaseManager()

    ui.clear_screen()
    ui.print_banner()
    mood = ask_mood_at_startup()
    dm.load_tasklist(mood)

    while True:
        ui.clear_screen()
        ui.print_banner()
        ui.print_menu_title("PROCRASTINOT Task Manager")
        ui.print_menu_option(1, "Add a task")
        ui.print_menu_option(2, "Remove a task")
        ui.print_menu_option(3, "View tasks")
        ui.print_menu_option(4, "Quit")
        choice = ui.prompt("Choose an option (1-4):").strip()

        if choice == "1":
            add_task_flow(dm, mood)
        elif choice == "2":
            remove_task_flow(dm)
        elif choice == "3":
            view_tasks_flow(dm)
        elif choice == "4":
            dm.save_tasklist()
            ui.print_success("Goodbye!")
            break
        else:
            ui.print_error("Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()