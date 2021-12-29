#######################################################################
#### Project Name: Reinforcement Learning - An Interactive Example ####
#### Author: Vasileios Vasileiou                                   ####
#### Date: November 2021                                           ####
#######################################################################

#### Importing libraries ----
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
# import base64
from random import random

####  Initial parameter setting ----
app = Dash(__name__, prevent_initial_callbacks=True)
# logo_filename = 'logo.jpg' 
# encoded_image = base64.b64encode(open(logo_filename, 'rb').read())
n_coins = 10

df = pd.DataFrame(columns=['Number of coin tokens left', 
                           'Last bandit played',
                           'Profit from the last bandit', 
                           'Total profit'])

df = df.append({'Number of coin tokens left': n_coins, 
                'Last bandit played': 'None played yet',
                'Profit from the last bandit': 0, 
                'Total profit': 0}, ignore_index=True)

#### The brains of our bandits ----
def brain_bandit_1():
    r = random()
    if (r >= 0.8):
        profit = 13
    else:
        profit = 2
    ## Expected profit per play: 4.2
    return profit

def brain_bandit_2():
    r = random()
    if (r >= 0.5):
        profit = 5
    else:
        profit = 3
    ## Expected profit per play: 4.0
    return profit
        
def brain_bandit_3():
    r = random()
    if (r >= 0.9):
        profit = 45
    else:
        profit = 0
    ## Expected profit per play: 4.5
    return profit

#### App layout (Our frontend/UI) ----
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('Reinforcement Learning: A multi-armed bandit example'),
                                 html.Br(),
                                 html.P('''How to play: You have 10 token coins and there are three slot machines (bandits) to spend your coins on. 
                                           Click on a bandit to play and use one of your tokens. 
                                           '''),
                                 html.P('''The objective is to win as much money as possible so good luck!'''),
                                 html.Br(),
                                 html.Br(),
                                 html.Br(),
                                 html.Br(),
                                 html.P('Click any of the bandits below to play!'),
                                 html.Br(),
                                 html.Div([
                                 html.Button('Bandit 1: \"No dream is ever just a dream\"', style = {'background-color': 'rgb(255, 255, 255)', 
                                                                                                     'color': 'black',
                                                                                                     'border': 'none'
                                                                                                     },  id='btn-nclicks-1', n_clicks=0),
                                 html.Br(),
                                 html.Br(),
                                 html.Button('Bandit 2: \"Initiative comes to thems that wait\"', style = {'background-color': 'rgb(255, 255, 255)', 
                                                                                                     'color': 'black',
                                                                                                     'border': 'none'}, id='btn-nclicks-2', n_clicks=0),
                                 html.Br(),
                                 html.Br(),
                                 html.Button('Bandit 3: \"Here\'s Johnny!\"', style = {'background-color': 'rgb(255, 255, 255)', 
                                                                                                     'color': 'black',
                                                                                                     'border': 'none'}, id='btn-nclicks-3', n_clicks=0),
                                 html.Div(id='bandits')])
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True,
                                 figure=px.line(df,
                         x='Number of coin tokens left',
                         y='Total profit',
                         template='plotly_dark').update_layout(
                                   {'plot_bgcolor': 'rgba(30, 30, 30, 30)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'}).update_xaxes(range=[10,0]).update_yaxes(range=[0,140])
                                    ),
                                     html.Div(children=[
            html.P(id = 'live-update-text-coins-left', children = 'Number of coin tokens left: 10'),
            html.P(id = 'live-update-text-total-profit', children = 'Total profit: £0')
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),
            html.Br(),
            html.Br(),
                             dash_table.DataTable(
                                 id='table',
                                 columns=[{"name": i, "id": i} for i in df.columns],
                                 data=df.to_dict('records'),
                                    style_data_conditional=[{
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'rgba(30, 30, 30, 30)',
                                        'color': 'grey'
                                    },{
                                        'if': {'column_id': 'Total profit (£)'},
                                        'backgroundColor': 'rgba(30, 30, 30, 30)',
                                        'color': 'floralwhite',
                                        'fontWeight' : 'bold'
                                        }],
                                    style_header_conditional=[{
                                        'if': {'column_editable': False},
                                        'backgroundColor': 'rgba(30, 30, 30, 30)',
                                        'color': 'white'
                                    },{
                                        'if': {'column_id': 'Total profit (£)'},
                                        'backgroundColor': 'rgba(30, 30, 30, 30)',
                                        'color': 'floralwhite',
                                        'fontWeight' : 'bold'
                                       }
                                        ],
                                )
                            ])
                             ])
])

'''
Someone might ask hey "Vas, why did you set up the y limit to be 105?"
The answer is that the probability of passing it is very low. 
Just by trying the last bandit alone the probability is 1.28%
and I really don't expect that many people to play this app!!!
Uncomment to see why:
'''
# from scipy.stats import binom
# 1 - (binom.pmf(0, 10, 0.1) + binom.pmf(1, 10, 0.1) + binom.pmf(2, 10, 0.1) + binom.pmf(3, 10, 0.1))
                             
#### The Callback function - Our bridge between backend and frontend ----
## We need as many outputs as vars we want to display and as many inputs as the user selections/interactions
@app.callback(
    [Output('table', 'data'),
     Output('timeseries', 'figure'),
     Output('live-update-text-coins-left', 'children'),
     Output('live-update-text-total-profit', 'children'),
     ],
    [
    Input('table', 'data'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')]
)

#### Our main backend function ---- 
## Needs to have as many parameters as inputs and as many returns as outputs
def update_audit_table(df, *args):
    df = pd.DataFrame(df)
    coins_left = df.iloc[-1].values[0]
    total_profit = df.iloc[-1].values[3]
    if (coins_left > 0):
        bandit_played = [p['prop_id'] for p in callback_context.triggered][0]
        if 'btn-nclicks-1' in bandit_played:
            profit_now = brain_bandit_1()
            last_bandit = 'Bandit 1'
        elif 'btn-nclicks-2' in bandit_played:
            profit_now = brain_bandit_2()
            last_bandit = 'Bandit 2'
        elif 'btn-nclicks-3' in bandit_played:
            profit_now = brain_bandit_3()
            last_bandit = 'Bandit 3'
        df = df.append({'Number of coin tokens left': coins_left - 1, 
                        'Last bandit played': last_bandit,
                        'Profit from the last bandit': profit_now, 
                        'Total profit': total_profit + profit_now}, 
                        ignore_index=True)
    to_retun_fig = px.line(df,
                           x='Number of coin tokens left',
                           y='Total profit',
                           template='plotly_dark').update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'}).update_xaxes(range=[10,0]).update_yaxes(range=[0,140])
    to_return_coins_left = 'Number of coin tokens left: {}'.format(df['Number of coin tokens left'].iat[-1])
    to_return_profit = 'Total profit: £{}'.format(df['Total profit'].iat[-1])
    to_return_df = df.to_dict('records')
    return to_return_df, to_retun_fig, to_return_coins_left, to_return_profit
        
#### Start the app ----
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050)