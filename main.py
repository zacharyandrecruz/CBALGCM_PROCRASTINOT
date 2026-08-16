import datetime
import databaseManager

dm = databaseManager.DatabaseManager()
dm.load_tasklist()

running = True

while(running):
    print("YOU ARE RUNNING THE PROCRASTINOT PROGRAM\n")
    choice = input()
    if choice == "1":
        running = False
