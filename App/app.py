import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from urllib.request import urlopen
import json
import plotly.express as px

# Load CSV file
data = pd.read_csv("totaldata.csv")

# Initializing variables for use in Dash
countystatelist = data.CountyState.unique()

distances = ['half', '1', '10', '20']

indicators = [['Total', 'LATotal%'],
              ['Low-Income', 'LALow-Income%'],
              ['Kids', 'LAKids%'],
              ['Seniors', 'LASeniors%'],
              ['White', 'LAWhite%'],
              ['Black', 'LABlack%'],
              ['Asian', 'LAAsian%'],
              ['Hispanic', 'LAHispanic%']]

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


#Dash app initialization
app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.H1(children='Visualizing Food Access in the U.S.A.',
            style={
                'textAlign': 'center',
                'color': 'SlateBlue'
            }
            ),
    html.Div('An MVP Developed by Group 8 for ITSC 3155', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H2('Heat Map', style={'color': 'SlateBlue'}),
    html.Div('The values shown on the map are the percent of people in the given population type that live beyond the given distance from the nearest supermarket'),
    html.Br(),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3("""Population Filter:""",
                        style={'margin-right': '2em'})
            ]),
            dcc.Dropdown(
                id='dataset',
                options=[{'label': i[0], 'value': i[1]} for i in indicators],
                value="LATotal%",
                placeholder='Population type...',
                style={'width': '45em', 'verticalAlign': 'middle'},
                searchable=False
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'}),
        html.Div(children=[
            html.Div(children=[
                html.H3("""Distance From Nearest Supermarket:""",
                        style={'margin-right': '2em'})
            ]),
            dcc.Dropdown(
                id='distance',
                options=[
                    {'label': 'Beyond 0.5 mi', 'value': 'half'},
                    {'label': 'Beyond 1 mi', 'value': '1'},
                    {'label': 'Beyond 10 mi', 'value': '10'},
                    {'label': 'Beyond 20 mi', 'value': '20'},
                ],
                value='half',
                placeholder='Distance...',
                style={'width': '45em', 'verticalAlign': 'middle'},
                searchable=False
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'})

    ]),
    dcc.Graph(id='graphic'),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.Br(),
    html.H2('County Search', style={'color': 'SlateBlue'}),
    html.Div('This bar graph shows the percent of people in each population type that live beyond the given distance from the nearest supermarket. Each of these values is compared with the state average.'),
    html.Br(),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3("""County Name:""",
                        style={'margin-right': '2em'})
            ]),
            dcc.Dropdown(
                id='countystateforsearch',
                value='Autauga, Alabama',
                placeholder='County, State...',
                options=[{'label': i, 'value': i} for i in countystatelist],
                style={'width': '45em', 'height':'2em', 'verticalAlign': 'top'},
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'}),
        html.Div(children=[
            html.Div(children=[
                html.H3("""Distance From Nearest Supermarket:""",
                        style={'margin-right': '2em'})
            ]),
            dcc.Dropdown(
                id='distanceforsearch',
                options=[
                    {'label': 'Beyond 0.5 mi', 'value': 'half'},
                    {'label': 'Beyond 1 mi', 'value': '1'},
                    {'label': 'Beyond 10 mi', 'value': '10'},
                    {'label': 'Beyond 20 mi', 'value': '20'},
                ],
                value='half',
                placeholder='Distance...',
                style={'width': '45em', 'verticalAlign': 'top'},
                searchable=False
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'})
    ], style={'display':'flex', 'flex-wrap':'wrap'}),
    dcc.Graph(id='searchgraphic')
])

# Callback method to update heat map
@app.callback(
    Output('graphic', 'figure'),
    Input('dataset', 'value'),
    Input('distance', 'value'))
def update_graph(dataset_name, distance_value):
    fig = px.choropleth(data, geojson=counties, locations='FIPS', color=dataset_name + distance_value,
     color_continuous_scale='fall',
     range_color=(data[dataset_name + distance_value].quantile(0.05),
                  data[dataset_name + distance_value].quantile(0.95)),
     scope='usa',
     hover_name="CountyState",
    )
    
    fig.update_layout(autosize=False,
        margin = dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=4,
                autoexpand=True
            ),
        width=1500)
    
    return fig

# Callback method to update bar chart
@app.callback(
    Output('searchgraphic', 'figure'),
    Input('countystateforsearch', 'value'),
    Input('distanceforsearch', 'value'),
    Input('searchgraphic', 'figure'))
def update_search_graph(county_state_name, distance_value, prev_graphic):
    county_values = []
    state_values = []
    for val in [col[1] for col in indicators]:
        county_val_list = data.loc[data['CountyState']==county_state_name,val+distance_value].tolist()
        state_val_list = data.loc[data['CountyState']==county_state_name,val+distance_value+'avg'].tolist()
        if county_val_list and state_val_list:
            county_values.append(county_val_list[0])
            state_values.append(state_val_list[0])
    
    if county_values and state_values:
        fig = go.Figure(data=[
            go.Bar(name='County Average', x=[col[0] for col in indicators], y=county_values),
            go.Bar(name='State Average', x=[col[0] for col in indicators], y=state_values)
        ])
        fig.update_layout(barmode='group')
    else:
        fig = prev_graphic
    
    return fig

# Start Dash server
if __name__ == '__main__':
    app.run_server()
