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

totaldata['LATotal%'] = totaldata['lapop10']/totaldata['POP2010'] * 100;
totaldata['LALow-Income%'] = totaldata['lalowi10']/totaldata['TractLOWI'] * 100;
totaldata['LAKids%'] = totaldata['lakids10']/totaldata['TractKids'] * 100;
totaldata['LASeniors%'] = totaldata['laseniors10']/totaldata['TractSeniors'] * 100;
totaldata['LAWhite%'] = totaldata['lawhite10']/totaldata['TractWhite'] * 100;
totaldata['LABlack%'] = totaldata['lablack10']/totaldata['TractBlack'] * 100;
totaldata['LAAsian%'] = totaldata['laasian10']/totaldata['TractAsian'] * 100;
totaldata['LAHispanic%'] = totaldata['lahisp10']/totaldata['TractHispanic'] * 100;

indicators = ['LATotal%', 'LALow-Income%', 'LAKids%', 'LASeniors%', 'LAWhite%', 'LABlack%', 'LAAsian%', 'LAHispanic%']


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
    html.H3('Heat map', style={'color': '#df1e56'}),
    dcc.Dropdown(
        id='dataset',
        options=[{'label': i, 'value': i} for i in indicators],
        value="LATotal%"
    ),
    dcc.Graph(id='graphic')
])

@app.callback(
    Output('graphic', 'figure'),
    Input('dataset', 'value'))
def update_graph(dataset_name):
    fig = px.choropleth(totaldata, geojson=counties, locations='FIPS', color=dataset_name,
     color_continuous_scale='fall',
     range_color=(totaldata[dataset_name].quantile(0.05), totaldata[dataset_name].quantile(0.95)),
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
