import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
import os
import json
import pandas as pd
from api_keys.myapikey import apikey



########### Define a few variables ######

tabtitle = 'Twitter Search'
sourceurl = 'https://github.com/twitterdev/Twitter-API-v2-sample-code'
githublink = 'https://github.com/shepparjani/twitterapi.git'
placeholderinput = ""


########### Set up the default figures ######

def base_fig():
    data=go.Table(columnwidth = [200,200,1000],
                    header=dict(values=['author_id', 'id', 'text'], align=['left']),
                    cells=dict(align=['left'],
                               values=[[1,2,3],
                                       [1,2,3],
                                       ['waiting for data','waiting for data','waiting for data']])
                 )
    fig = go.Figure([data])
    return fig

########## Authorization ############
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    bearer_token = apikey


    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    #if response.status_code != 200:
        #raise Exception(response.status_code, response.text)
    return response.json()

def generate_output(search_url, query_params):
    json_response = connect_to_endpoint(search_url, query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    tweetdict = json_response["data"]
    tweetdf = pd.DataFrame(tweetdict)

    #set up table
    data=go.Table(columnwidth = [200,200,1000],
                    header=dict(values=tweetdf.columns, align=['left']),
                    cells=dict(align=['left'],
                               values=[tweetdf['author_id'].values,
                                       tweetdf['id'].values,
                                       tweetdf['text'].values])
                 )
    figure = go.Figure([data])
    return figure



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

###########Layout#############
app.layout = html.Div(children=[
    html.H1("Keyword searches with Twitter's API"),
    html.Div(children=[
        dcc.Input(id='input-1-state', type='text', value='Enter search terms'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Div(id='output-state'),
        dcc.Graph(id='figure-1'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


########### Callback ###########
@app.callback(Output('figure-1', 'figure'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value')]
             )

### Is this the correct variable for the parens?
def update_output(n_clicks, children):

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': children,'tweet.fields': 'author_id','user.fields': 'location', 'max_results': 25}


    if n_clicks==0:
        return base_fig()
    elif n_clicks>=1:
        return generate_output(search_url, query_params)

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
