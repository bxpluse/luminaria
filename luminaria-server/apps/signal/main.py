from apps.baseapp import App
from common.engine import get_engine
from common.enums import APP

i = 0


def test(a, b):
    global i
    i += 1
    if i < 4:
        print(i / 0)
    print("job just ran ", i, a, b)


class Signal(App):
    APP_ID = APP.SIGNAL

    def __init__(self):
        super().__init__()
        print("Signal inited")

        triggers = {}
        triggers['second'] = '10,20,30,40,50,0'

        # self.scheduler = JobScheduler()
        # self.scheduler.create_job(name='test()', app_id=self.APP_ID, func=test, triggers=triggers, args=('a', 'b'))

    def execute(self, command, **kwargs):
        if command == 'save':
            return {}


if __name__ == "__main__":
    engine = get_engine()
    print(engine.modules)
    engine.get('sample_rule')
