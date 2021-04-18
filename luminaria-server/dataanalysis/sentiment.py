import numpy as np
import plotly.graph_objects as go

from common.enums import SeriesAttribute
from common.timeless import is_weekend
from database.stream.comment_frequency_model import CommentFrequencyModel
from vars import DB_CONFIG, DB_STATIC


def plot_freq(symbol, exclude_weekends=False):
    cursor1 = DB_CONFIG.execute_sql('''select date, sum(times_mentioned)
                                from COMMENT_FREQUENCY 
                                where symbol=?
                                GROUP BY date;''',
                                    (symbol,))

    from_date = CommentFrequencyModel.get_first_record_by_symbol(symbol).date

    cursor2 = DB_CONFIG.execute_sql('''select date, sum(times_mentioned)
                                from COMMENT_FREQUENCY 
                                where date >= ?
                                GROUP BY date;''',
                                    (from_date,))

    cursor3 = DB_STATIC.execute_sql('''select *
                                    from TIME_SERIES_DAILY_ADJUSTED 
                                    where date >= ? and symbol = ?
                                    order by date;''',
                                    (from_date, symbol))

    totals = []  # Total comments on a date
    x = []  # Date
    y_abs = []  # Absolute number of comments

    for row in cursor2.fetchall():
        if exclude_weekends and is_weekend(row[0]):
            totals.append(None)
        else:
            totals.append(row[1])

    i = 0
    for row in cursor1.fetchall():
        x.append(row[0])
        if exclude_weekends and is_weekend(row[0]):
            y_abs.append(None)
        else:
            y_abs.append(row[1])
        i += 1

    time_series_dates = []
    time_series_adjusted_closes = []
    time_series_volumes = []
    for row in cursor3.fetchall():
        time_series_dates.append(row[SeriesAttribute.DATE])
        time_series_adjusted_closes.append(row[SeriesAttribute.ADJUSTED_CLOSE])
        time_series_volumes.append(row[SeriesAttribute.VOLUME])

    assert len(x) == len(totals)

    x = np.array(x)
    totals = np.array(totals, dtype=np.float)
    y_abs = np.array(y_abs, dtype=np.float)
    y_normalized = y_abs / totals

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y_abs, mode='markers', name="Absolute"))
    fig.add_trace(go.Scatter(x=x, y=y_normalized, mode='markers', name="Percentage", yaxis="y2"))

    fig.add_trace(
        go.Scatter(x=time_series_dates, y=time_series_adjusted_closes, name='Close', mode='lines', yaxis="y3"))
    fig.add_trace(go.Bar(x=time_series_dates, y=time_series_volumes, opacity=0.1, name='Volume', yaxis="y4"))

    fig.update_layout(
        title="Exuberance " + symbol,
        xaxis_title="Date",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#7f7f7f"
        ),
        xaxis=dict(
            domain=[0.15, 0.9]
        ),
        yaxis=dict(
            title="Absolute Number of Comments",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="Percentage of Comments",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.05
        ),
        yaxis3=dict(
            title="Adjusted Close",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right",
            position=0.1
        ),
        yaxis4=dict(
            overlaying="y",
            visible=False,
            range=[0, max(time_series_volumes) * 4]
        ),
    )

    fig.show()
