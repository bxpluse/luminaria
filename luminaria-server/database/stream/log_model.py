from datetime import datetime

from peewee import *

from database.base_model import StreamModel


class LogModel(StreamModel):
    appname = CharField()
    message = CharField()
    level = IntegerField()
    datetime_created = DateTimeField()

    class Meta:
        table_name = 'LOG'

    @staticmethod
    def log_message(appname, message, level):
        now = datetime.now()
        LogModel.create(
            appname=appname,
            message=message,
            level=level,
            datetime_created=now
        )

    @staticmethod
    def tail(num_lines, apps, levels):
        if len(apps) == 0:
            query = LogModel.select()\
                .where(LogModel.level << levels)\
                .order_by(LogModel.datetime_created.desc())\
                .limit(num_lines)
        else:
            query = LogModel.select() \
                .where((LogModel.level << levels) & (LogModel.appname << apps)) \
                .order_by(LogModel.datetime_created.desc()) \
                .limit(num_lines)
        return query


if __name__ == "__main__":
    LogModel.regenerate()
