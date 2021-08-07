from common.enums import APP
from common.job_scheduler import JobScheduler
from constants import IS_DEV_ENV


class Rule:

    def __init__(self, name, rule_id=None):
        self.id = rule_id
        self.name = name
        self.description = ''
        self.subrule_names = []
        self.is_running = False
        self.suppressed = False
        self.scheduler = JobScheduler()
        self.app_id = None

    def create_subrule(self, name, func, triggers, args=None):
        self.subrule_names.append(name)
        if IS_DEV_ENV:
            self.mock_fields()
        if args is not None:
            if type(args) != tuple:
                args = (args, )
        self.scheduler.create_job(name=name,
                                  app_id=self.app_id,
                                  func=func,
                                  args=args,
                                  triggers=triggers
                                  )

    def mock_fields(self):
        if not self.app_id:
            self.app_id = APP.TBD
