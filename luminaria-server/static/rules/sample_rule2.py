from common.abstract_classes.rule import Rule

rule = Rule('Sample Rule 2')
rule.description = 'Sample description 2'


def run():
    rule.create_subrule(
        subrule_name='subrule1',
        func=some_func,
        args=('param1', 'param2'),
        triggers={
            'day_of_week': 'fri',
            'hour': '*/1'
        }
    )


def some_func(param1, param2):
    pass
