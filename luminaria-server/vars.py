import os
from peewee import SqliteDatabase
from common.enums import ENVIRONMENT
from constants import DATABASE_NAME

# Vars
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV = ENVIRONMENT.PROD
DB = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE_NAME))
