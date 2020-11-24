from database.global_config_model import GlobalConfigModel

CLIENT_SECRET = GlobalConfigModel.retrieve('CLIENT_SECRET')
CLIENT_ID = GlobalConfigModel.retrieve('CLIENT_ID')
ALPHA_VANTAGE_KEY = GlobalConfigModel.retrieve('ALPHA_VANTAGE_KEY')
