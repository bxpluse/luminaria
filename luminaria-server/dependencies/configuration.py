from common.enums import DEPENDENCY
from database.config.global_config_model import GlobalConfigModel
from database.config.local_config_model import LocalConfigModel
from dependencies.base_dependency import Dependency


class Configuration(Dependency):
    DEPENDENCY_ID = DEPENDENCY.CONFIGURATION

    def __init__(self):
        super().__init__()
        self.config_map = {**LocalConfigModel.retrieve_all(), **GlobalConfigModel.retrieve_all()}

    def refresh_config_map(self):
        self.config_map = {**LocalConfigModel.retrieve_all(), **GlobalConfigModel.retrieve_all()}

    def __getitem__(self, arg):
        return self.config_map[arg]
