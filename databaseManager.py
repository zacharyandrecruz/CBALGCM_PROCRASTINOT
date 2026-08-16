import json
from datetime import datetime

class Task:

    def __init__(self, name : str, date : datetime, group : bool, significant : bool):
        self.name = name
        self.date = date
        self.group = group
        self.significant = significant
        
    

class DatabaseManager:

    def __init__(self):
        self.tasklist = []

    def load_tasklist(self):

        try:
            with open("tasklist.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasklist = [Task(**item) for item in data]
        except FileNotFoundError:
            with open("tasklist.json", "w", encoding="utf-8") as f:
                json.dump([], f)
        

    def save_tasklist(self):
        with open("tasklist.json", "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in self.tasklist], f, default=str, indent=4)

