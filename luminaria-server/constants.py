import os
import sqlite3

from peewee import SqliteDatabase

from common.enums import ENVIRONMENT


def bootstrap_config():
    def consume_rows():
        rows = cur.fetchall()
        for row in rows:
            res[row['parameter']] = row['value']
    res = {}
    conn = sqlite3.connect(os.path.join(ROOT_DIR, DATABASE_CONFIG_NAME))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''SELECT * FROM GLOBAL_CONFIG''')
    consume_rows()
    cur.execute('''SELECT * FROM LOCAL_CONFIG''')
    consume_rows()
    cur.close()
    conn.close()
    return res


# Directories
STATIC_DIR = 'static'
EXCHANGES_DIR = 'exchanges'
BACKUP_DIR = 'backup_folder'

# Filenames
DATABASE_CONFIG_NAME = 'db_config.sqlite3'
DATABASE_DYNAMIC_NAME = 'db_dynamic.sqlite3'
DATABASE_STATIC_NAME = 'db_static.sqlite3'
DATABASE_STREAM_NAME = 'db_stream.sqlite3'
BLACKLIST_FILENAME = 'blacklist.txt'
WHITELIST_FILENAME = 'whitelist.txt'
LOGFILE = 'log.txt'

# Variables
ENV = ENVIRONMENT.DEV if os.name == 'nt' else ENVIRONMENT.PROD
IS_DEV_ENV = True if ENV == ENVIRONMENT.DEV else False
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_CONFIG = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_CONFIG_NAME))
DB_DYNAMIC = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_DYNAMIC_NAME))
DB_STATIC = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_STATIC_NAME))
DB_STREAM = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_STREAM_NAME))

# Dictionary of all configs; must restart app to refresh changes if using this constant
CONFIG_MAP = bootstrap_config()
