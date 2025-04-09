## Dataset

### Problems

Unfortunately data before 2004 is not usable, since there is no way to get votes for the single state and also merging parties with the general result is not possible since we miss the `ACRONYM` field in the single state results, which only report the whole group result.\
Moreover, the percentages relate to the whole assembly seats, not the in-state vote, meaning we cannot use it to gauge party's popularity in their respective state.


This can be seen, for example, at [italian results csv](https://github.com/mhetacc/data15003/blob/main/project/data/eu_parliament/2004/results-parties-it.csv): there is no single party code.

The most we could know is that *party X*, e.g., `IT01`, which may be `FI` as in `Forza Italia` got 22 seats in the parliament. Unfortunately

We will need to calculate it based in the seats assigned to the whole country and the seats assigned to each single party.

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

