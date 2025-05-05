## Visualizer

Highlighting clicked country functionality was not implemented since it requires an update of the map every time, which resets the zoom and makes using it very annoying. 

Dropdown menu was changed into an Radioitem menu to make it clear for the user which options are present, and it was put in line to occupy less space.

Stylizing the slider was not implemented since it would require external CSS tools, but the default value was changed to 2019 to make self evident the fact that it is a year-slider.

All elements have been wrapped into an html.Div([]) to better position them vertically in the page, now no scroll is required to see all tools which make it way clearer. 


I would have liked to add an annotation in the choropleth to instruct the user to click a country (e.g., "Click any country to see specific country-related data") that would then disappear after any click. Unfortunately its the same problem as highlighting: zoom level reset since map updates. 

```python
@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value'),
    Input('map', 'clickData')
)
def update_map(year, clickData):
    return make_map(year, clickData)
```

## Dataset

### Problems

#### Data before 2004

Unfortunately data before 2004 is not usable, since there is no way to get votes for the single state and also merging parties with the general result is not possible since we miss the `ACRONYM` field in the single state results, which only report the whole group result.\
Moreover, the percentages relate to the whole assembly seats, not the in-state vote, meaning we cannot use it to gauge party's popularity in their respective state.


This can be seen, for example, at [italian results csv](https://github.com/mhetacc/data15003/blob/main/project/data/eu_parliament/2004/results-parties-it.csv): there is no single party code.

The most we could know is that *party X*, e.g., `IT01`, which may be `FI` as in `Forza Italia` got 22 seats in the parliament. Unfortunately

**Solution:**

We will need to calculate votes percentage based in the seats assigned to the whole country and the seats assigned to each single party, e.g.,
- PARTY1 10 seats
- PARTY2 5  seats
- total 100% = 15 seats 
- so parties are like 75% and 25%
 
#### Temperature grading

Since the objective is the visualization first and foremost i tried, and i could have done it, to let gpt do the grading. Unfortunately i would need to have GPT4 premium to actually complete the whole thing, here follows the link to the chat: [gpt chat - grading political temperature](https://chatgpt.com/share/67fd142c-cdc4-800b-99f6-71a2ebfa03fe). 

Two things to notice:
1. doing it by hand would require an inordinate amount of time
2. in the chat we see parties taken from datasets from 2024, so the total quantity is even bigger

I could do it with microsoft copilot with the university account but i need to manually divide the list of parties since it exceed greatly the max number of characters allowed, as it can be seen at the [prompt link](https://www.microsoft365.com/chat/entity1-d870f6cd-4aa5-4d42-9626-ab690c041429/eyJpZCI6IlZYTmxjbFl4ZkdoMGRIQnpPaTh2YzNWaWMzUnlZWFJsTFdsdWRDNXZabVpwWTJVdVkyOXRMM3hQU1VRNk0yRmpaamsyT1RrdE5EQTFOQzAwWkRCbUxUZzNOVFV0T0dOa01EUXhOVFkwTUdNeWZHUTFOelEwT1daa0xUTTBOVEl0TkRVeE1DMWhNREk1TFdJME16QTBZVEU0TVRneE5ud3lNREkxTFRBMExURTBWREUwT2pFeE9qVXlMakUzTWpReE5qZGEiLCJzY2VuYXJpbyI6InNoYXJlTGluayIsInByb3BlcnRpZXMiOnsicHJvbXB0U291cmNlIjoidXNlciIsImNsaWNrVGltZXN0YW1wIjoiMjAyNS0wNC0xNFQxNDoxMTo1Mi4zMjZaIn0sImNoYXRUeXBlIjoid2ViIiwidmVyc2lvbiI6MS4xfQ)

For these reasons, i decided for now to assign a random grading to the various parties just for demonstration purposes. If time allows it i will try to get the full result from AIs.

### Build Political Dataset

1. merge `parties.csv` and `country_codes.csv` on `DIVISION_ID = alpha-2`
   1. thus obtain table with parties and respective country name
2. merge new `parties.csv` with each `result-parties-country.csv` on `ID = PARTY_ID`
   1. thus obtain table with name of parties and percentage 

After this we should have a table with all parties names, countries and year of election.

#### For 2004 and 1999

- calculate for each `results-parties*` percentage of votes based on seats taken
- procede as before
- add the `year` column since it is not present

### Country Codes

I need the `alpha-2` column for each country.

### Poverty Risk

Changed dataset with: [Persistent at-risk-of-poverty rate by sex and age](https://ec.europa.eu/eurostat/databrowser/view/ilc_li21/default/bar?lang=en&category=livcon.ilc.ilc_ip.ilc_li)

### Net Earnings

Many different options to choose from, taken the following:
- estruct: Net earning
- ecase: Single person without children earning 100% of the average earning
- currency: Euro

### Immigration

Did not lock the scale of the line graph otherwise some values would not have been readable, since some countries need a scale between [0, 2M] and some between [0, 200k]. The EU average is present to give the user a sense of scale and difference.  

