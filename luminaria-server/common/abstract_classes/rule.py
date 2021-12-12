from common.enums import APP
from common.job_scheduler import JobScheduler
from constants import IS_DEV_ENV


class Rule:

    def __init__(self, name, rule_id=None, alarmable=True):
        self.id = rule_id
        self.name = name
        self.description = ''
        self.subrule_names = set()
        self.scheduler = JobScheduler()
        self.app_id = None
        self.alarmable = alarmable  # Display if suppression toggle should be shown
        self.suppressed = False  # Boolean flag for rule to decide how to use

    def create_subrule(self, subrule_name, func, triggers, args=None, metadata=None):
        if metadata is None:
            metadata = {}
        if IS_DEV_ENV:
            self.mock_fields()
        if args is not None:
            if type(args) != tuple:
                args = (args,)
        successfully_created = self.scheduler.create_job(name=subrule_name,
                                                         app_id=self.app_id,
                                                         func=func,
                                                         args=args,
                                                         triggers=triggers,
                                                         metadata=metadata
                                                         )
        if successfully_created:
            self.subrule_names.add(subrule_name)
        return successfully_created

    def remove_subrule(self, subrule_name):
        self.subrule_names.remove(subrule_name)
        self.scheduler.remove_job(subrule_name)

    def mock_fields(self):
        if not self.app_id:
            self.app_id = APP.TBD
