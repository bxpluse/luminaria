class Messenger:

    def __init__(self, socketio):
        self.socketio = socketio

    def toast(self, message):
        self.socketio.emit('toast-message', {'message': message})

    def status(self, app, status):
        self.socketio.emit('toast-status', {'name': app, 'status': status})
