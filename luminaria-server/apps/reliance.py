from common.enums import APP, DEPENDENCY
from dependencies.overseer import Overseer


DEPENDENCIES = {
    DEPENDENCY.OVERSEER: Overseer()
}

DEPENDENCY_LIST = {
    DEPENDENCY.OVERSEER: {APP.SIGNAL, APP.FEEDS, APP.FINDER}
}
