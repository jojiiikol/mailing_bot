import datetime

from cheduler import scheduler

def baba():
    print("Hello")

scheduler.add_job(baba, 'date', run_date=datetime.datetime(2024, 5, 13, 16, 30))
scheduler.start()