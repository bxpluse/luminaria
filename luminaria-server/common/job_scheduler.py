import threading
from enum import Enum

from apscheduler.schedulers.background import BackgroundScheduler

from common.logger import log, LogLevel
from config import SCHEDULER_TIME_ZONE
from database.stream.executed_job_model import ExecutedJobModel


class OnError(Enum):
    CANCEL = 'CANCEL'    # Cancel the job
    RESTART = 'RESTART'  # Restart the scheduled job and wait until next scheduled run
    RETRY = 'RETRY'      # Retry once instantly, then restart the job


class Job:
    TIMES_TO_RETRY = 8
    SECS_BETWEEN_RETRY = 10
    SECS_BEFORE_RESTART = 30
    LOG_LEVEL_WARN = LogLevel.WARN

    def __init__(self, name, app_id, func, triggers, on_error, scheduler, args=None):
        self.name = name
        self.app_id = app_id.value
        self.func = func
        self.args = args
        self.on_error = on_error
        self.scheduler = scheduler
        self.scheduler_job = None
        self.triggers = triggers
        self.hour = triggers.get('hour', None)
        self.minute = triggers.get('minute', None)
        self.second = triggers.get('second', None)
        self.day_of_week = triggers.get('day_of_week', None)

    def run(self):
        self.scheduler_job = self.scheduler.add_job(self.execute_job, args=self.args, trigger='cron',
                                                    hour=self.hour, second=self.second, minute=self.minute,
                                                    day_of_week=self.day_of_week)
        all_jobs = self.scheduler.get_jobs()
        log(self.app_id, 'Running scheduler with {0} job(s): {1}\n'
                         'function: {2}   args: {3}  on_error: {4}  triggers: {5}'
            .format(len(all_jobs), all_jobs, self.func.__name__, self.args, self.on_error, self.triggers))

    def execute_job(self, *args):
        try:
            self.run_job(*args)
        except Exception as exception:
            log(self.app_id, 'Encountered error on execute: {0}'.format(str(exception)), level=self.LOG_LEVEL_WARN)
            if self.on_error == OnError.CANCEL:
                self.scheduler_job.remove()
            elif self.on_error == OnError.RESTART:
                self.scheduler_job.remove()
                timer = threading.Timer(self.SECS_BEFORE_RESTART, self.run)
                timer.start()
            elif self.on_error == OnError.RETRY:
                self.scheduler_job.remove()
                self.retry(1, *args)

    def retry(self, count, *args):
        if count == self.TIMES_TO_RETRY:
            self.run()
        try:
            self.run_job(*args)
            self.run()
        except Exception as exception:
            log(self.app_id, 'Encountered error on retry[{0}]: {1}'
                .format(str(count), str(exception)), level=self.LOG_LEVEL_WARN)
            timer = threading.Timer(self.SECS_BETWEEN_RETRY, self.retry, args=(count + 1, *args))
            timer.start()

    def run_job(self, *args):
        response = self.func(*args)
        # Job has ran successfully
        ExecutedJobModel.insert_new(
            name=self.name,
            app_id=self.app_id,
            func=self.func.__name__,
            triggers=self.triggers,
            on_error=self.on_error.value,
            response=str(response)
        )

    def get_info(self):
        d = {'name': self.name,
             'func': self.func.__name__,
             'args': self.args,
             'on_error': self.on_error.value,
             'triggers': self.triggers
             }
        return d


class JobScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': SCHEDULER_TIME_ZONE})
        self.scheduler.start()
        self.jobs = {}

    def create_job(self, name, app_id, func, triggers, args=None, on_error=OnError.RETRY):
        if name not in self.jobs:
            job = Job(name, app_id, func, triggers, args=args, on_error=on_error, scheduler=self.scheduler)
            self.jobs[name] = job
            job.run()

    def get_str_jobs(self):
        return [job.get_info() for job in self.jobs.values()]
