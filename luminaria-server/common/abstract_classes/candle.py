class Candle:

    def __init__(self):
        pass

    def get_close(self):
        pass

    def get_last(self):
        pass

    def get_date(self):
        pass

    def get_time(self):
        pass

    def get_datetime(self):
        return str(self.get_date()) + ' ' + str(self.get_time())
