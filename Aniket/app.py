## Bootstrap Grid tutorial - adding style to the app

import pandas as pd
import numpy as np

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go


df = pd.read_csv('Encoded_Data.csv')

app = dash.Dash()

non_encoded = pd.read_csv('2016 School Explorer.csv')

nf = pd.read_csv('nfcsv.csv', encoding = 'utf-8')

k_means_df = pd.read_csv('KMeansLabels.csv')

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
                            'title': 'Top 5 NY Cities with the Most Schools<br>Annotation = Economic Need Index (ENI).</br>',
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
                ], className= 'five columns'
                )
            ], className="row"),
        html.Div([
                dcc.Markdown('''

#### Racial Distribution of Students in New York:
###### *Observable in the interactive map to the right, there are clear *clusters* of racial activity in New York.*
* The majority of the white and asian student population is concentrated in the **southwest** and **Manhattan Area**.
    * Additionally, it can be observed that they frequent schools with **larger estimated incomes**. 
* The majority of the black student population is concentrated in the **Southeast Area**.
    * Additionally, it can be observed that they frequent schools with **lower estimated incomes**. 
* The majority of the hispanic student population is concentrated in the **Northern**.
    * Additionally, it can be observed that they on average, frequent schools with **lower estimated incomes**. 

''')
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
                        placeholder='Select a race:',
                        value = 'White'
                    ),
                dcc.Graph(
                    id='race-map-2',
                )
                ], className= 'seven columns'
                )
            ], className="row"),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='correlation-heatmap-1',
                    figure={
                        'data': [
                            go.Heatmap(z=np.array(df.corr()),
                            x = df.columns,
                            y = df.columns[::-1])
                        ],
                        'layout': {
                            'title':'Correlation Heatmap of All Studied Variables',
                            'tickfont':{
                                'size':7
                            }
                        }
                    }
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='eni-vs-chronic-absence',
                    figure={
                    'data': [
                        go.Scatter(
                            x=nf['Economic Need Index'],
                            y=nf['Average Grades'],
                            text=df['School Name'],
                            mode='markers',
                            opacity=1.0,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'},
                                "colorscale":"YlGnBu",
                                "colorbar" : {
                                    "thickness" : 10
                                },
                                'color': nf['School Income Estimate'],
                            },
        )], 'layout': go.Layout(
        title= "Economic Need Index vs. Average Grades.<br>Color = School Income Estimate.",
        xaxis={'title': 'Economic Need Index'},
        yaxis={'title': 'Average Grades (GPA)'},
        hovermode='closest'
    )},   
                )
                ], className= 'six columns'
                )
        ]),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph-8',
                    figure={
    'data': [
          {
             'x': nf["Economic Need Index"], 
            'y': nf["Percent of Students Chronically Absent"]*100, 
            'text': nf["School Name"], 
            'mode': 'markers', 
            'name': 'Trust'},

    ],
    'layout': {
        'title':'Economic Need Index vs Chronic Absences',
        'xaxis': {'title': 'Economic Need Index (ENI)'},
        'yaxis': {'title': "Chronic Absence Percentage"},
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
  		{
  			'x': nf["Percent Black"], 
        	'y': nf["Percent of Students Chronically Absent"]*100, 
        	'text': nf["School Name"], 
        	'mode': 'markers', 
        	'name': 'Black'},
  		{
  			'x': nf["Percent Hispanic"], 
        	'y': nf["Percent of Students Chronically Absent"]*100, 
        	'text': nf["School Name"], 
        	'mode': 'markers', 
        	'name': 'Hispanic'},
  		{
  			'x': nf["Percent White"], 
        	'y': nf["Percent of Students Chronically Absent"]*100, 
        	'text': nf["School Name"], 
        	'mode': 'markers', 
        	'name': 'White'},
  		{
  			'x': nf["Percent Asian"], 
        	'y': nf["Percent of Students Chronically Absent"]*100, 
        	'text': nf["School Name"], 
        	'mode': 'markers', 
        	'name': 'Asian'},
    ],
    'layout': {
        'title':'Distribution of Race vs. Chronic Absence',
        'xaxis': {'title': 'Percent Race'},
        'yaxis': {'title': "Chronic Absences"}
    }
}
                )
                ], className= 'six columns'
                )
        ]),
    html.Div([
            html.Div([
                dcc.Graph(
                    id='k_means-elbow-plot',
                    figure={
                        'data': [
                            {'x': list(range(1,10)), 'y': [397917909644.87122, 169929639284.22815, 87832269638.271652, 49611051065.437546, 34825937172.590172, 25049172542.533951, 15802640302.250399, 12389934516.879337, 9845184947.2853928, 7829834480.651763], 'type': 'line', 'name': 'Variance'},
                        ],
                        'layout': {
                            'title': 'KMeans: Elbow Plot',
                            'xaxis' : dict(
                                title='Clusters',
                                titlefont=dict(
                                family='Arial',
                                size=15,
                                color='#000000'
                            )),
                            'yaxis' : dict(
                                title='Variance',
                                titlefont=dict(
                                family='Arial',
                                size=15,
                                color='#000000'
                            ))
                        }
                    }
                )
                ], className= 'five columns'
                ),

                html.Div([
                dcc.Graph(
                    id='kMeans-geospatial-11',
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
                                        'ticktext': ['1 Percentile', '25 Percentile', "50 Percentile", "75 Percentile", '99 Percentile']
                                    },
                                    "opacity": 1,
                                    "color": k_means_df['KMeans Labels']  
                                }
                            },
                        ],
                        'layout': {
                            'title': 'KMeans: Geospatial Analysis<br>Color = Learned KMeans Labels. Size = School Estimated Income.</br>',
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
        ]),
     html.Div([
            html.Div([
                dcc.Graph(
                    id='bar-graph-of-kmeans-distribution',
                    figure={
                        "data": [
                            go.Bar(
                                x = k_means_df['KMeans Labels'].value_counts().index,
                                y = k_means_df['KMeans Labels'].value_counts()
                            )
                        ],
                        'layout': go.Layout(
                            title = "KMeans Learned Labels:<br>Distribution of NY Educational Infrastructure</br>",
                            xaxis = {
                                'title':'Cluster/Economic Need'
                            },
                            yaxis = {
                                'title':'Amount of Schools'
                            }
                        )
                    }
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='kmeans-categorical',
                    figure={
                        'data': [
                            go.Scatter(
                                x=df['Economic Need Index'],
                                y=df['School Income Estimate'],
                                text=df['School Name'],
                                mode='markers',
                                opacity=1.0,
                                marker={
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': 'white'},
                                    "colorscale":"YlGnBu",
                                    "colorbar" : {
                                        "thickness" : 10,
                                        'tickvals': list(range(1,6))
                                    },
                                    'color': k_means_df['KMeans Labels'],
                                    
                                },
                            )
                        ],
                        'layout': go.Layout(
                            title= "KMeans: Economic Need Index vs. School Income Estimate",
                            xaxis={'title': 'Economic Need Index'},
                            yaxis={'title': 'School Income Estimate'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
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