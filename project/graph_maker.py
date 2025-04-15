from dash import Dash, html, dcc, dash_table
import plotly.express
import pandas


countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

app = Dash()

####### political temperature UE map ########

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
    # dash_table.DataTable(data=df_transformed.to_dict('records'), page_size=20),
    # dcc.Graph(figure=bargraph_full),
    # dcc.Graph(figure=bargraph_purged),
    # dcc.Graph(figure=boxplot),
    # dcc.Graph(figure=choropleth_continuous),
    dcc.Graph(figure=choropleth_discrete),
    dash_table.DataTable(
        data=countries_temp_df
        .to_dict('records'))
]

if __name__ == '__main__':
    app.run(debug=True)