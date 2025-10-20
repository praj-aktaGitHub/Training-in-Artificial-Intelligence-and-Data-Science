import pandas as pd
from datetime import datetime


processed_visits = pd.read_csv("processed_visits.csv")


today = datetime.now().date()
daily_visits = processed_visits[pd.to_datetime(processed_visits["Date"]).dt.date == today]

filename = f"daily_visits_report_{today.strftime('%Y%m%d')}.csv"
daily_visits.to_csv(filename, index=False)

with open("scheduler_log.txt", "a", encoding="utf-8") as log:
    log.write(f"Scheduler ran at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
