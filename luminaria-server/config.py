from database.config.global_config_model import GlobalConfigModel
from database.config.local_config_model import LocalConfigModel

CLIENT_SECRET = GlobalConfigModel.retrieve('CLIENT_SECRET')
CLIENT_ID = GlobalConfigModel.retrieve('CLIENT_ID')
ALPHA_VANTAGE_KEY = GlobalConfigModel.retrieve('ALPHA_VANTAGE_KEY')
SCHEDULER_TIME_ZONE = GlobalConfigModel.retrieve('SCHEDULER_TIME_ZONE')

CONFIG_MAP = {**GlobalConfigModel.retrieve_all(), **LocalConfigModel.retrieve_all()}
