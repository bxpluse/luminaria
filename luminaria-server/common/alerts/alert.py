from common.interface.ruleable import Ruleable
from common.sms import send as send_msg


class Alert(Ruleable):

    def __init__(self, alert_type):
        super().__init__()
        self.alert_type = alert_type

    def on_alert(self):
        pass

    def send(self, message):
        send_msg(message)

    def cancel(self):
        pass

    def is_suppressed(self):
        return False
