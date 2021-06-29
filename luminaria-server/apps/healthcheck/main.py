import os
import subprocess

from apps.baseapp import App
from common.enums import APP


class Platform:
    WINDOWS = 'nt'
    LINUX = 'posix'


def cmd(command):
    lst = command.split(' ')
    return subprocess.run(lst, capture_output=True, text=True).stdout


def get_mock_syscheck():
    d = {'date': 'mock date',
         'uptime': 'mock uptime',
         'temperature': 'mock temperature',
         'ram': 'mock ram',
         'space': 'mock space'}
    return d


class HealthCheck(App):
    """
        Get overview of system.
    """

    APP_ID = APP.HEALTH_CHECK
    PLATFORM = None

    def __init__(self):
        super().__init__()
        self.PLATFORM = os.name

    def run_health_check(self):
        if self.PLATFORM != Platform.LINUX:
            return get_mock_syscheck()
        d = {'date': self.get_date(),
             'uptime': self.get_uptime(),
             'temperature': self.get_temp(),
             'ram': self.get_ram(),
             'space': self.get_space()
             }
        return d

    @staticmethod
    def get_date():
        return cmd("date")

    @staticmethod
    def get_uptime():
        return cmd("uptime")

    @staticmethod
    def get_temp():
        return cmd("vcgencmd measure_temp")

    @staticmethod
    def get_ram():
        return cmd("free -h")

    @staticmethod
    def get_space():
        return cmd("df -h")

    def execute(self, command, **kwargs):
        if command == 'checkup':
            return self.run_health_check()
