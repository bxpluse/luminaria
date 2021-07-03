from apps.baseapp import App
from common.engine import get_engine
from common.enums import APP
from common.enums import APPTYPE
from common.job_scheduler import JobScheduler


class Signal(App):
    APP_ID = APP.SIGNAL

    def __init__(self):
        super().__init__(app_type=APPTYPE.STREAMING)
        self.engine = get_engine()
        self.scheduler = JobScheduler()
        self.rules = []

        for rule_name in self.engine.modules:
            module = self.engine.get(rule_name)
            rule = module.rule
            rule.scheduler = self.scheduler
            rule.app_id = self.APP_ID
            module.run()
            rule.is_running = True
            self.rules.append(rule)

        self.start()

    def execute(self, command, **kwargs):
        if command == 'getAllRules':
            return {'rules': self.rules}
