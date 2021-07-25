from apps.backup.main import BackupDatabase
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
from apps.topten.main import TopTen
from apps.updater.main import ExchangeUpdater
from common.enums import APP
from database.config.local_config_model import LocalConfigModel

APPS = {
    APP.EXCHANGE_UPDATER: ExchangeUpdater(),
    APP.LOG_VIEWER: LogViewer(),
    APP.DB_BACKUP: BackupDatabase(),
    APP.RC_STREAMER: RCListener(subs=LocalConfigModel.retrieve('SUBREDDITS_TO_MONITOR'), interval=15),
    APP.IPO_LISTENER: IPOListener(),
    APP.TOP_TEN: TopTen(),
    APP.NEWS: News(),
    APP.NOTES: Notes(),
    APP.POOL: Pool(),
    APP.HEALTH_CHECK: HealthCheck(),
    APP.SIGNAL: Signal(),
    APP.GRAPHY: Graphy(),
    APP.RESEARCH: Research()
}
