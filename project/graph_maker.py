from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express
import pandas
import plotly.graph_objects


countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

annual_net_earnings_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_net_earnings.csv', sep=';')

annual_immigration_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_immigration.csv', sep=';')

annual_poverty_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_poverty.csv', sep=';')

linegraph_datasets = {
    'Net Earnings': annual_net_earnings_df,
    'Immigration': annual_immigration_df,
    'Poverty Risk': annual_poverty_df
}

app = Dash()

####### political temperature EU map ########


# create map and set data displayed with outside slider via callback
def make_map(year):
    filtered_df=countries_temp_df[countries_temp_df['YEAR'] == year]

    map = plotly.express.choropleth(
        data_frame=filtered_df,
        locations='COUNTRY_NAME',
        locationmode='country names',  
        scope='europe',        
        color='TEMPERATURE',
        hover_name='COUNTRY_NAME',
        hover_data={'COUNTRY_NAME': False, 'TEMPERATURE': False, 'YEAR': False},  # hide some fields
        color_continuous_scale="RdBu",
        labels={
            'TEMPERATURE':'Temp',
        },
        title='Political temperature per country',
    )



    map.update_layout(
        autosize=True,
        margin = dict(l=0,r=0,b=0,t=0),
        #width=1500,
        #height=800,
        coloraxis_colorbar=dict(
            title='',
            tickvals=[0, 25, 50, 75, 100],
            ticktext=['Far Left', 'Left', 'Center', 'Right', 'Far Right']
        )
    )

    return map



# Place element in the page
app.layout = html.Div([
    html.H1(
        children='Political Temperature Throughout the Years', 
        style={
            'textAlign':'center',
            'fontFamily':'Arial',
            'marginBottom':'0px',
            'marginTop':'0px',
        }
    ),
    html.P(
        children='Move the years slider and click on a country to see different data',
        style={
            'textAlign':'center',
            'fontFamily':'Arial',
            'marginTop':'0px',
        }
    ),
    html.Div([
        dcc.Graph(
            id='map', 
            style={'height':'100%', 'width':'100%'},
            config={'responsive': True}
            )
    ], style={'height':'40vh'}),
    html.Div([
        dcc.Slider(
            id='year-slider',
            min=countries_temp_df['YEAR'].min(),
            max=countries_temp_df['YEAR'].max(),
            value=2019,  # default value
            marks={str(year): str(year) for year in countries_temp_df['YEAR'].unique()},    
            step=None, 
            )
    ], style={'height':'4vh'}),
    html.Div([
        dcc.RadioItems(
            id='linegraph_selector',
            options=[{'label': name, 'value': name} for name in linegraph_datasets.keys()],
            value='Net Earnings',  # default selection
             labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        ),
    ], style={'height':'2.15vh'}),
    html.Div([
        dcc.Graph(id='linegraph')
    ], style={'height':'45vh'})
])


# Callback to update the map based on the slider
@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(year):
    return make_map(year)


# Callback to update the line graph based on the map click
@app.callback(
    Output('linegraph', 'figure'),
    Input('map', 'clickData'),
    Input('year-slider', 'value'),
    Input('linegraph_selector', 'value')
)
def update_linegraph(clickData, selected_year, selected_dataset):
    dataset = linegraph_datasets[selected_dataset]

    if selected_dataset == 'Net Earnings':

        if clickData is not None:
            country_clicked = clickData['points'][0]['location']
            line_df=dataset.loc[dataset['COUNTRY_NAME'] == country_clicked]

        avg_df = dataset.loc[dataset['COUNTRY_NAME'] == 'European Union - 15 countries (1995-2004)']

        fig = plotly.graph_objects.Figure()

        # dynamic line
        if clickData is not None and not line_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=line_df['YEAR'],
                    y=line_df['NET_EARNINGS'],
                    mode='lines+markers',
                    name=country_clicked,
                    marker=dict(color='blue'),
                )
            )

        # average line
        if not avg_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=avg_df['YEAR'],
                    y=avg_df['NET_EARNINGS'],
                    mode='lines+markers',
                    name='EU Average',
                    marker=dict(color='red'),
                )
            )

        # add year vertical line
        fig.add_shape(
            type='line',
            x0=selected_year,
            y0=0,
            x1=selected_year,
            y1=1,
            yref='paper',
            line=dict(color='black', width=2, dash='dash'),
            name='Selected Year'
        )

        fig.update_layout(
            title='Income over time',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Income in Euro', range=[0, 40000]),
            margin=dict(t=60) 
        )

    elif selected_dataset == 'Immigration':
        
        if clickData is not None:
            country_clicked = clickData['points'][0]['location']
            line_df=dataset.loc[dataset['COUNTRY_NAME'] == country_clicked]

        avg_df = dataset.loc[dataset['COUNTRY_NAME'] == 'Europe Average']

        fig = plotly.graph_objects.Figure()

        # dynamic line
        if clickData is not None and not line_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=line_df['YEAR'],
                    y=line_df['IMMIGRATION'],
                    mode='lines+markers',
                    name=country_clicked,
                    marker=dict(color='blue'),
                )
            )

        # average line
        if not avg_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=avg_df['YEAR'],
                    y=avg_df['IMMIGRATION'],
                    mode='lines+markers',
                    name='EU Average',
                    marker=dict(color='red'),
                )
            )

        # add year vertical line
        fig.add_shape(
            type='line',
            x0=selected_year,
            y0=0,
            x1=selected_year,
            y1=1,
            yref='paper',
            line=dict(color='black', width=2, dash='dash'),
            name='Selected Year'
        )

        fig.update_layout(
            title='Immigration over time',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Immigration'),
            margin=dict(t=60)
        )

    elif selected_dataset == 'Poverty Risk':
        if clickData is not None:
            country_clicked = clickData['points'][0]['location']
            line_df=dataset.loc[dataset['COUNTRY_NAME'] == country_clicked]

        avg_df = dataset.loc[dataset['COUNTRY_NAME'] == 'Europe Average']

        fig = plotly.graph_objects.Figure()

        # dynamic line
        if clickData is not None and not line_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=line_df['YEAR'],
                    y=line_df['POVERTY_RISK'],
                    mode='lines+markers',
                    name=country_clicked,
                    marker=dict(color='blue'),
                )
            )

        # average line
        if not avg_df.empty:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=avg_df['YEAR'],
                    y=avg_df['POVERTY_RISK'],
                    mode='lines+markers',
                    name='EU Average',
                    marker=dict(color='red'),
                )
            )

        # add year vertical line
        fig.add_shape(
            type='line',
            x0=selected_year,
            y0=0,
            x1=selected_year,
            y1=1,
            yref='paper',
            line=dict(color='black', width=2, dash='dash'),
            name='Selected Year'
        )

        fig.update_layout(
            title='Poverty risk over time',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Poverty risk %', range=[0, 13]),
            margin=dict(t=60)
        )

    return fig

if __name__ == '__main__':
    app.run(debug=True)