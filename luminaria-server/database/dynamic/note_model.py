from datetime import datetime

from peewee import *

from common.transformer import model_to_dict_wrapper
from database.base_model import DynamicModel

EMPTY_CONTENT = '{"blocks":[{"key":"bcj07","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],' \
                '"entityRanges":[],"data":{}}],"entityMap":{}} '


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
    def load_notes(offset):
        query = NoteModel.select().order_by(NoteModel.id.desc()).limit(10)
        notes = [model_to_dict_wrapper(note) for note in query]
        if len(notes) == 0:
            notes.append({'content': EMPTY_CONTENT})
        notes[0]['max_offset'] = len(notes)
        return notes[offset]
