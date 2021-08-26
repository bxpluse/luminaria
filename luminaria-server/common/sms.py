from enum import Enum
from threading import Timer

from twilio.rest import Client

from common.logger import log, LogLevel
from database.config.local_config_model import LocalConfigModel
from database.config.global_config_model import GlobalConfigModel

TWILIO_SID = GlobalConfigModel.retrieve('TWILIO_SID')
TWILIO_TOKEN = GlobalConfigModel.retrieve('TWILIO_TOKEN')
TWILIO_FROM_NUMBER = GlobalConfigModel.retrieve('TWILIO_FROM_NUMBER')
TWILIO_TO_NUMBER = GlobalConfigModel.retrieve('TWILIO_TO_NUMBER')


batch_messages = []
dead_switch = True


class When(Enum):
    ONCE = 0
    NOW = 1
    NEXT = 2
    BATCH = 3


def send(msg, requester=None, when=When.NOW):
    log_message = ''
    if requester:
        log_message += '(Requester: {0})'.format(requester)
    log_message += ' ' + msg

    try:
        if when == When.NOW:
            send_sms(msg)
            log_sms('SENT', log_message)
        elif when == When.NEXT:
            log(app_name='sms', message='NEXT msg: {0}; batch: {1}; batch size: {2}'
                .format(msg, str(batch_messages), str(len(batch_messages))), level=LogLevel.DEBUG)
            if len(batch_messages) == 0:
                secs = LocalConfigModel.retrieve('SMS_BATCH_WAIT_SECS', default=60)
                Timer(secs, send, ('', None, When.BATCH)).start()
                log(app_name='sms', message='NEXT starting timer in {0} secs'.format(str(secs)), level=LogLevel.DEBUG)
            batch_messages.append(msg)
        elif when == When.BATCH:
            concat_msg = ''
            for msg in batch_messages:
                concat_msg += msg + ' | '
            send_sms(concat_msg)
            log_sms('SENT {0} BATCH'.format(len(batch_messages)), concat_msg)
            batch_messages.clear()
        elif when == When.ONCE:
            global dead_switch
            if dead_switch:
                send_sms(msg)
                log_sms('SENT ONCE', log_message)
                dead_switch = False
            else:
                log_sms('DEAD SWITCH', log_message)

    except Exception as exception:
        msg_with_error = 'FAILED TO SEND SMS EXCEPTION: {0} | {1} '.format(str(exception), log_message)
        log(app_name='sms', message=msg_with_error, level=LogLevel.ERROR)


def log_sms(style, message):
    log(app_name='sms', message='{0} > {1}'.format(style, message), level=LogLevel.INFO)


def send_sms(msg):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(to=TWILIO_TO_NUMBER, from_=TWILIO_FROM_NUMBER, body=msg)
