from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express
import pandas


countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

annual_net_earnings_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_net_earnings.csv', sep=';')

app = Dash()

####### political temperature EU map ########

choropleth_discrete = plotly.express.choropleth(
    data_frame=countries_temp_df,
    locations='COUNTRY_NAME',
    locationmode='country names',  
    scope='europe',        
    color='TEMPERATURE',
    color_continuous_scale="RdBu",
    animation_frame='YEAR',
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
    dcc.Graph(id='map',figure=choropleth_discrete),
    dcc.Graph(id='linegraph'),
    dash_table.DataTable(
        data=countries_temp_df
        .to_dict('records'))
]


# Callback to update the line graph based on the map click
@app.callback(
    Output('linegraph', 'figure'),
    Input('map', 'clickData')
)
def update_linegraph(clickData):
    if clickData is None:
        country_clicked = 'European Union - 15 countries (1995-2004)'
    else:
        country_clicked = clickData['points'][0]['location']
    
    line_df=annual_net_earnings_df.loc[annual_net_earnings_df['COUNTRY_NAME'] == country_clicked]



    fig = plotly.express.line(
        data_frame=line_df,
        x='YEAR',
        y='NET_EARNINGS',
        title=f'Net Earnings: {country_clicked}',
        markers=True,
        labels={
            'NET_EARNINGS':'Euro',
            'YEAR':'Year'
        },
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)