from apps.dbutil.main import DBUtil
from apps.feeds.main import Feeds
from apps.finder.main import Finder
from apps.graphy.main import Graphy
from apps.healthcheck.main import HealthCheck
from apps.ipolistener.main import IPOListener
from apps.logviewer.main import LogViewer
from apps.monitor.main import RCListener
from apps.news.main import News
from apps.notes.main import Notes
from apps.pool.main import Pool
from apps.research.main import Research
from apps.signal.main import Signal
from apps.syscmd.main import Syscmd
from apps.topten.main import TopTen
from apps.updater.main import ExchangeUpdater
from common.enums import APP

APPS = {
    APP.EXCHANGE_UPDATER: ExchangeUpdater(),
    APP.LOG_VIEWER: LogViewer(),
    APP.DB_UTIL: DBUtil(),
    APP.RC_STREAMER: RCListener(),
    APP.IPO_LISTENER: IPOListener(),
    APP.TOP_TEN: TopTen(),
    APP.NEWS: News(),
    APP.NOTES: Notes(),
    APP.POOL: Pool(),
    APP.HEALTH_CHECK: HealthCheck(),
    APP.SIGNAL: Signal(),
    APP.GRAPHY: Graphy(),
    APP.RESEARCH: Research(),
    APP.SYSCMD: Syscmd(),
    APP.FEEDS: Feeds(),
    APP.FINDER: Finder()
}
