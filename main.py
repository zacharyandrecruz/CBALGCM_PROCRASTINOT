import datetime
import databaseManager

dm = databaseManager.DatabaseManager()
dm.load_tasklist(1)

#dm.add_task("Mega Important Project", datetime.datetime.now().__add__(datetime.timedelta(days=1)), 5, False, True)

dm.save_tasklist()
