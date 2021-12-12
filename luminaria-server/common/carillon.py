from common.abstract_classes.rule import Rule
from common.alerts.quote_alert import QuoteAlert
from common.api.quote import get_candle


def create(rule: Rule, alert: QuoteAlert):
    return rule.create_subrule(
        subrule_name=alert.symbol,
        func=scan,
        args=alert,
        metadata={'symbol': alert.symbol, 'below': alert.below, 'above': alert.above},
        triggers={
            'end_date': alert.end_time,
            'day_of_week': 'mon,tue,wed,thu,fri',
            'hour': '10-15',
        }
    )


def scan(alert: QuoteAlert):
    if not alert.is_suppressed():
        candle = get_candle(alert.symbol, interval='1m')
        last = candle.get_last()
        if last < alert.below or last > alert.above:
            alert.send('Threshold breached for {0} | Last {1} | Below {2} | Above {3}'
                       .format(alert.symbol, last, alert.below, alert.above))
            alert.cancel()
            return 'Threshold breached. Last was {0}'.format(str(last))
        return 'No action. Last was {0}'.format(str(last))
    return 'Alert is suppressed'
