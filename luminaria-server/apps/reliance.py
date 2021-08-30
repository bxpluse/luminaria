from common.enums import APP, DEPENDENCY
from dependencies.configuration import Configuration
from dependencies.overseer import Overseer
from dependencies.praw_wrapper import PrawWrapper


DEPENDENCIES = {
    DEPENDENCY.OVERSEER: Overseer(),
    DEPENDENCY.CONFIGURATION: Configuration(),
    DEPENDENCY.PRAW_WRAPPER: PrawWrapper()
}

DEPENDENCY_LIST = {
    DEPENDENCY.OVERSEER: {APP.SIGNAL, APP.FEEDS, APP.FINDER},
    DEPENDENCY.CONFIGURATION: {APP.TOP_TEN, APP.SYSCMD, APP.FEEDS, APP.FINDER,
                               APP.IPO_LISTENER, APP.NEWS, APP.RC_STREAMER},
    DEPENDENCY.PRAW_WRAPPER: {APP.FEEDS}
}
