import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash

cor = ['rgb(252, 194, 25)', 'rgb(102, 100, 101)', 'rgba(0,0,0,0)', 'rgb(255, 255, 255)', 'rgba(0,0,0)']
background = ['rgba(0,0,0,0)']


# external CSS stylesheets
# external_stylesheets = ['https://tomiworld.com/resources/style.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def modules(path, values, labels, colors):
    
    for i in range(len(values)):
        if values[i] <= 7:
            labels[i]=""


    fig = go.Figure(
        data=[go.Pie(
            # Events: , Transports: ,  Search: ,  News: ,
           
            labels=labels,
            values=values)])

    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='label',
        textfont_size=40,
        textfont_color=cor[4],
        textposition='inside',
        marker=dict(
            colors=colors,
            line=dict(
                color=cor[3],
                width=5
            )
        )
    )

    fig.update(
        layout_showlegend=False,
    )

    fig.update_layout(
        autosize=False,

        width=300,
        height=300,

        paper_bgcolor=cor[2],
        plot_bgcolor=cor[2],

        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=4
        ),

        font_family="TomiFont",

    ),

    #fig.show()
    fig.write_image(path+"/Modules_Graphic.svg")


#======= action chart
def actions(path, values, colors, text):
    #text="ACTIONS BY <br> TOURISTS AND <br> LOCALS"
    labels = []
    
    for i in range(0, len(values)):
        labels.append(i)

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(
        rows=1,
        cols=1,
        specs=[[{'type': 'domain'}]])

    fig.add_trace(go.Pie(
        labels=labels,
        # values = ["79%", "18%", "3%"]
        values=values,
        name='GHG',
        marker_colors=colors,

    ))

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(
        hole=.7,
        hoverinfo="label+percent+name",
        textinfo='none',
        textfont_color=cor[3],

    )

    fig.update(
        layout_showlegend=False,
    )

    fig.update_layout(
        autosize=False,

        width=300,
        height=300,

        paper_bgcolor=background[0],

        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=4
        ),
        legend=dict(
            y=0.5,
            traceorder='reversed',
            # font=dict(size=50),
            # itemwidth=50,
            # itemsizing='constant',
        ),
        annotations=[
            dict(
                text=text,
                font_size=15,
                showarrow=False,
            )
        ]
    ),

    #fig.show()
    fig.write_image(path+"/Actions_Locals.svg")
