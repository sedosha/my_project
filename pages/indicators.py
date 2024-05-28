from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

all_cont = df['continent'].unique()

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H1("Статистика"),
                html.P(" Используйте фильтры, чтобы увидеть результат."),
                html.Hr(style={'color':'black'}),
            ], style={'textAlign':'center'})
        )
    ]),

    html.Br(),
    
        dbc.Row([ 
            dbc.Col([
                html.P("Выберите период:")],width=2),
            dbc.Col([
                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[df['Year'].min(), df['Year'].max()],
                    marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1)},
                ),
            ], width=9),
    ]),
   html.Br(),

     dbc.Row ([
        dbc.Col([
            html.P("Выберите континент:")
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-cont',
                # заполняем дропдаун уникальными значениями континентоы из датасета
                options = [{'label': i, 'value': i} for i in all_cont],
                # значение континента, выбранное по умолчанию
                value = all_cont[0],
                # возможность множественного выбора
                multi = False
            )
        ],width=3),
    ]),



    html.Br(),
    
        dbc.Row([
            dbc.Col([
                dbc.Label("Выберите показатель:"),
                dbc.RadioItems(
                    options=[
                        {'label': 'Продолжительность жизни', 'value': 'Life expectancy'},
                        {'label': 'Население', 'value': 'Population'},
                        {'label': 'ВВП', 'value': 'GDP'},
                        {'label': 'Школьное образование', 'value': 'Schooling'},
                    ],
                    value='GDP',
                    id='indicator-radio',
                ),
            ], width=3),
            dbc.Col([
                dcc.Graph(id='indicator-graph', config={'displayModeBar': False}),
            ], width=9),
            dbc.Col([
                dcc.Graph(id='bar-graph', config={'displayModeBar': False}),  # Add bar chart here
            ], width=12),
        ])])
   
@callback(
    [Output('indicator-graph', 'figure'),
     Output('bar-graph', 'figure')],  # Change to list of outputs
    [
        Input('crossfilter-cont', 'value'),
        Input('year-slider', 'value'),
        Input('indicator-radio', 'value'),
    ])

def update_graph(selected_continents, selected_years, selected_indicator):
    if isinstance(selected_continents, str):
        selected_continents = [selected_continents]
    
    filtered_df = df[(df['continent'].isin(selected_continents)) &
                     (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    line_fig = px.line(filtered_df, x='Year', y=selected_indicator, color='Country',
                       labels={'Year': 'Год', selected_indicator: selected_indicator},
                       title=f'Динамика по странам')
    
    line_fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 20})
    
    bar_fig = px.bar(filtered_df, x='Country', y=selected_indicator, color='Country',
                     labels={'Country': 'Страна', selected_indicator: selected_indicator},
                     title=f'Столбчатая диаграмма')
    
    bar_fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 20})
    
    return line_fig, bar_fig  # Return both figures