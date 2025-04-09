## Dataset

### Build Political Dataset

1. merge `parties.csv` and `country_codes.csv` on `DIVISION_ID = alpha-2`
   1. thus obtain table with parties and respective country name
2. merge new `parties.csv` with each `result-parties-country.csv` on `ID = PARTY_ID`
   1. thus obtain table with name of parties and percentage 
3. add to all data `year` column

After this we should have a table with all parties names, countries and year of election.

### Country Codes

I need the `alpha-2` column for each country.

### Poverty Risk

Changed dataset with: [Persistent at-risk-of-poverty rate by sex and age](https://ec.europa.eu/eurostat/databrowser/view/ilc_li21/default/bar?lang=en&category=livcon.ilc.ilc_ip.ilc_li)

