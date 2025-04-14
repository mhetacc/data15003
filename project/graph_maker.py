from dash import Dash, html, dcc, dash_table
import plotly.express
import pandas


countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

app = Dash()

####### discrete colors usa map ########

choropleth_discrete = plotly.express.choropleth(
    data_frame=countries_temp_df
    locations='COUNTRY_CODE',
    locationmode='USA-states',  #TODO
    scope='usa',                #TODO
    color='TEMPERATURE',
    #color_discrete_map=color_scale,
    labels={
        'TEMPERATURE',:'Political Temperature',
    },
    title='Political temperature per country',
    #category_orders={"TEMPERATURE',": [-1, 0, 1, 2]}
).update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}
)


# Place element in the page
app.layout = [
    html.H1(
        children='Grade retentions over gender, age and states', 
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
        .query('Ageyears <= 20')
        .sort_values(by='Ageyears')
        .to_dict('records'))
]

if __name__ == '__main__':
    app.run(debug=True)