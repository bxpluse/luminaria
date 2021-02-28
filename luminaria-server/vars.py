import os
from peewee import SqliteDatabase
from common.enums import ENVIRONMENT
from constants import DATABASE1_NAME, DATABASE2_NAME

# Vars
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV = ENVIRONMENT.PROD
DB1 = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE1_NAME))
DB2 = SqliteDatabase(os.path.join(ROOT_DIR, DATABASE2_NAME))
