from enum import Enum


class APP(Enum):
    # App ID must match up with id column in APPS table
    BASE = 'base-app'
    TBD = 'app-in-development'
    EXCHANGE_UPDATER = 'updater'
    LOG_VIEWER = 'log-viewer'
    DB_BACKUP = 'db-backup'
    RC_STREAMER = 'rc-streamer'
    IPO_LISTENER = 'ipo-listener'
    TOP_TEN = 'top-ten'
    NEWS = 'news'
    HEALTH_CHECK = 'health-check'
    NOTES = 'notes'
    POOL = 'pool'
    SIGNAL = 'signal'
    GRAPHY = 'graphy'
    RESEARCH = 'research'
    SYSCMD = 'syscmd'
    FEEDS = 'feeds'
    FINDER = 'finder'


class DEPENDENCY(Enum):
    BASE = 'base-dependency'
    OVERSEER = 'overseer'


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


class TimeFrame(Enum):
    MONTH_START = 0
    MONTH_END = 1
    WEEK_START = 2
    WEEK_END = 3


class SeriesAttribute:
    DATE = 2
    ADJUSTED_CLOSE = 10
    VOLUME = 11


class Variant:
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    DARK = 'dark'
