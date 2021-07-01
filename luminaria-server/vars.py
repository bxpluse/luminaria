import os
from peewee import SqliteDatabase
from common.enums import ENVIRONMENT
from constants import DATABASE_CONFIG_NAME, DATABASE_STATIC_NAME, DATABASE_STREAM_NAME, DATABASE_DYNAMIC_NAME

# Vars
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
ENV = ENVIRONMENT.PROD
DB_CONFIG = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_CONFIG_NAME))
DB_DYNAMIC = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_DYNAMIC_NAME))
DB_STATIC = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_STATIC_NAME))
DB_STREAM = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_STREAM_NAME))
