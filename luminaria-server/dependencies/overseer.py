from common.abstract_classes.rule import Rule
from common.enums import DEPENDENCY
from common.logger import log, panic
from dependencies.base_dependency import Dependency


class Overseer(Dependency):
    DEPENDENCY_ID = DEPENDENCY.OVERSEER

    def __init__(self):
        super().__init__()
        self.rules_map = {}

    def add_rule(self, rule: Rule):
        rule.id = identify(rule.name)

        # Rule id's should be unique
        if rule.id in self.rules_map:
            panic('overseer', 'Rule id clash. Rule id: [{0}] name: [{1}]'.format(rule.id, rule.name))
            return

        self.rules_map[rule.id] = rule
        subrules = rule.scheduler.get_str_jobs()
        log('overseer', 'Running rule id: [{0}] name: [{1}] with [{2}] subrules. Subrules: {3}'
            .format(rule.id, rule.name, len(subrules), subrules))

    def suppress(self, rule_id, is_suppressed):
        self.rules_map[rule_id].suppressed = is_suppressed

    def get_rule(self, name):
        rule_id = identify(name)
        if rule_id in self.rules_map:
            return parse_rule(self.rules_map[rule_id])

    def get_all_rules(self):
        rules = self.rules_map.values()
        return [parse_rule(rule) for rule in rules]

    def dismiss_subrule(self, rule_id, subrule_name):
        rule = self.rules_map[rule_id]
        rule.remove_subrule(subrule_name)


def identify(rule_name):
    return rule_name.lower().strip().replace(' ', '-')


def parse_rule(rule: Rule):
    d = {'id': str(rule.id),
         'name': rule.name,
         'description': rule.description,
         'subrule_names': list(rule.subrule_names),
         'suppressed': rule.suppressed,
         'alarmable': rule.alarmable,
         'jobs': rule.scheduler.get_str_jobs()
         }
    return d
