from common.abstract_classes.rule import Rule

rule = Rule('Sample Rule')
rule.description = 'This is a sample template on creating a rule'


def run():
    rule.create_subrule(
        subrule_name='subrule1',
        func=dummy,
        args='param',
        triggers={
            'day_of_week': 'mon,tue,wed,thu,fri',
            'hour': '1'
        }
    )

    rule.create_subrule(
        subrule_name='subrule2',
        func=dummy,
        triggers={
            'day_of_week': 'tue,thu',
            'hour': '5',
            'minute': '30'
        }
    )


def dummy(arg=None):
    pass
