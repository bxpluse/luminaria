import numpy as np
import plotly.graph_objects as go
import plotly

from common.timeless import is_weekend
from constants import DB_STREAM
from database.stream.comment_frequency_model import CommentFrequencyModel


def plot_freq(symbol, show=False):
    cursor1 = DB_STREAM.execute_sql('''select date, sum(times_mentioned)
                                from COMMENT_FREQUENCY 
                                where symbol=?
                                GROUP BY date;''',
                                    (symbol,))

    from_date = CommentFrequencyModel.get_first_record_by_symbol(symbol).date

    cursor2 = DB_STREAM.execute_sql('''select date, sum(times_mentioned)
                                from COMMENT_FREQUENCY 
                                where date >= ?
                                GROUP BY date;''',
                                    (from_date,))

    totals = []         # Total comments on a date
    x = []              # Date
    y_abs_weekday = []  # Absolute number of comments on weekdays
    y_abs_weekend = []  # Absolute number of comments on weekends

    for row in cursor2.fetchall():
        totals.append(row[1])

    for row in cursor1.fetchall():
        x.append(row[0])
        if is_weekend(row[0]):
            y_abs_weekday.append(None)
            y_abs_weekend.append(row[1])
        else:
            y_abs_weekday.append(row[1])
            y_abs_weekend.append(None)

    assert len(x) == len(totals)

    x = np.array(x)
    totals = np.array(totals, dtype=float)
    y_abs_weekday = np.array(y_abs_weekday, dtype=float)
    y_abs_weekend = np.array(y_abs_weekend, dtype=float)
    y_weekday_normalized = y_abs_weekday / totals
    y_weekend_normalized = y_abs_weekend / totals

    fig = go.Figure()

    marker_abs = dict(color='#345fef')
    marker_per = dict(color='#ef18a9')

    fig.add_trace(go.Scatter(x=x, y=y_abs_weekday, mode='markers', marker=marker_abs, name="Absolute", fillcolor='red'))
    fig.add_trace(go.Scatter(x=x, y=y_abs_weekend, mode='markers', marker=marker_abs, name="Absolute(weekend)"))

    fig.add_trace(
        go.Scatter(x=x, y=y_weekday_normalized, mode='markers', marker=marker_per, yaxis="y2", name="Percentage"))
    fig.add_trace(go.Scatter(x=x, y=y_weekend_normalized, mode='markers', marker=marker_per, yaxis="y2",
                             name="Percentage(weekend)"))

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
    )

    if show:
        fig.show()
    return plotly.offline.plot(fig, output_type='div', auto_open=False, include_plotlyjs="cdn")
