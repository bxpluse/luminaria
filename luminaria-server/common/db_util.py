import os
import sqlite3

from constants import DATABASE1_NAME
from database.apps_model import AppsModel
from database.comment_frequency_model import CommentFrequencyModel
from database.global_config_model import GlobalConfigModel
from database.local_config_model import LocalConfigModel
from vars import ROOT_DIR, DB1


def db_exists():
    return os.path.isfile(os.path.join(ROOT_DIR, DATABASE1_NAME))


def create_db():
    conn = sqlite3.connect(os.path.join(ROOT_DIR, DATABASE1_NAME))
    conn.close()

    DB1.connect()
    DB1.create_tables([
        AppsModel,
        CommentFrequencyModel,
        GlobalConfigModel,
        LocalConfigModel
    ])

    GlobalConfigModel.create(username='CLIENT_SECRET')
    GlobalConfigModel.create(username='CLIENT_ID')
