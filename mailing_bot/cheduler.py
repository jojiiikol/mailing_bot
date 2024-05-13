from apscheduler.schedulers.asyncio import AsyncIOScheduler

# TODO: make pre_start function

class Scheduler(AsyncIOScheduler):
    options = {
        'apscheduler.timezone': 'Asia/Yekaterinburg'
    }

    def __init__(self, **options):
        super().__init__(**options)

    def start(self, paused=False):
        print('APSheduler started')
        super().start(paused)
