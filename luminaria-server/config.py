from database.global_config_model import GlobalConfigModel

CLIENT_SECRET = GlobalConfigModel.retrieve('CLIENT_SECRET')
CLIENT_ID = GlobalConfigModel.retrieve('CLIENT_ID')
