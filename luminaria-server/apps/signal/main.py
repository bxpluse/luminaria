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
            rule.is_running = True
            module.run()
            self.rules.append(rule)

        self.start()

    def execute(self, command, **kwargs):
        if command == 'getAllRules':
            return {'rules': [parse_rule(rule) for rule in self.rules]}
        elif command == 'updateRuleRunning':
            rule_id = int(kwargs.get('id'))
            is_running = bool(kwargs.get('isRunning'))
            for rule in self.rules:
                if rule.id == rule_id:
                    rule.is_running = is_running
                    break


def parse_rule(rule):
    d = {'id': str(rule.id),
         'name': rule.name,
         'description': rule.description,
         'rule_names': str(rule.rule_names),
         'is_running': rule.is_running,
         'jobs': rule.scheduler.get_str_jobs()
         }
    return d
