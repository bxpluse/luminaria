import threading
from datetime import datetime
from enum import Enum

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler

from common.logger import log, LogLevel
from database.config.global_config_model import GlobalConfigModel
from database.stream.executed_job_model import ExecutedJobModel


class OnError(Enum):
    CANCEL = 'CANCEL'  # Cancel the job
    RESTART = 'RESTART'  # Restart the scheduled job and wait until next scheduled run
    RETRY = 'RETRY'  # Retry once instantly, then restart the job


class Job:
    TIMES_TO_RETRY = 6
    STARTING_SECS_BETWEEN_RETRY = 2
    SECS_BEFORE_RESTART = 30
    LOG_LEVEL_WARN = LogLevel.WARN

    def __init__(self, name, app_id, func, triggers, scheduler_num, on_error, scheduler, metadata, args=None):
        self.name = str(name)
        self.app_id = app_id.value
        self.func = func
        self.args = args
        self.on_error = on_error
        self.scheduler = scheduler
        self.scheduler_job = None
        self.triggers = triggers
        self.scheduler_num = scheduler_num
        self.metadata = metadata
        self.start_date = triggers.get('start_date', None)
        self.end_date = triggers.get('end_date', None)
        self.hour = triggers.get('hour', None)
        self.minute = triggers.get('minute', None)
        self.second = triggers.get('second', None)
        self.day_of_week = triggers.get('day_of_week', None)
        self.secs_between_retry = Job.STARTING_SECS_BETWEEN_RETRY

    def run(self):
        self.scheduler_job = self.scheduler.add_job(self.execute_job, args=self.args, trigger='cron',
                                                    start_date=self.start_date, end_date=self.end_date,
                                                    hour=self.hour, second=self.second, minute=self.minute,
                                                    day_of_week=self.day_of_week)

    def remove(self):
        # Try removing the job id it hasn't been automatically cleaned up
        if self.scheduler_job is not None:
            try:
                self.scheduler_job.remove()
            except JobLookupError:
                pass

    def execute_job(self, *args):
        try:
            self.run_job(*args)
        except Exception as exception:
            log(self.app_id, 'Job [{0}] encountered error on execute: {1}'
                .format(self.name, str(exception)), level=self.LOG_LEVEL_WARN)
            self.remove()
            if self.on_error == OnError.RESTART:
                timer = threading.Timer(Job.SECS_BEFORE_RESTART, self.run)
                timer.start()
            elif self.on_error == OnError.RETRY:
                self.retry(1, *args)

    def retry(self, count, *args):

        def x(t):
            total = 0
            current = Job.STARTING_SECS_BETWEEN_RETRY
            for i in range(t):
                total += current
                current *= 2
            return total

        if count == Job.TIMES_TO_RETRY:
            self.run()
            total_time_elapsed = x(count)
            log(self.app_id, 'Max retry exceeded for job [{0}]'.format(self.name), level=self.LOG_LEVEL_WARN)
            self.insert_job('Failed after max [{0}] tries with total [{1}] secs'
                            .format(Job.TIMES_TO_RETRY, str(total_time_elapsed)))
            self.secs_between_retry = Job.STARTING_SECS_BETWEEN_RETRY
            return
        try:
            self.run_job(*args)
        except Exception as exception:
            log(self.app_id, 'Job [{0}] encountered error on retry[{1}]. Next try in [{2}] secs: {3}'
                .format(self.name, str(count), str(self.secs_between_retry), str(exception)), level=self.LOG_LEVEL_WARN)
            timer = threading.Timer(self.secs_between_retry, self.retry, args=(count + 1, *args))
            self.secs_between_retry *= 2
            timer.start()
            return

        # Restart normal run after job executes successfully
        log(self.app_id, 'Job [{0}] succeeded after [{1}] try(s)'
            .format(str(self.name), str(count)), level=self.LOG_LEVEL_WARN)
        self.run()

    def run_job(self, *args):
        response = self.func(*args)
        # Job has ran successfully
        self.insert_job(response)

    def insert_job(self, response):
        ExecutedJobModel.insert_new(
            name=self.name,
            app_id=self.app_id,
            func=self.func.__name__,
            triggers=self.triggers,
            on_error=self.on_error.value,
            response=str(response)
        )

    def get_info(self):
        expired = True
        if self.scheduler_job.next_run_time is not None:
            expired = self.scheduler_job.next_run_time < datetime.now(self.scheduler_job.next_run_time.tzinfo)
        d = {'name': self.name,
             'func': self.func.__name__,
             'args': str(self.args),
             'on_error': self.on_error.value,
             'triggers': self.triggers,
             'expired': expired,
             'metadata': self.metadata
             }
        return d


class JobScheduler:
    SCHEDULER_NUM = 1
    SCHEDULER_TIME_ZONE = GlobalConfigModel.retrieve('SCHEDULER_TIME_ZONE')

    def __init__(self):
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': JobScheduler.SCHEDULER_TIME_ZONE})
        self.scheduler_num = JobScheduler.SCHEDULER_NUM
        JobScheduler.SCHEDULER_NUM += 1
        self.scheduler.start()
        self.jobs = {}

    def create_job(self, name, app_id, func, triggers, metadata, args=None, on_error=OnError.RETRY):
        if name not in self.jobs:
            job = Job(name=name, app_id=app_id, func=func, triggers=triggers, scheduler_num=self.scheduler_num,
                      args=args, on_error=on_error, scheduler=self.scheduler, metadata=metadata)
            self.jobs[name] = job
            job.run()
            return True
        return False

    def remove_job(self, name):
        if name in self.jobs:
            job = self.jobs[name]
            job.remove()
            del self.jobs[name]

    def get_str_jobs(self):
        return [job.get_info() for job in self.jobs.values()]
