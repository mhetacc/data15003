# data15003
Interactive Data Visualization Course, Master in Data Science at University of Helsinki

## Build

Be mindful that, to build the project, paths in `graph_maker.py` needs to be modified (lines #7, #9, #11, #13)

### Requirements

All Python's requirements can be installed by running 

```bash
pip install -r requirements.txt
```

### Run Dash Application

To run the Dash app and see the visualizer it is sufficient to run the script 

```bash
python3 project/graph_maker.py
```

Provided that paths in at lines #7, #9, #11, and #13 get modified e.g.,

```python
countries_temp_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', sep=';')

# change it to
countries_temp_df = pandas.read_csv('YOUR_PATH/project/data/build/countries_temp_all_merged.csv', sep=';')
```