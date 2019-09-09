import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s==%(funcName)s==%(message)s')

all_names = pd.read_csv('data/by_yr_name_sex.csv')

app = dash.Dash()
server = app.server
app.title = 'US Baby Names, Births per Year 1910 - 2016'

app.layout = html.Div([
    dcc.Graph(id='by_year_graph',
              config={'displayModeBar': False}),
    html.Div([
        dcc.Dropdown(id='select_names',
                     multi=True,
                     value=tuple(),
                     placeholder='Search for a name(s)',
                     options=[{'label': name, 'value': name}
                              for name in sorted(all_names['names'].unique(), key=lambda s: (s, len(s)))]),
        
    ], style={'width': '60%', 'margin-left': '20%'}),
    html.Div([
        html.Br() for x in range(5)
    ])
], style={'background-color': '#eeeeee', 'font-family': 'Palatino'})

@app.callback(Output('by_year_graph', 'figure'),
             [Input('select_names', 'value')])
def plot_names_by_year(nameslist):
    logging.info(msg=locals())
    df = all_names[all_names['names'].isin(nameslist)].groupby(['year','names'])['births'].sum().to_frame().reset_index()
    return {
        'data': [go.Scatter(x=df[df['names'] == n]['year'],
                            y=df[df['names'] == n]['births'],
                            mode='markers',
                            marker={'size': 10, 'opacity': 0.65},
                            name=n)
                 for n in nameslist],
        'layout': go.Layout(title='US Baby Names (births per year) 1910 - 2016<br>' + ', '.join(nameslist),
                            xaxis={'tickvals': [str(x) for x in range(1910, 2030, 10)],
                                   'tickfont': {'size': 15}},
                            yaxis={'tickfont': {'size': 15},
                                   'zeroline': False},
                            paper_bgcolor='#eeeeee',
                            plot_bgcolor='#eeeeee',
                            height=600,
                            font={'family':'Palatino'})
    }

if __name__ == '__main__':
    app.run_server()