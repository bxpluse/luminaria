from datetime import datetime

from peewee import *

from database.base_model import DynamicModel


class NoteModel(DynamicModel):
    content = CharField()
    datetime_created = DateTimeField()

    class Meta:
        table_name = 'NOTE'

    @staticmethod
    def save_note(note):
        now = datetime.now()
        NoteModel.create(
            content=note,
            datetime_created=now
        )

    @staticmethod
    def load_note():
        query = NoteModel.select().order_by(NoteModel.id.desc()).get()
        return query.content
