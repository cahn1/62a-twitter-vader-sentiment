import json
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

from api.twitter import Twitter
from common import util as u

# Reference
#https://datascienceparichay.com/article/get-data-from-twitter-api-in-python-step-by-step-guide/

# Global variables
tab_title = 'Twitter HashTag Search'
source_url = 'https://github.com/twitterdev/Twitter-API-v2-sample-code'
github_link = 'https://github.com/cahn1/62a-twitter-vader-sentiment'


# Default figure
def base_fig():
    data = go.Table(
        columnwidth=[170, 170, 590, 110, 360],
        header={'values': ['AUTHOR_ID', 'ID', 'TEXT', 'SCORE', 'SENTIMENT'],
                'line_color': '#eeeeee',
                'fill_color': '#e0e8ea',
                'font': dict(color='#5b5b5b', size=11, family="Courier New",),
                'align': ['left']},
        cells={
            'align': ['left'],
            'values': []
        }
    )
    fig = go.Figure([data])
    return fig


def render_output(params):
    tw = Twitter()
    data = tw.submit(params, '').get('data', {})
    #print(json.dumps(data, indent=4, sort_keys=True))
    df_tweepy = pd.DataFrame(data)
    df_tweepy[['score', 'sentiment']] = \
        df_tweepy['text'].apply(u.analyze_sentiment)

    # Render table
    data = go.Table(
        columnwidth=[170, 170, 590, 110, 360],
        header=dict(
            values=df_tweepy.columns.str.upper(),
            line_color='#eeeeee',
            fill_color='#e0e8ea',
            font=dict(color='#5b5b5b', size=11, family="Courier New",),
            align=['left']),
        cells=dict(
            align=['left'],
            values=[
                df_tweepy['author_id'].values,
                df_tweepy['id'].values,
                df_tweepy['text'].values,
                df_tweepy['score'].values,
                df_tweepy['sentiment'].values
            ],
            line_color='#eeeeee',
            fill_color='#ecf0f1',
            font=dict(color='black', size=12, family="Courier New",)
        )
    )
    table = go.Figure([data])
    #print(f"score={df_tweepy['score']}")
    df_tweepy['score_float'] = df_tweepy['score'].apply(u.to_float)
    #print(f"score_float={df_tweepy['score_float']}")

    figure = go.Figure(
        go.Box(
            x=df_tweepy['score_float'],
            fillcolor='#a9dfbf',
            boxpoints='all'
        )
    )
    return table, figure


# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tab_title

# app component layout
app.layout = html.Div(
    children=[
        html.H1("Keyword search and vader sentiment analysis via Twitter's "
                "API"),
        html.Div(
            children=[
                dcc.Input(
                    id='input-1-state',
                    type='text',
                    placeholder='Enter search term'),
                html.Button(
                    id='submit-button-state',
                    n_clicks=0,
                    children='Vader'),
                html.Div(id='output-state1'),
                dcc.Graph(id='figure-1'),
                html.Div(id='output-state2'),
                dcc.Graph(id='table-1'),
            ],
            className='twelve columns'),
        # Footer
        html.Br(), html.Br(),
        html.A('Code on Github', href=github_link),
        html.Br(),
        html.A("Data Source", href=source_url),
    ]
)


# callback
@app.callback(
    Output('table-1', 'figure'),
    Output('figure-1', 'figure'),
    [Input('submit-button-state', 'n_clicks')],
    [State('input-1-state', 'value')])
def update_output(n_clicks, term):
    if n_clicks == 0:
        return base_fig(), go.Figure(go.Box(x=[0]))
    return render_output(u.render_query(term))


if __name__ == '__main__':
    app.run_server(debug=True)
