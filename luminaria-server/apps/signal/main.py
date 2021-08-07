from apps.baseapp import App
from common.engine import get_engine
from common.enums import APP
from common.enums import APPTYPE


class Signal(App):
    APP_ID = APP.SIGNAL

    def __init__(self):
        super().__init__(app_type=APPTYPE.STREAMING)
        self.engine = get_engine()

        for rule_name in self.engine.modules:
            module = self.engine.get(rule_name)
            rule = module.rule
            rule.app_id = self.APP_ID
            rule.is_running = True
            module.run()
            self.overseer.add_rule(rule)

        self.start()

    def execute(self, command, **kwargs):
        if command == 'fetch-all-rules':
            return {'rules': self.overseer.get_all_rules()}
        elif command == 'update-rule-suppressed':
            rule_id = kwargs.get('id')
            suppressed = bool(kwargs.get('suppressed'))
            self.overseer.suppress(rule_id, suppressed)
