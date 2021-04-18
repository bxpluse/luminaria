from apps.baseapp import App
from common.enums import APP
from database.dynamic.note_model import NoteModel


class Notes(App):
    APP_ID = APP.NOTES

    def __init__(self):
        super().__init__()

    def save(self, content):
        NoteModel.save_note(content)

    def load(self):
        content = str(NoteModel.load_note())
        return content

    def execute(self, command, **kwargs):
        if command == 'save':
            content = kwargs['content']
            self.save(content)
            return {}
        elif command == 'load':
            return {'content': self.load()}
