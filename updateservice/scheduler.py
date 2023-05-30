from apscheduler.schedulers.background import BackgroundScheduler
from .update import update_task_status

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_task_status, 'interval', minutes=1)
    scheduler.start()
