import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from urllib.request import urlopen
import json
import plotly.express as px
import functools

# Load CSV file from Datasets folder
"""
df1 = pd.read_csv('../Datasets/FoodDataCSV.csv')
fips = pd.read_excel('../Datasets/all-geocodes-v2019.xlsx', skiprows=4)

currentCounty = "Autauga"
countyCountList = []
count = 0
for i in df1.index:
    if df1['County'][i] == currentCounty:
        count += 1
    else:
        countyCountList.append([df1['State'][i-1], currentCounty, count])
        currentCounty = df1['County'][i]
        count = 1

countyCountDF = pd.DataFrame(countyCountList, columns = ["State", "County", "TractCount"])

data = df1.groupby(['State','County']).sum()

totaldata = pd.merge(data, countyCountDF, on=["State","County"], how="left")

fips_counties = fips[fips['Summary Level'] == 50]

fips_counties['County Code (FIPS)'] = fips_counties['County Code (FIPS)'].astype(str)
fips_counties['County Code (FIPS)'] = fips_counties['County Code (FIPS)'].str.rjust(3, fillchar='0')

fips_counties['State Code (FIPS)'] = fips_counties['State Code (FIPS)'].astype(str)
fips_counties['State Code (FIPS)'] = fips_counties['State Code (FIPS)'].str.rjust(2, fillchar='0')

fips_counties['FIPS'] = fips_counties['State Code (FIPS)'] + fips_counties['County Code (FIPS)']

to_remove = [" County", " Census Area", " Borough", " Municipality", " Parish"]

for i in fips_counties.index:
    fips_counties["Area Name (including legal/statistical area description)"][i] = functools.reduce(lambda s, pat: s.split(pat, 1)[0], to_remove, fips_counties["Area Name (including legal/statistical area description)"][i])

fips_states = fips[fips['Summary Level'] == 40]
fips_states['State Code (FIPS)'] = fips_states['State Code (FIPS)'].astype(str)
fips_states['State Code (FIPS)'] = fips_states['State Code (FIPS)'].str.rjust(2, fillchar='0')
fips_states_dict = {}

for i in fips_states.index:
    fips_states_dict[fips_states["State Code (FIPS)"][i]] = fips_states["Area Name (including legal/statistical area description)"][i]

fips_list = []
for i in fips_counties.index:
    fips_list.append([fips_states_dict[fips_counties["State Code (FIPS)"][i]], fips_counties["Area Name (including legal/statistical area description)"][i], fips_counties["FIPS"][i]])

fips_DF = pd.DataFrame(fips_list, columns = ["State", "County", "FIPS"])

totaldata = pd.merge(totaldata, fips_DF, on=["State","County"], how="left")

totaldata['CountyState'] = totaldata['County'] + ", " + totaldata['State']

for el in distances:
    totaldata['LATotal%' + el] = totaldata['lapop' + el] / totaldata['POP2010'] * 100
    totaldata['LALow-Income%' + el] = totaldata['lalowi' + el] / totaldata['TractLOWI'] * 100
    totaldata['LAKids%' + el] = totaldata['lakids' + el] / totaldata['TractKids'] * 100
    totaldata['LASeniors%' + el] = totaldata['laseniors' + el] / totaldata['TractSeniors'] * 100
    totaldata['LAWhite%' + el] = totaldata['lawhite' + el] / totaldata['TractWhite'] * 100
    totaldata['LABlack%' + el] = totaldata['lablack' + el] / totaldata['TractBlack'] * 100
    totaldata['LAAsian%' + el] = totaldata['laasian' + el] / totaldata['TractAsian'] * 100
    totaldata['LAHispanic%' + el] = totaldata['lahisp' + el] / totaldata['TractHispanic'] * 100

totaldata = pd.read_csv("totaldata.csv")
totaldata['FIPS'] = totaldata['FIPS'].astype(str)
totaldata['FIPS'] = totaldata['FIPS'].str.rjust(7, fillchar='0')
for i in totaldata.index:
    totaldata['FIPS'][i] = totaldata['FIPS'][i][0:5]

tempdict = {}
for el in distances:
    tempdict['LATotal%' + el + 'avg'] = []
    tempdict['LALow-Income%' + el + 'avg'] = [] 
    tempdict['LAKids%' + el + 'avg'] = [] 
    tempdict['LASeniors%' + el + 'avg'] = [] 
    tempdict['LAWhite%' + el + 'avg'] = [] 
    tempdict['LABlack%' + el + 'avg'] = []
    tempdict['LAAsian%' + el + 'avg'] = []
    tempdict['LAHispanic%' + el + 'avg'] = []
    for i in totaldata.index:
        tempdict['LATotal%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LATotal%' + el].mean())
        tempdict['LALow-Income%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LALow-Income%' + el].mean())
        tempdict['LAKids%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LAKids%' + el].mean())
        tempdict['LASeniors%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LASeniors%' + el].mean())
        tempdict['LAWhite%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LAWhite%' + el].mean())
        tempdict['LABlack%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LABlack%' + el].mean())
        tempdict['LAAsian%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LAAsian%' + el].mean())
        tempdict['LAHispanic%' + el + 'avg'].append(totaldata.loc[totaldata['State'] == totaldata['State'][i], 'LAHispanic%' + el].mean())

for el in distances:
   totaldata['LATotal%' + el + 'avg'] = tempdict['LATotal%' + el + 'avg']
   totaldata['LALow-Income%' + el + 'avg'] = tempdict['LALow-Income%' + el + 'avg']
   totaldata['LAKids%' + el + 'avg'] = tempdict['LAKids%' + el + 'avg']
   totaldata['LASeniors%' + el + 'avg'] = tempdict['LASeniors%' + el + 'avg']
   totaldata['LAWhite%' + el + 'avg'] = tempdict['LAWhite%' + el + 'avg']
   totaldata['LABlack%' + el + 'avg'] = tempdict['LABlack%' + el + 'avg']
   totaldata['LAAsian%' + el + 'avg'] = tempdict['LAAsian%' + el + 'avg']
   totaldata['LAHispanic%' + el + 'avg'] = tempdict['LAHispanic%' + el + 'avg']

totaldata.to_csv('totaldata.csv', index=False)
"""

totaldata = pd.read_csv("totaldata.csv")

countylist = totaldata.County.unique()

statelist = totaldata.State.unique()

test2 = 0

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

"""
rank_fig = px.choropleth(totaldata, geojson=counties, locations='FIPS', color='LA1and10 Per Tract',
 color_continuous_scale='fall',
 range_color=(0, 100),
 scope='usa',
 labels={''}
 )
"""

app = dash.Dash()


# Layout
app.layout = html.Div(children=[
    html.H1(children='Visualizing Food Access in the U.S.A.',
            style={
                'textAlign': 'center',
                'color': 'SlateBlue'
            }
            ),
    html.Div('A MVP Developed by Group 8 for ITSC 3155', style={'textAlign': 'center'}),
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
                id='countyforsearch',
                value='Autauga',
                placeholder='County...',
                options=[{'label': i, 'value': i} for i in countylist],
                style={'width': '30em', 'height':'2em', 'verticalAlign': 'top'},
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'}),
        html.Div(children=[
            html.Div(children=[
                html.H3("""State Name:""",
                        style={'margin-right': '2em'})
            ]),
            dcc.Dropdown(
                id='stateforsearch',
                value='Alabama',
                placeholder='State...',
                options=[{'label': i, 'value': i} for i in statelist],
                style={'width': '30em', 'height':'2em', 'verticalAlign': 'top'},
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
                style={'width': '30em', 'verticalAlign': 'top'},
                searchable=False
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'})
    ], style={'display':'flex', 'flex-wrap':'wrap'}),
    dcc.Graph(id='searchgraphic')
])

@app.callback(
    Output('graphic', 'figure'),
    Input('dataset', 'value'),
    Input('distance', 'value'))
def update_graph(dataset_name, distance_value):
    fig = px.choropleth(totaldata, geojson=counties, locations='FIPS', color=dataset_name + distance_value,
     color_continuous_scale='fall',
     range_color=(totaldata[dataset_name + distance_value].quantile(0.05),
                  totaldata[dataset_name + distance_value].quantile(0.95)),
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

@app.callback(
    Output('searchgraphic', 'figure'),
    Input('countyforsearch', 'value'),
    Input('stateforsearch', 'value'),
    Input('distanceforsearch', 'value'),
    Input('searchgraphic', 'figure'))
def update_search_graph(county_name, state_name, distance_value, prev_graphic):
    county_values = []
    state_values = []
    for val in [col[1] for col in indicators]:
        county_val_list = totaldata.loc[(totaldata['State']==state_name) & (totaldata['County']==county_name),val+distance_value].tolist()
        state_val_list = totaldata.loc[(totaldata['State']==state_name) & (totaldata['County']==county_name),val+distance_value+'avg'].tolist()
        if county_val_list and state_val_list:
            county_values.append(county_val_list[0])
            state_values.append(state_val_list[0])
    print(county_values)
    print(state_values)
    
    if county_values and state_values:
        fig = go.Figure(data=[
            go.Bar(name='County Average', x=[col[0] for col in indicators], y=county_values),
            go.Bar(name='State Average', x=[col[0] for col in indicators], y=state_values)
        ])
        fig.update_layout(barmode='group')
    else:
        fig = prev_graphic
    
    return fig

if __name__ == '__main__':
    app.run_server()
