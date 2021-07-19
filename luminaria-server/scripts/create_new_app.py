import os
from constants import ROOT_DIR


def create_app(app_name):
    def write(line):
        if line == '\n':
            file.write('\n')
        else:
            file.write(line + '\n')

    dir_name = app_name.lower()
    dir_path = os.path.join(ROOT_DIR, 'apps', dir_name)
    os.mkdir(dir_path)

    file = open('{0}/main.py'.format(dir_path), 'a+')
    write('from apps.baseapp import App')
    write('from common.enums import APP')
    write('\n')
    write('\n')
    write('class {0}(App):'.format(dir_name.title()))
    write('    APP_ID = APP.TBD')
    write('\n')
    write('    def __init__(self):')
    write('        super().__init__()')
    write('\n')
    write('    def execute(self, command, **kwargs):')
    write("        if command == 'call':")
    write("            return {'res': ''}")


if __name__ == "__main__":
    create_app('test')
