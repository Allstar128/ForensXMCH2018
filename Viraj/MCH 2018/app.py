## Bootstrap Grid tutorial - adding style to the app

import pandas as pd
import numpy as np

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html


df = pd.read_csv('Encoded_Data.csv')

app = dash.Dash()

non_encoded = pd.read_csv('database.csv')

text = [df['School Name'], df['Economic Need Index']]
mapbox_access_token = "pk.eyJ1IjoicGFudDIwMDIiLCJhIjoiY2prenlwb2ZtMHlnMjNxbW1ld3VxYWZ4cCJ9.rOb8DhCzsysBIw69MxyWKg"

app.title = "NY: Educational Infrastructure"

#Data Crap
all_cities = non_encoded["City"].unique()
cities_schools = pd.DataFrame()
cities = np.array([])
eni_value = np.array([])
count = np.array([])
for city in all_cities:
    cities = np.append(city, cities)
    city_data = non_encoded[non_encoded['City'] == city]
    city_total = len(city_data['District'])
    count = np.append(city_total, count)
cities_schools['City'] = cities
cities_schools['Count'] = count

yuh = ["BROOKLYN", "BRONX", "NEW YORK", "STATEN ISLAND", "JAMAICA"]
bc_calc = []
for bet in yuh:
    k = non_encoded[non_encoded['City'] == bet]
    precal = k['Economic Need Index'].mean()
    conjugate = round(precal,3)
    bc_calc.append(conjugate)
    
cities_schools.head(20)
cities_schools = cities_schools.sort_values('Count')
cities_schools = cities_schools[::-1]

y10 = np.array([411, 297, 232, 60, 32])
color10 = np.array(['rgb(255,255,255)']*y10.shape[0])
color10[y10 % 411 == 0] = 'rgb(34, 94, 168)'
color10[y10 % 297 == 0 ] = 'rgb(54, 114, 188)'
color10[y10 % 232 == 0] = 'rgb(74, 124, 198)'
color10[y10 % 60 == 0 ] = 'rgb(94, 144, 188)'
color10[y10 % 32 == 0] = 'rgb(114, 164, 208)'

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501

app.layout = html.Div([
    html.Div([
        html.Div(
            [
                html.H1(children='NY: Educational Infrastucture',
                        className='nine columns',
                        style = {
                            'margin-top':35,
                            'font-family':"Arial",
                        }),
                html.Img(
                    src="http://p10cdn4static.sharpschool.com/UserFiles/Servers/Server_109143/Image/Logo/JCIB-Logo-Website.png",
                    className='three columns',
                    style={
                        'height': '10%',
                        'width': '10%',
                        'float': 'right',
                        'position': 'relative',
                        'margin-top': 5,
                    },
                ),
                html.Div(children='''
                        ForensX Magic City Hacks: An indepth investigation of the educational infrastructure of New York State.
                        We provide a model for the accurate prediction of the economic need of schools and monitoring of their performance. 
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='map-1',
                    figure={
                        'data': [
                            {
                              "type": "scattermapbox",
                                "lat": list(df['Latitude']),
                                "lon": list(df['Longitude']),
                                "text": non_encoded['School Name'],
                                "mode": "markers",
                                "name": list(non_encoded['School Name']),
                                "marker": {
                                    "size": df['School Income Estimate']/8000,
                                    "colorscale":"YlGnBu",
                                    "colorbar" : {
                                        "thickness" : 10,
                                        "ticks" : "outside",
                                    },
                                    "opacity": 1,
                                    "color": df['Economic Need Index']  
                                }
                            },
                        ],
                        'layout': {
                            'title': 'ENI Distribution: Geospatial Analysis<br>Color = Economic Need Index (ENI). Size = School Estimated Income.</br>',
                            "autosize" : True,
                            "hovermode": "closest",
                            "mapbox": {
                                "accesstoken" : mapbox_access_token,
                                "bearing": 0,
                                "center": {
                                    "lat" : 40.70,
                                    "lon" : -73.98
                                },
                                "pitch" : 0,
                                "style" : 'basic',
                                "zoom" : 8
                            }

                        }
                    }
                )
                ], className= 'seven columns'
                ),

                html.Div([
                dcc.Graph(
                    id='Top-Cities-BarPlot',
                    figure={
                            'data': [
                            {'type' : 'bar',
                             'x': cities_schools['City'][0:5][::-1], 'y': cities_schools['Count'][0:5][::-1], 
                             'text' : bc_calc, 'textposition' : 'auto', 
                             'textfont' : {
                                 'family' : 'Arial, sans-serif', 
                                 'size' : 12, 
                                 'color' : 'black'
                             },
                             'marker' : {
                                 'color' : color10.tolist()
                             }}
                        ],
                        'layout': {
                            'title': 'Top 5 NY Cities with the Most Schools<br>Annotation = Economic Need Index',
                            'margin':{
                                'l' : 75,
                                'r' : 50,
                                'b' : 36,
                                't' : 100,
                                'pad' : 2
                            },
                            'xaxis' : {
                                'title' : 'City',
                                'titlefont' : {
                                    'family' : 'Arial, sans-serif',
                                    'size' : 16,
                                    'color' : 'black'
                                },
                            'showticklabels' : 'True',
                            'tickangle' : 360,
                            'tickfont' : {
                                'family' : 'Arial, sans-serif',
                                'size' : 10,
                                'color' : 'black',
                            },
                            'exponentformat' : 'e',
                            'showexponent' : 'all',
                            },
                            'yaxis' : {
                                'title' : 'Number of Schools',
                                'titlefont' : {
                                    'family' : 'Arial, sans-serif',
                                    'size' : 16,
                                    'color' : 'black',
                                },
                            'showticklabels' : 'True',
                            'tickangle' : 360,
                            'tickfont' : {
                                'family' : 'Arial, sans-serif',
                                'size' : 18,
                                'color' : 'black',
                            },
                            'exponentformat' : 'e',
                            'showexponent' : 'all',
                            },
                            }
                        }
                )
                ], className= 'five columns'
                )
            ], className="row"),
        html.Div([
                dcc.Graph(
                    id='example-graph-3',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Graph 1',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Arial',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Arial',
                                size=20,
                                color='#7f7f7f'
                            ))
                        }
                    }
                )
                ], className= 'five columns',
                ),
                html.Div([
                    dcc.Dropdown(
                        id = 'race-map-dropdown-select',
                        options=[
                            {'label': 'White', 'value': 'White'},
                            {'label': 'Black', 'value': 'Black'},
                            {'label': 'Asian', 'value': 'Asian'},
                            {'label': 'Hispanic', 'value': 'Hispanic'}
                        ],
                        placeholder='Select a race:'
                    ),
                dcc.Graph(
                    id='race-map-2',
                    figure={
                        'data': [
                            {
                              "type": "scattermapbox",
                                "lat": list(df['Latitude']),
                                "lon": list(df['Longitude']),
                                "text": non_encoded['School Name'],
                                "mode": "markers",
                                "name": list(non_encoded['School Name']),
                                "marker": {
                                    "size": df['School Income Estimate']/8000,
                                    "colorscale":"YlGnBu",
                                    "colorbar" : {
                                        "thickness" : 10,
                                        "ticks" : "outside",
                                    },
                                    "opacity": 1,
                                    "color": df['School Income Estimate']  
                                }
                            },
                        ],
                        'layout': {
                            'title': 'Race Distribution of New York: Geospatial Analysis<br>Color = Economic Need Index (ENI). Size = School Estimated Income</br>',
                            "autosize" : True,
                            "hovermode": "closest",
                            "mapbox": {
                                "accesstoken" : mapbox_access_token,
                                "bearing": 0,
                                "center": {
                                    "lat" : 40.70,
                                    "lon" : -73.98
                                },
                                "pitch" : 0,
                                "style" : 'basic',
                                "zoom" : 8
                            }

                        }
                    }
                )
                ], className= 'seven columns'
                )
            ], className="row")
    ], className='ten columns offset-by-one')

'''
# Interactivity Callbacks
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
'''

if __name__ == '__main__':
    app.run_server(debug=True)