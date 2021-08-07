from common.enums import DEPENDENCY
from dependencies.base_dependency import Dependency
from common.util import gen_id


class Overseer(Dependency):
    DEPENDENCY_ID = DEPENDENCY.OVERSEER

    def __init__(self):
        super().__init__()
        self.rules = []
        self.rules_map = {}

    def add_rule(self, rule):
        rule.id = gen_id()
        self.rules.append(rule)
        self.rules_map[rule.id] = rule

    def suppress(self, rule_id, is_suppressed):
        self.rules_map[rule_id].suppressed = is_suppressed

    def get_all_rules(self):
        return [parse_rule(rule) for rule in self.rules]


def parse_rule(rule):
    d = {'id': str(rule.id),
         'name': rule.name,
         'description': rule.description,
         'subrule_names': rule.subrule_names,
         'is_running': rule.is_running,
         'suppressed': rule.suppressed,
         'jobs': rule.scheduler.get_str_jobs()
         }
    return d
