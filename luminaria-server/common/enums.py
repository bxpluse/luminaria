from enum import Enum


class APP(Enum):
    EXCHANGE_UPDATER = 'updater'
    LOG_VIEWER = 'log-viewer'
    DB_BACKUP = 'db-backup'
    RC_STREAMER = 'rc-streamer'


class APPTYPE(Enum):
    STREAMING = 0
    EXECUTABLE = 1


class RUNMODE(Enum):
    COMMAND_LINE = 0
    USER_INTERFACE = 1


class APPSTATUS(Enum):
    STOPPED = 'Stopped'
    STARTED = 'Running'
    READY = 'Ready'
    INPROGRESS = 'Inprogress'
    UNKNOWN = 'Unknown'
    ERROR = 'Error'
    LINK = 'Link'


class ENVIRONMENT(Enum):
    DEV = 0
    PROD = 1


class COMMAND(Enum):
    RUN = 0
