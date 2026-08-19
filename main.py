"""
CBALGCM Project — Main 
---------------------------------------------

Flow:
    1. Show banner, ask mood once, at startup.
    2. Load tasklist with that mood (priorities calculated for existing tasks).
    3. Menu loop: add task / edit task / remove task / view tasks / quit.
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

# type: 0 = "Submit by", 1 = "Prepare for"
TASK_TYPE_LABELS = {0: "Submit by", 1: "Prepare for"}


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


def ask_task_type():
    """
    Prompts for the task's type: 0 = "Submit by", 1 = "Prepare for".

    Returns:
        int: 0 or 1.
    """
    while True:
        ui.print_info("What kind of deadline is this?\n  0 = Submit by\n  1 = Prepare for")
        raw = ui.prompt("Enter 0 or 1:").strip()
        if raw in ("0", "1"):
            return int(raw)
        ui.print_error("Please enter 0 or 1.\n")


# ---------------------------------------------------------------------------
# Optional ("press Enter to keep current value") prompts, used by edit only
# ---------------------------------------------------------------------------

def ask_optional_text(question, current):
    """
    Text prompt that keeps `current` if the user just presses Enter.
    """
    raw = ui.prompt(f"{question} (Enter to keep '{current}'):")
    return current if raw.strip() == "" else raw.strip()


def ask_optional_estimated_time(current):
    """
    Estimated-time prompt that keeps `current` if the user just presses Enter,
    """
    while True:
        raw = ui.prompt(f"New estimated time in days (Enter to keep {current}):")
        if raw.strip() == "":
            return current
        try:
            value = float(raw)
        except ValueError:
            ui.print_error("Please enter a number.\n")
            continue
        if value < 0:
            ui.print_error("Estimated time can't be negative.\n")
            continue
        return value


def ask_optional_yes_no(question, handler, current):
    """
    Yes/no prompt that keeps `current` (0 or 1 / bool) if the user just
    presses Enter.
    """
    current_label = "yes" if current else "no"
    while True:
        raw = ui.prompt(f"{question} (yes/no, Enter to keep '{current_label}'):")
        if raw.strip() == "":
            return int(bool(current))
        result = handler(raw)
        if result == ERROR:
            ui.print_error("Please answer yes or no.\n")
            continue
        return result


def ask_optional_task_type(current):
    """
    Task-type prompt that keeps `current` if the user just presses Enter.
    """
    current_label = TASK_TYPE_LABELS.get(current, str(current))
    while True:
        ui.print_info("What kind of deadline is this?\n  0 = Submit by\n  1 = Prepare for")
        raw = ui.prompt(f"Enter 0 or 1 (Enter to keep '{current_label}'):")
        if raw.strip() == "":
            return current
        if raw.strip() in ("0", "1"):
            return int(raw.strip())
        ui.print_error("Please enter 0 or 1.\n")


def ask_optional_deadline(current):
    """
    Deadline prompt that keeps `current` (a datetime) if the user answers no
    to changing it
    """
    formatted_current = current.strftime("%b %d, %Y at %I:%M %p")
    while True:
        raw = ui.prompt(f"Change deadline? Currently {formatted_current} (yes/no, Enter to keep):")
        answer = raw.strip().lower()
        if answer in ("", "n", "no"):
            return current
        if answer in ("y", "yes"):
            return collect_deadline_datetime()
        ui.print_error("Please answer yes or no.\n")


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
    task_type = ask_task_type()

    dm.add_task(name, deadline, estimated_time, delegatable, grade_impact, mood, task_type)
    ui.print_success(f"'{name}' added.\n")
    ui.prompt("Press Enter to continue...")


def edit_task_flow(dm, mood):
    """
    Lists current tasks, lets the user pick one by number, then walks through
    each field letting them press Enter to keep the current value.
    """
    ui.print_section_header("Edit Task")
    if not dm.tasklist:
        ui.print_info("No tasks to edit.\n")
        ui.prompt("Press Enter to continue...")
        return

    for i, task in enumerate(dm.tasklist):
        ui.print_menu_option(i + 1, task.name)

    while True:
        raw = ui.prompt("Enter the number of the task to edit (or 0 to cancel):")
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
            break
        ui.print_error("That number doesn't match a task. Try again.\n")

    index = choice - 1
    task = dm.tasklist[index]

    ui.print_info(f"Editing '{task.name}'. Press Enter on any question to keep its current value.\n")

    name = ask_optional_text("New task name", task.name)
    deadline = ask_optional_deadline(task.date)
    estimated_time = ask_optional_estimated_time(task.estimatedTime)
    delegatable = bool(ask_optional_yes_no("Can this task be delegated / is it group work?", is_delegatable, task.group))
    grade_impact = bool(ask_optional_yes_no("Does this task have a significant impact on your grade?", has_significant_grade_impact, task.significant))
    task_type = ask_optional_task_type(task.type)

    dm.edit_task(index, name, deadline, estimated_time, delegatable, grade_impact, mood, task_type)
    ui.print_success(f"'{name}' updated.\n")
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
        ui.print_menu_option(2, "Edit a task")
        ui.print_menu_option(3, "Remove a task")
        ui.print_menu_option(4, "View tasks")
        ui.print_menu_option(5, "Quit")
        choice = ui.prompt("Choose an option (1-5):").strip()

        if choice == "1":
            add_task_flow(dm, mood)
            dm.save_tasklist()
        elif choice == "2":
            edit_task_flow(dm, mood)
            dm.save_tasklist()
        elif choice == "3":
            remove_task_flow(dm)
            dm.save_tasklist()
        elif choice == "4":
            view_tasks_flow(dm)
        elif choice == "5":
            dm.save_tasklist()
            ui.print_success("Goodbye!")
            break
        else:
            ui.print_error("Please enter 1, 2, 3, 4, or 5.\n")


if __name__ == "__main__":
    main()