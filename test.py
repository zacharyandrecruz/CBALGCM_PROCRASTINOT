import json

from datetime import datetime
from datetime import timedelta

from databaseManager import DatabaseManager

dm = DatabaseManager()
sum = timedelta()

try:
    with open("tasklist.json", "r", encoding="utf-8") as f:
        data = json.load(f)
   
except FileNotFoundError:
    with open("tasklist.json", "w", encoding="utf-8") as f:
        json.dump([], f)

print(len(data))
for i in range(10):
    time1 = datetime.now()
    dm.load_tasklist(1)
    time2 = datetime.now()
    diff = time2 - time1
    print(diff)
    sum += diff

print("Final Average: " + str(sum/10))