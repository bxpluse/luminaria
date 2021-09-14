from apps.reliance import DEPENDENCIES, DEPENDENCY_LIST
from common.enums import APP, DEPENDENCY, APPTYPE, ENVIRONMENT, APPSTATUS
from common.logger import LogLevel, log as log_to_db
from constants import ENV


class App:
    """
        Base class for all Apps to inherit from.
    """

    APP_ID = APP.BASE

    def __init__(self, app_type=APPTYPE.EXECUTABLE, cache=None):
        self.app_type = app_type
        if self.app_type == APPTYPE.STREAMING:
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.status = APPSTATUS.READY
        self.signal = None
        self.debugging = False
        self.first_start = True
        self.cache = cache

        # Dependencies
        self.overseer = self.install_dependency(DEPENDENCY.OVERSEER)
        self.configuration = self.install_dependency(DEPENDENCY.CONFIGURATION)
        self.praw_wrapper = self.install_dependency(DEPENDENCY.PRAW_WRAPPER)

    def install_dependency(self, dependency):
        if self.APP_ID in DEPENDENCY_LIST[dependency]:
            return DEPENDENCIES[dependency]
        return None

    def start(self):
        """ Called when an App is run. """
        self.log("~ App Starting")
        self.status = APPSTATUS.STARTED

    def stop(self):
        """ Called when an App is finished running or stopped. """
        if self.app_type == APPTYPE.STREAMING:
            self.log("~ App Stopping")
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.log("~ App Finished")
            self.status = APPSTATUS.READY

    def try_cache(self, command, hash_id):
        if self.has_cache():
            # Exclude requests in exclusion set
            if command in self.cache.exclusion:
                return None
            res = self.cache.fetch(hash_id)
            return res
        return None

    def store_to_cache(self, command, data, response):
        if self.has_cache():
            self.cache.store(command, data, response)

    def has_cache(self):
        return self.cache is not None

    def get_status(self):
        return self.status.value

    def get_data(self):
        return {}

    def log(self, message, level=LogLevel.INFO):
        """ Prints or logs information depending on environment. """
        if ENV == ENVIRONMENT.PROD:
            log_to_db(self.APP_ID.value, message, level)
        elif ENV == ENVIRONMENT.DEV:
            print('[{0}][{1}]'.format(self.APP_ID.value, level), message)

    def run(self, **kwargs):
        """
        Runs a streamable app
        """
        pass

    def blob(self, command, data):
        """
        Returns an absolute path to a file.
        """
        return ''

    def query(self, command, **kwargs):
        """
        Interface to execute a query.
        """
        return {}

    def execute(self, command, **kwargs):
        """
        Interface to execute a command.
        """
        return {}
