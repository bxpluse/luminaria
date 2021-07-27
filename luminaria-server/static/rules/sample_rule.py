from common.abstract_classes.rule import Rule

rule = Rule(-1, 'Sample Rule')
rule.description = 'This is a sample template how creating a rule'
rule.subrule_names = ['subrule1', 'subrule2']


def run():
    rule.create_subrule(
        name='subrule1',
        func=dummy,
        args='param',
        triggers={
            'day_of_week': 'mon,tue,wed,thu,fri',
            'hour': '1'
        }
    )

    rule.create_subrule(
        name='subrule2',
        func=dummy,
        triggers={
            'day_of_week': 'tue,thu',
            'hour': '5',
            'minute': '30'
        }
    )


def dummy(arg=None):
    pass
