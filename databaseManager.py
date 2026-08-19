import json
from algorithmManager import AlgorithmManager
from datetime import datetime

class Task:

    def __init__(self, name : str, date : datetime, estimatedTime : int, group : bool, significant : bool):
        self.name = name
        self.date = date
        self.estimatedTime = estimatedTime
        self.group = group
        self.significant = significant
        
    

class DatabaseManager:

    def __init__(self):
        self.tasklist = []
        self.taskprioritylist = []
        self.am = AlgorithmManager()

    def load_tasklist(self, mood : int):

        try:
            with open("tasklist.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if "date" in item and isinstance(item["date"], str):
                        item["date"] = datetime.fromisoformat(item["date"])
                    self.tasklist.append(Task(**item))
        except FileNotFoundError:
            with open("tasklist.json", "w", encoding="utf-8") as f:
                json.dump([], f)

        for task in self.tasklist:
            self.taskprioritylist.append(0)
            self.calculate_task_priority(self.tasklist.index(task), mood)
        

    def save_tasklist(self, name = "tasklist"):
        with open(name + ".json", "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in self.tasklist], f, default=str, indent=4)

    def add_task(self, name : str, date : datetime, estimatedTime : int, group : bool, significant : bool, mood : int):
        new_task = Task(name, date, estimatedTime, group, significant)
        self.tasklist.append(new_task)
        self.taskprioritylist.append(0)
        self.calculate_task_priority(len(self.tasklist) - 1, mood)

    def remove_task(self, task : Task):
        index = self.tasklist.index(task)
        self.tasklist.remove(task)
        del self.taskprioritylist[index]

    def import_tasklist(self, name, mood : int):

        try:
            with open(name + ".json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if "date" in item and isinstance(item["date"], str):
                        item["date"] = datetime.fromisoformat(item["date"])
                    self.tasklist.append(Task(**item))
                    self.taskprioritylist.append(0)
                    self.calculate_task_priority(len(self.tasklist) - 1, mood)
        except FileNotFoundError:
            return -1

        return 0
        

    def export_tasklist(self, name):
        self.save_tasklist(name)

    def calculate_task_priority(self, index : int, mood : int):

        group_flag = int(self.tasklist[index].group)

        time_till_deadline = max(self.tasklist[index].date.timestamp() - datetime.now().timestamp(), 0)
        urgent_flag = int(time_till_deadline > (self.tasklist[index].estimatedTime * 86400))

        important_flag = int(self.tasklist[index].significant)

        input = [group_flag, urgent_flag, important_flag, mood]

        result = self.am.process_state_machine_algorithm(input)

        """
        print(self.tasklist[index].name + " : " + str(input) + " : " + str(result))

        """

        self.taskprioritylist[index] = result

        