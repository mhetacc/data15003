from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express
import pandas
import plotly.graph_objects


countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

annual_net_earnings_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_net_earnings.csv', sep=';')

app = Dash()

####### political temperature EU map ########


# create map and set data displayed with outside slider via callback
def make_map(year):
    filtered_df=countries_temp_df[countries_temp_df['YEAR'] == year]

    return plotly.express.choropleth(
        data_frame=filtered_df,
        locations='COUNTRY_NAME',
        locationmode='country names',  
        scope='europe',        
        color='TEMPERATURE',
        color_continuous_scale="RdBu",
        labels={
            'TEMPERATURE':'Temp',
        },
        title='Political temperature per country',
    ).update_layout(
        margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=0,
                    #autoexpand=True
                ),
                #width=1500,
                height=800,
        coloraxis_colorbar=dict(
            title='',
            tickvals=[0, 25, 50, 75, 100],
            ticktext=['Far Left', 'Left', 'Center', 'Right', 'Far Right']
        )
    )



# Place element in the page
app.layout = [
    html.H1(
        children='Political Temperature Throughout the Years', 
        style={'textAlign':'center',
               'fontFamily':'Arial'}),
    dcc.Graph(id='map'),
    dcc.Slider(
        id='year-slider',
        min=countries_temp_df['YEAR'].min(),
        max=countries_temp_df['YEAR'].max(),
        value=countries_temp_df['YEAR'].min(),
        marks={str(year): str(year) for year in countries_temp_df['YEAR'].unique()},    
        step=None
    ),
    dcc.Graph(id='linegraph'),
    dash_table.DataTable(
        data=countries_temp_df
        .to_dict('records'))
]


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
    Input('year-slider', 'value')
)
def update_linegraph(clickData, selected_year):
    if clickData is not None:
        country_clicked = clickData['points'][0]['location']
        line_df=annual_net_earnings_df.loc[annual_net_earnings_df['COUNTRY_NAME'] == country_clicked]

    avg_df = annual_net_earnings_df.loc[annual_net_earnings_df['COUNTRY_NAME'] == 'European Union - 15 countries (1995-2004)']

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
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)