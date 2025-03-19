from dash import Dash, html, dcc, dash_table
import plotly.express
import pandas

"""
Grade retentions over gender and age, where age = [10, 18] years old.
Graphs are as follows: first two shows all held back (or advanced) years stacked on top of each other, while the last graph is a box graph that shows the median over the years (hence it is the "correct" one).
Only the first graph uses data from all ages, meaning we can see students that are 34 or 63 years old.

Data taken from: https://docs.google.com/spreadsheets/d/1S6Dgsh_S2ghVo7hSoJ2aD25FjLSXSQMkI_McGE88dCY/edit?usp=sharing 
"""

# Read data, add the expected grade, add the age offset for each row
dataframe = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/ii_second_assignment/USA_school_census.csv')
dataframe['expected_age'] = dataframe['ClassGrade'] + 5
dataframe['age_offset'] = dataframe['Ageyears'] - dataframe['expected_age']

# Create dataframe with only useful data
df_transformed = dataframe[['age_offset', 'Ageyears', 'Gender']]

#print(df_transformed)

app = Dash()


bargraph_full = plotly.express.bar(
    df_transformed,
    x = 'Ageyears',
    y = 'age_offset',
    color = 'Gender',
    barmode = 'group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age'
    },
    title='Stacked grade retentions over gender and age, full data'
)


# purged data i.e., only student between 10 and 20 years old
bargraph_purged = plotly.express.bar(
    df_transformed.query('Ageyears <= 20'),
    x = 'Ageyears',
    y = 'age_offset',
    color = 'Gender',
    barmode = 'group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age'
    },
    title='Stacked grade retentions over gender and age, purged data'
)


# purged data i.e., only student between 10 and 20 years old
boxplot = plotly.express.box(
    df_transformed.query('Ageyears <= 20'),
    x = 'Ageyears',
    y = 'age_offset',
    #points='all',
    color = 'Gender',
    boxmode='group',
    labels={
        'age_offset':'Years held back (ord advanced)',
        'Ageyears':'Age'
    },
    title='Boxplot grade retentions over gender and age, purged data'
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
    dcc.Graph(figure=boxplot),
    dash_table.DataTable(
        data=df_transformed
        .query('Ageyears <= 20')
        .sort_values(by='Ageyears')
        .to_dict('records'))
]

if __name__ == '__main__':
    app.run(debug=True)