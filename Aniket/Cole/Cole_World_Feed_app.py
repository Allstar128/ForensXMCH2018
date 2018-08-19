# this is a dash app to display which countries eat a certain type of food
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# get the entire dataframe
df = pd.read_csv('FAO.csv', encoding='latin1')
item = "Wheat and products"
year = "2013"

app = dash.Dash()


#do app stuff
app.layout = html.Div(children=[
    
    html.H1(children='Food Production'),
    html.Div(children='''
        The following graph shows the food production of
        the selected food over the year 2013 
    '''),
    html.P(),
    html.Label('Food Type:'),
    dcc.Dropdown(
        id='selectDropDown',
        value = "Wheat and products",
        options = [
            {'label': 'Wheat and products',             'value': 'Wheat and products'},
            {'label': 'Rice (Milled Equivalent)',       'value': 'Rice (Milled Equivalent)'},
            {'label': 'Barley and products',            'value': 'Barley and products'},
            {'label': 'Maize and products',             'value': 'Maize and products'},
            {'label': 'Millet and products',            'value': 'Millet and products'},
            {'label': 'Cereals, Other',                 'value': 'Cereals, Other'},
            {'label': 'Potatoes and products',          'value': 'Potatoes and products'},
            {'label': 'Sugar (Raw Equivalent)',         'value': 'Sugar (Raw Equivalent)'},
            {'label': '	Sweeteners, Other',             'value': '	Sweeteners, Other'},
            {'label': 'Honey',                          'value': 'Honey'},
            {'label': 'Pulses, Other and products',     'value': 'Pulses, Other and products'},
            {'label': 'Nuts and products',              'value': 'Nuts and products'},
            {'label': 'Coconuts - Incl Copra',          'value': 'Coconuts - Incl Copra'},
            {'label': 'Sesame seed',                    'value': 'Sesame seed'},
            {'label': 'Olives (including preserved)',   'value': 'Olives (including preserved)'},
            {'label': 'Soyabean Oil',                   'value': 'Soyabean Oil'},
            {'label': 'Groundnut Oil',                  'value': 'Groundnut Oil'},
        ],
    ),               
    dcc.Graph( id='foodGraph' ) 
    
]) #end layout

@app.callback(
        dash.dependencies.Output('foodGraph', 'figure'),
        [dash.dependencies.Input('selectDropDown', 'value')]
        )
def update_figure(food):
    dfCopy = df[df.Item == food]
    dfCopy = dfCopy[dfCopy["Element"] == 'Food']
    return {
            'data': [dict (
                type = 'choropleth',
                locations = dfCopy['Area Abbreviation'],
                z = dfCopy['Y' + year],
                text = dfCopy['Area'],
                colorscale = 'Rainbow',
                autocolorscale = False,
                reversescale = True,
                marker = dict(
                    line = dict(
                        color = 'rgb(180,180,180)',
                        width = 0.5
                    )),
                colorbar = dict(
                    autotick = False,
                    tickprefix = '',
                    title = 'Production per<br>1000 tonnes'),
                
                ) ],
            'layout': dict(
                title = 'Showing: ' + item,
                geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection = dict(
                        type = 'Mercator'
                    )
                )
            )
            }
if __name__ == '__main__':
    app.run_server(debug=True)