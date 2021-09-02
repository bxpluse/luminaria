from apps.baseapp import App
from common.cache import Cache
from common.enums import APP
from database.dynamic.note_model import NoteModel


class Notes(App):
    APP_ID = APP.NOTES

    def __init__(self):
        self.cache = Cache(600)
        super().__init__(cache=self.cache)

    @staticmethod
    def save(content):
        NoteModel.save_note(content)

    @staticmethod
    def load(offset):
        note = NoteModel.load_notes(offset)
        return note

    def execute(self, command, **kwargs):
        if command == 'save':
            self.cache.invalidate()
            content = kwargs['content']
            self.save(content)
            return {}
        elif command == 'load':
            offset = kwargs.get('offset')
            return {'note': self.load(offset)}
