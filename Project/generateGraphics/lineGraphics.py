import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta, datetime
from calendar import monthrange


daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
colors = ['rgba(0,0,0,0)', 'rgb(0,0,0)', 'rgb(49,130,189)', 'rgb(189,189,189)', 'rgb(170, 187, 206)',
          'rgb(237, 187, 30)', 'rgb(216, 216, 216)', 'rgb(148, 162, 179)', 'rgb(187, 150, 27)']


def calHighestValue(value1, value2):
    val1 = max(value1)
    val2 = max(value2)

    highestValue = val1

    if val2 > highestValue:
        highestValue = val2

    return highestValue


def duringMonth(path, date1, date2, during_x, values_y1, values_y2):

    dayMonth = []
    X = []
    day1, month1, year1 = date1.split('-')
    day2, month2, year2 = date2.split('-')
    t1 = date(int(year1), int(month1), int(day1))
    t2 = date(int(year2), int(month2), int(day2))

    delta = timedelta(days=1)
    while t1 <= t2: #save Month array dayMonth
        dayMonth.append(t1.strftime("%d")+"-"+during_x[int(t1.strftime("%m"))-1])
        t1 += delta

    for i in range(0, len(dayMonth)):
        X.append(str(i))

    position1 = 0
    position3 = round(len(dayMonth) / 2)
    position2 = round(position3 / 2)
    position4 = round(position3 + position2)
    position5 = len(dayMonth) 
    Positions = [position1, position2, position3, position4, position5]

    PositionValues = [dayMonth[0], dayMonth[position2], dayMonth[position3], dayMonth[position4], dayMonth[-1]]

    values_y1_high = max(values_y1)
    values_y1_low = min(values_y1)

    n_pos_high_y1 = values_y1.index(values_y1_high)  # position value max
    n_pos_low_y1 = values_y1.index(values_y1_low)  # position value max

    values_y2_high = max(values_y2)
    values_y2_low = min(values_y2)

    n_pos_high_y2 = values_y2.index(values_y2_high)  # position value max
    n_pos_low_y2 = values_y2.index(values_y2_low)  # position value max

    fonte_size = 11

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=X,
            y=values_y1,
            name="yaxis data",
            mode='lines+markers+text',
            line=dict(
                color=colors[5],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
    )

    fig.add_trace(
        go.Scatter(
            x=X,
            y=values_y2,
            name="yaxis2 data",
            mode='lines+markers+text',
            # fill='toself',
            line=dict(
                color=colors[4],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
        secondary_y=True,

    )

    fig.update_layout(
        autosize=False,
        width=850,
        height=230,

        paper_bgcolor=colors[0],
        plot_bgcolor=colors[0],

        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=0
        ),

        showlegend=False,

        xaxis=dict(
            tickmode='array',
            tickvals=Positions,
            ticktext=PositionValues,
        )

    )

    ## high =============================================

    fig.add_annotation(
        x=n_pos_high_y1,
        y=values_y1_high,
        xref="x",
        yref="y",
        text="<b> " + str(values_y1_high) + "<b>",
        showarrow=True,
        font=dict(
            size=fonte_size,
            color='#fff',
        ),
        align="center",
        # yshift=20,

        arrowhead=6,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=colors[8],

        ax=0,
        ay=30,
        bordercolor=colors[8],
        borderwidth=1,
        borderpad=3,
        bgcolor=colors[5],  # colors[5],
        # opacity=0.7
    )

    fig.add_annotation(
        x=n_pos_high_y2,
        y=values_y2_high,
        xref="x",
        yref="y2",
        text="<b> " + str(values_y2_high) + "<b>",
        showarrow=True,
        font=dict(
            size=fonte_size,
            color='#fff',
        ),
        align="center",

        # yshift=-20,

        arrowhead=6,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=colors[7],

        ax=0,
        # ay=300,
        bordercolor=colors[7],
        borderwidth=1,
        borderpad=3,
        bgcolor=colors[4],
        # opacity=0.7
    )

    ## low =============================================

    fig.add_annotation(
        x=n_pos_low_y1,
        y=values_y1_low,
        xref="x",
        yref="y",
        text="<b> " + str(values_y1_low) + "<b>",
        showarrow=True,
        font=dict(
            size=fonte_size,
            color='#fff',
        ),
        align="center",
        # yshift=-20,

        arrowhead=6,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=colors[8],
        ax=0,
        ay=20,
        bordercolor=colors[8],
        borderwidth=1,
        borderpad=3,
        bgcolor=colors[5],
        # opacity=0.7
    )

    fig.add_annotation(
        x=n_pos_low_y2,
        y=values_y2_low,
        xref="x",
        yref="y2",
        text="<b> " + str(values_y2_low) + "<b>",
        showarrow=True,
        font=dict(
            size=fonte_size,
            color='#fff',
        ),

        align="center",
        # yshift=20,

        arrowhead=6,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=colors[7],
        ax=0,
        # ay=-300,
        bordercolor=colors[7],
        borderwidth=1,
        borderpad=3,
        bgcolor=colors[4],
        # opacity=0.7
    )
    Positions[2] = Positions[2] - 1
    Positions[1] = Positions[1] - 1
    Positions[3] = Positions[3] - 1
    Positions[4] = Positions[4] - 1

    # dashed creation
    for l in range(len(Positions)):
        # print(Positions[l])
        fig.add_shape(
            type="line",
            x0=Positions[l], y0=calHighestValue(values_y1, values_y2), x1=Positions[l], y1=2,
            line=dict(
                color=colors[6],
                width=1,
                dash="dash",
            )
        )

    fig.update_xaxes(
        showgrid=False,

        showticklabels=True,
        gridwidth=1,
        zeroline=False,
        color=colors[1],
        # title_standoff=0,
        # gridcolor='LightPink',
    )

    fig.update_yaxes(

        showticklabels=False,
        showgrid=False,
        zeroline=False,

    )

    fig.update_yaxes(

        showticklabels=False,
        showgrid=False,
        zeroline=False,

    )
    # fig.show()
    fig.write_image(path + "/During_Month.svg")


def weeklyTrend(path, week_x, values_y1, values_y2):
    highestValue = calHighestValue(values_y1, values_y2)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=week_x,
            y=values_y1,
            name="yaxis data",
            mode='lines',
            line=dict(
                color=colors[4],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
        secondary_y=False,

    )

    fig.add_trace(
        go.Scatter(
            x=week_x,
            y=values_y2,
            name="yaxis2 data",
            mode='lines',
            # fill='toself',
            line=dict(
                color=colors[5],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
        secondary_y=True,

    )

    fig.update_traces(
        # line_shape="spline"
        mode='lines',
    )

    fig.update_layout(
        autosize=False,
        width=850,
        height=230,

        paper_bgcolor=colors[0],
        plot_bgcolor=colors[0],

        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=0
        ),
        showlegend=False,

        # xaxis=dict(tickformat="dd")
    )

    # dashed creation
    for i in range(len(week_x)):
        fig.add_shape(
            type="line",
            x0=i, y0=highestValue, x1=i, y1=2,
            line=dict(
                color=colors[6],
                width=1,
                dash="dash",
            )
        )

    fig.update_xaxes(
        showgrid=False,
        showticklabels=True,
        gridwidth=1,
        zeroline=False,
        color=colors[1],
        title_standoff=0,

    )

    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        color=colors[1],

        # title_text="<b>right</b>",
        secondary_y=True,
    )
    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        color=colors[1],

        # title_text="<b>right</b>",
        secondary_y=False,
    )

    # fig.show()
    fig.write_image(path + "/Weekly_Trend_TwoLine.svg")


def dailyTrend(path, daily_x, values_y1, values_y2):
    highestValue = calHighestValue(values_y1, values_y2)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=daily_x,
            y=values_y1,
            name="yaxis data",
            line=dict(
                color=colors[4],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
        secondary_y=False,

    )

    fig.add_trace(
        go.Scatter(
            x=daily_x,
            y=values_y2,
            name="yaxis2 data",

            line=dict(
                color=colors[5],
                width=5,
                # dash='dash', ##dash options include 'dash', 'dot', and 'dashdot'
            ),

        ),
        secondary_y=True,

    )

    fig.update_traces(
        # line_shape="spline"
    )

    fig.update_layout(
        autosize=False,
        width=850,
        height=230,

        paper_bgcolor=colors[0],
        plot_bgcolor=colors[0],

        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=0
        ),
        showlegend=False,

        xaxis=dict(tickformat="dd")
    )

    # dashed creation (set)
    positions = {0, 6, 12, 18, 23}

    for i in range(len(daily_x)):
        if i in positions:
            fig.add_shape(
                type="line",
                x0=i, y0=highestValue, x1=i, y1=2,
                line=dict(
                    color=colors[6],
                    width=1,
                    dash="dash",
                )
            )

    # result = (range(len(daily_x)))
    # print(range(len(month_x)))
    # print(len(month_x) / 4)

    fig.update_xaxes(
        showgrid=False,
        showticklabels=True,
        gridwidth=1,
        zeroline=False,
        color=colors[1],
        # tickangle=0,
    )

    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        color=colors[1],

        # title_text="<b>right</b>",
        secondary_y=True,
    )
    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        color=colors[1],

        # title_text="<b>right</b>",
        secondary_y=False,
    )

    # fig.show()
    fig.write_image(path + "/Daily_Trend.svg")
