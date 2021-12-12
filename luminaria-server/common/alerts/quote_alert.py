from datetime import datetime, timedelta

from common.alerts.alert import Alert


class QuoteAlert(Alert):

    def __init__(self, symbol, below, above, days_to_cancel):
        super().__init__('QuoteAlert')
        self.symbol = symbol.upper()
        self.below = float(below)
        self.above = float(above)
        self.end_time = datetime.now() + timedelta(days=int(days_to_cancel))

    def is_suppressed(self):
        if self.rule is not None:
            return self.rule.suppressed
        return super().is_suppressed()

    def cancel(self):
        if self.rule is not None:
            self.rule.remove_subrule(self.symbol)

    def __str__(self):
        return 'Scanning for {0} at below {1} or above {2}'.format(self.symbol, str(self.below), str(self.above))

    def __repr__(self):
        return 'QuoteAlert(symbol={0}, below={1}, above={2})'.format(self.symbol, str(self.below), str(self.above))
