import os
from importlib import import_module

from constants import STATIC_DIR

engine = None
started = False
inactive_rules = {'sample_rule'}

RULES_IMPORT_PATH = 'static.rules.{0}'
DECLARATIONS = ['rule', 'run']


class Engine:
    def __init__(self, modules):
        self.modules = modules

    def get(self, name):
        return self.modules[name.lower()]


def verify_module(module):
    """
    Validates a given module
    :param module: a rule_name.py module
    :return: Boolean if module is a valid engine rule
    """
    for declares in DECLARATIONS:
        if declares not in dir(module):
            return False
    return True


def start_engine():
    modules = {}
    for filename in os.listdir(os.path.join(STATIC_DIR, 'rules')):
        if filename.endswith('.py'):
            module_name = filename.split('.')[0].lower()
            if module_name not in inactive_rules:
                module = import_module(RULES_IMPORT_PATH.format(module_name))
                if not verify_module(module):
                    continue
                modules[module_name] = module
    global started
    global engine
    started = True
    engine = Engine(modules)


def get_engine():
    global started
    if not started:
        start_engine()
    return engine
