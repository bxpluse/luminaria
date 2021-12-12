from apps.baseapp import App
from common.abstract_classes.rule import Rule
from common.alerts.quote_alert import QuoteAlert
from common.carillon import create
from common.enums import APP, Variant
from common.messenger import Toast


class Bells(App):
    APP_ID = APP.BELLS
    RULE_NAME = 'Divine Bells'

    def __init__(self):
        super().__init__()
        self.rule = Rule(Bells.RULE_NAME, alarmable=True)
        self.rule.description = 'Scanning for value(s) to see if they are breached every hour'
        self.rule.app_id = self.APP_ID
        self.overseer.add_rule(self.rule)

    def execute(self, command, **kwargs):
        if command == 'get-alerts':
            rule = self.overseer.get_rule(Bells.RULE_NAME)
            return {'rule': rule}
        elif command == 'create-alert':
            symbol = kwargs['symbol']
            below = kwargs['below']
            above = kwargs['above']
            days_to_cancel = kwargs['daysToCancel']
            alert = QuoteAlert(symbol, below, above, days_to_cancel)
            alert.set_rule(self.rule)
            if create(self.rule, alert):
                return {Toast.IDENTIFIER: Toast('Created alert', duration=2, variant=Variant.SUCCESS)}
            else:
                return {Toast.IDENTIFIER: Toast('Failed to create alert', variant=Variant.ERROR)}
        elif command == 'remove-alert':
            subrule_name = kwargs['subruleName']
            self.rule.remove_subrule(subrule_name)
