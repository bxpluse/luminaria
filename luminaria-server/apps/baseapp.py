from common.enums import APPTYPE
from common.enums import ENVIRONMENT, APPSTATUS
from common.logger import log
from vars import ENV


class App:
    """
        Base class for all Apps to inherit from.
    """

    APP_ID = 'base_app'

    def __init__(self, app_type=APPTYPE.EXECUTABLE):
        self.app_type = app_type
        if self.app_type == APPTYPE.STREAMING:
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.status = APPSTATUS.READY
        self.signal = None
        self.debugging = False
        self.first_start = True

    def start(self):
        """ Called when an App is run. """
        self.info("~ Starting {0}".format(self.APP_ID))
        self.status = APPSTATUS.STARTED

    def stop(self):
        """ Called when an App is finished running or stopped. """
        if self.app_type == APPTYPE.STREAMING:
            self.info("~ Stopping {0}".format(self.APP_ID))
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.info("~ Finished {0}".format(self.APP_ID))
            self.status = APPSTATUS.READY

    def get_status(self):
        return self.status.value

    def get_data(self):
        return {}

    def info(self, message):
        """ Prints or logs information depending on environment. """
        if ENV == ENVIRONMENT.PROD:
            log(self.APP_ID, message)
        elif ENV == ENVIRONMENT.DEV:
            print(message)

    def debug(self, message):
        """ Prints or logs information depending on environment. """
        if self.debugging:
            if ENV == ENVIRONMENT.PROD:
                log(self.APP_ID, message)
            elif ENV == ENVIRONMENT.DEV:
                print(message)

    def get(self, command):
        return {}

    def blob(self, command):
        return ''

    def execute(self, command, **kwargs):
        return {}
