from common.enums import Variant
from constants import CONFIG_MAP

DEFAULT_DURATION = CONFIG_MAP['MESSAGE_DEFAULT_DURATION']
DEFAULT_VARIANT = Variant.INFO


class Messenger:

    def __init__(self, socketio):
        self.socketio = socketio

    def toast(self, toast):
        config = {'message': toast.message,
                  'duration': toast.duration,
                  'variant': toast.variant
                  }
        self.socketio.emit('toast-message', config)


class Toast:

    def __init__(self, message, duration=DEFAULT_DURATION, variant=DEFAULT_VARIANT):
        self.message = message
        self.duration = duration
        self.variant = variant
