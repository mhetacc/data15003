from dash import Dash, html, dcc, dash_table
import plotly.express
import pandas

dataframe = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/ii_second_assignment/USA_school_census.csv')
dataframe['expected_age'] = dataframe['ClassGrade'] + 5
dataframe['age_offset'] = dataframe['Ageyears'] - dataframe['expected_age']

df_transformed = dataframe[['age_offset', 'Ageyears', 'Gender']]

print(df_transformed)

app = Dash()


bargraph_full = plotly.express.bar(
    df_transformed,
    x = 'Ageyears',
    y = 'age_offset',
    color = 'Gender',
    barmode = 'group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age',
        'Gender':'Gender'
    },
    title='Stacked grade retentions over gender and age, full data'
)

bargraph_purged = plotly.express.bar(
    df_transformed.query('Ageyears <= 20'),
    x = 'Ageyears',
    y = 'age_offset',
    color = 'Gender',
    barmode = 'group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age',
        'Gender':'Gender'
    },
    title='Stacked grade retentions over gender and age, purged'
)


# TODO median offset graph needs much smaller coso or
# different graph like the bar thingy one
median_offsets = df_transformed.query('Ageyears <= 20').groupby(['Ageyears', 'Gender'])['age_offset'].transform('median')

df_transformed['median_offset'] = median_offsets

bargraph_purged_median = plotly.express.bar(
    df_transformed.query('Ageyears <= 20'),
    x = 'Ageyears',
    y = 'median_offset',
    color = 'Gender',
    barmode = 'group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age',
        'Gender':'Gender'
    },
    title='Median grade retentions over gender and age, purged'
)

# BOX PLOT WIP

boxplot = plotly.express.box(
    df_transformed.query('Ageyears <= 20'),
    x= 'Ageyears',
    y = 'age_offset',
    color = 'Gender',
    #TODO
)

app.layout = [
    html.H1(
        children='Grade retentions over gender and age', 
        style={'textAlign':'center',
               'fontFamily':'Arial'}),
    # dash_table.DataTable(data=df_transformed.to_dict('records'), page_size=20),
    dcc.Graph(figure=bargraph_full),
    dcc.Graph(figure=bargraph_purged),
    dcc.Graph(figure=boxplot) # it works but after 17 not so much
]

if __name__ == '__main__':
    app.run(debug=True)