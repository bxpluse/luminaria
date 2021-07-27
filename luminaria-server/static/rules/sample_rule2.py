from common.abstract_classes.rule import Rule

rule = Rule(-2, 'Sample Rule 2')
rule.description = 'Sample description 2'
rule.subrule_names = ['anotherrule']


def run():
    rule.create_subrule(
        name='subrule1',
        func=some_func,
        args=('param1', 'param2'),
        triggers={
            'day_of_week': 'fri',
            'hour': '*/1'
        }
    )


def some_func(param1, param2):
    pass
