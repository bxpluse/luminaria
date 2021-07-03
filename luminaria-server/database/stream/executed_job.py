from datetime import datetime

from peewee import CharField, DateTimeField

from database.base_model import StreamModel


class ExecutedJobModel(StreamModel):
    name = CharField()
    app_id = CharField()
    func = CharField()
    triggers = CharField()
    on_error = CharField()
    response = CharField()
    datetime_created = DateTimeField()

    class Meta:
        table_name = 'EXECUTED_JOB'

    @staticmethod
    def insert_new(name, app_id, func, triggers, on_error, response):
        ExecutedJobModel.create(
            name=name,
            app_id=app_id,
            func=func,
            triggers=triggers,
            on_error=on_error,
            response=response,
            datetime_created=datetime.now()
            )


if __name__ == "__main__":
    ExecutedJobModel.regenerate()
