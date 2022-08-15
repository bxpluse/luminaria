from common import util
from common.enums import Variant
from database.config.global_config_model import GlobalConfigModel


DEFAULT_DURATION = GlobalConfigModel.retrieve('MESSAGE_DEFAULT_DURATION')
DEFAULT_VARIANT = Variant.INFO


class Messenger:

    def __init__(self, socketio):
        self.socketio = socketio

    def toast(self, toast):
        config = {'message': toast.message,
                  'duration': toast.duration,
                  'variant': toast.variant,
                  'id': util.gen_id()
                  }
        self.socketio.emit('toast-message', config)


class Toast:

    IDENTIFIER = '<TOAST>'

    def __init__(self, message, duration=DEFAULT_DURATION, variant=DEFAULT_VARIANT):
        self.message = message
        self.duration = duration
        self.variant = variant
