## Bootstrap Grid tutorial - adding style to the app

import pandas as pd
import numpy as np

import plotly.graph_objs as go
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html


df = pd.read_csv('Encoded_Data.csv')

app = dash.Dash()

non_encoded = pd.read_csv('2016 School Explorer.csv')

text = [df['School Name'], df['Economic Need Index']]
mapbox_access_token = "pk.eyJ1IjoicGFudDIwMDIiLCJhIjoiY2prenlwb2ZtMHlnMjNxbW1ld3VxYWZ4cCJ9.rOb8DhCzsysBIw69MxyWKg"

app.title = "NY: Educational Infrastructure"

#Data Crap - Viraj
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

cities_schools = cities_schools.sort_values('Count')
cities_schools = cities_schools[::-1]

y10 = np.array([411, 297, 232, 60, 32])
color10 = np.array(['rgb(255,255,255)']*y10.shape[0])
color10[y10 % 411 == 0] = 'rgb(34, 94, 168)'
color10[y10 % 297 == 0 ] = 'rgb(54, 114, 188)'
color10[y10 % 232 == 0] = 'rgb(74, 124, 198)'
color10[y10 % 60 == 0 ] = 'rgb(94, 144, 188)'
color10[y10 % 32 == 0] = 'rgb(114, 164, 208)'

# Correlation Matrix - Aniket (NOT LONNIE)
columns_for_corr = df.columns[5:34]
df_corr = df[columns_for_corr]
df_corr = df.corr()


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
                html.Div(children=[
                        html.Div(
                        children='''
                        ForensX Magic City Hacks: An indepth investigation of the educational infrastructure of New York State.
                        We provide a model for the accurate prediction of the economic need of schools and monitoring of their performance                                                                                                     
                        ''',
                        
                        className='nine columns',
                        ),
                ]),
                

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
                            'height': 700,
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
                ], className= 'seven columns',
                style={'display': 'inline-block', 'width': '49%'}
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
                            'title': 'Top 5 NY Cities with the Most Schools<br>Annotation = Economic Need Index (ENI).</br>',
                            'height': 650,
                            'margin':{
                                'l' : 75,
                                'r' : 50,
                                'b' : 50,
                                't' : 100,
                                'pad' : 4
                            },
                            'xaxis' : {
                                'title' : '',
                                'titlefont' : {
                                    'family' : 'Arial, sans-serif',
                                    'size' : 13,
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
                                'size' : 13,
                                'color' : 'black',
                            },
                            'exponentformat' : 'e',
                            'showexponent' : 'all',
                            },
                            }
                        }
                )
                ], className= 'five columns',
                style={'display': 'inline-block', 'width': '49%'}
                )
            ], className="row"),
        html.Div([
                dcc.Markdown('''

#### Racial Distribution of Students in New York:
###### *Observable in the interactive map to the right, there are clearly observable clusters of racial activity in New York.*
* The majority of the white and asian student population is concentrated in the **southwest** and **Manhattan Area**.
    * Additionally, it can be observed that they frequent schools with **larger estimated incomes**. 
* The majority of the black student population is concentrated in the **Southeast Area**.
    * Additionally, it can be observed that they frequent schools with **lower estimated incomes**. 
* The majority of the hispanic student population is concentrated in the **Northern**.
    * Additionally, it can be observed that they on average, frequent schools with **lower estimated incomes**. 

''')
                ], className= 'five columns',
                style={'display': 'inline-block', 'width': '40%'}
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
                        placeholder='Select a race:',
                        value = 'White'
                    ),
                dcc.Graph(
                    id='race-map-2',
                    style={'display': 'inline-block', 'width': '100%'}
                )
                ], className= 'seven columns',
                )
            ], className="row"),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='correlation-heatmap-1',
                    figure={
                        'data': [
                                go.Heatmap(z=[[1, 20, 30],
                                [20, 1, 60],
                                [30, 60, 1]])
                                ],
                        "layout": go.Layout(
                                title='Title'
                                )
                    }
                )
                ], className= 'six columns',
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-7',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Graph 2'
                        }
                    }
                )
                ], className= 'six columns',
                )
        ]),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph-8',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Mix up the sizings of the columns of the plots',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            ))
                        }
                    }
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-9',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'GET RID OF THIS FOR MARKDOWN AND MAKE NEW ROW'
                        }
                    }
                )
                ], className= 'six columns'
                )
        ]),
    html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph-10',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'KMeans: Elbow Plot',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            ))
                        }
                    }
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-11',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'KMeans: Economic Need Index (ENI) vs. School Estimated Income'
                        }
                    }
                )
                ], className= 'six columns'
                )
        ]),
     html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph-12',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'BLANK: Could be Markdown/Table Overview',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            ))
                        }
                    }
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-13',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 't-SNE: School Clustering and Similarity Studies'
                        }
                    }
                )
                ], className= 'six columns'
                )
        ])
    ], className='ten columns offset-by-one')

# Interactivity Callbacks
@app.callback(
    dash.dependencies.Output('race-map-2', 'figure'),
    [dash.dependencies.Input('race-map-dropdown-select', 'value')])
def update_image_src(selector):
    data = []    
    if 'White' in selector:
        data.append({
            "type": "scattermapbox",
            "lat": df['Latitude'],
            "lon": df['Longitude'],
            "text": non_encoded['School Name'],
            "mode": "markers",
            "name": non_encoded['School Name'],
            "marker": {
                "size": df['School Income Estimate']/8000,
                "colorscale":"YlGnBu",
                "colorbar" : {
                    "thickness" : 10,
                    "ticks" : "outside",
                },
                "opacity": 1,
                "color": df['Percent White']
                }
        })
    elif 'Black' in selector:
        data.append({
            "type": "scattermapbox",
            "lat": df['Latitude'],
            "lon": df['Longitude'],
            "text": non_encoded['School Name'],
            "mode": "markers",
            "name": non_encoded['School Name'],
            "marker": {
                "size": df['School Income Estimate']/8000,
                "colorscale":"YlGnBu",
                "colorbar" : {
                    "thickness" : 10,
                    "ticks" : "outside",
                },
                "opacity": 1,
                "color": df['Percent Black']
                }
        })
    elif 'Asian' in selector:
        data.append({
            "type": "scattermapbox",
            "lat": df['Latitude'],
            "lon": df['Longitude'],
            "text": non_encoded['School Name'],
            "mode": "markers",
            "name": non_encoded['School Name'],
            "marker": {
                "size": df['School Income Estimate']/8000,
                "colorscale":"YlGnBu",
                "colorbar" : {
                    "thickness" : 10,
                    "ticks" : "outside",
                },
                "opacity": 1,
                "color": df['Percent Asian']
                }
        })
    elif 'Hispanic' in selector:
        data.append({
            "type": "scattermapbox",
            "lat": df['Latitude'],
            "lon": df['Longitude'],
            "text": non_encoded['School Name'],
            "mode": "markers",
            "name": non_encoded['School Name'],
            "marker": {
                "size": df['School Income Estimate']/8000,
                "colorscale":"YlGnBu",
                "colorbar" : {
                    "thickness" : 10,
                    "ticks" : "outside",
                },
                "opacity": 1,
                "color": df['Percent Hispanic']
                }
        })
    figure={
        'data': data,
        'layout': {
            'title': 'Race Distribution of New York: Geospatial Analysis<br>Color = Percentage Selected Race. Size = School Estimated Income</br>',
            'height': 450,
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
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)