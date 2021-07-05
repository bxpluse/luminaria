import os
from importlib import import_module
from constants import ROOT_DIR, STATIC_DIR, ENV, ENVIRONMENT

engine = None
started = False
inactive_rules = {} if ENV != ENVIRONMENT.PROD else {'sample_rule'}

RULES_IMPORT_PATH_DEV = 'static.rules.{0}'
RULES_IMPORT_PATH_PROD = 'static.rules.prod.{0}'
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
    for r, d, f in os.walk(os.path.join(ROOT_DIR, STATIC_DIR, 'rules')):
        for filename in f:
            if filename.endswith('.py'):
                module_name = filename.split('.')[0].lower()
                if module_name not in inactive_rules:
                    try:
                        module = import_module(RULES_IMPORT_PATH_DEV.format(module_name))
                    except ModuleNotFoundError:
                        if ENV != ENVIRONMENT.PROD:
                            continue
                        module = import_module(RULES_IMPORT_PATH_PROD.format(module_name))
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
