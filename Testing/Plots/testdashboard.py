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

totaldata.to_csv('totaldata.csv', index=False)
"""
totaldata = pd.read_csv("totaldata.csv")
totaldata['FIPS'] = totaldata['FIPS'].astype(str)
totaldata['FIPS'] = totaldata['FIPS'].str.rjust(7, fillchar='0')
for i in totaldata.index:
    totaldata['FIPS'][i] = totaldata['FIPS'][i][0:5]

totaldata['CountyState'] = totaldata['County'] + ", " + totaldata['State']

distances = ['half', '1', '10', '20']
for el in distances:
    totaldata['LATotal%' + el] = totaldata['lapop' + el] / totaldata['POP2010'] * 100
    totaldata['LALow-Income%' + el] = totaldata['lalowi' + el] / totaldata['TractLOWI'] * 100
    totaldata['LAKids%' + el] = totaldata['lakids' + el] / totaldata['TractKids'] * 100
    totaldata['LASeniors%' + el] = totaldata['laseniors' + el] / totaldata['TractSeniors'] * 100
    totaldata['LAWhite%' + el] = totaldata['lawhite' + el] / totaldata['TractWhite'] * 100
    totaldata['LABlack%' + el] = totaldata['lablack' + el] / totaldata['TractBlack'] * 100
    totaldata['LAAsian%' + el] = totaldata['laasian' + el] / totaldata['TractAsian'] * 100
    totaldata['LAHispanic%' + el] = totaldata['lahisp' + el] / totaldata['TractHispanic'] * 100


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
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Food Access in the U.S.A. in 2015', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H2('Heat map', style={'color': '#df1e56'}),
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
                style={'width': '50em', 'verticalAlign': 'middle'},
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
                style={'width': '50em', 'verticalAlign': 'middle'},
                searchable=False
            )
        ], style={'display': 'inline-block', 'margin-right': '2em'})

    ]),
    dcc.Graph(id='graphic')
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


if __name__ == '__main__':
    app.run_server()
