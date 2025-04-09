import pandas 
import glob


def merge_parties_countries_votepercentage(year):
        # Read csv files, separating by `;`
    parties = pandas.read_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/eu_parliament/{year}/parties.csv', sep=';')
    country_codes = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/country_codes.csv', sep=';')

    # Merge `parties.csv` and `country_codes.csv` on `DIVISION_ID = alpha-2`
    # Make one dataframe with all parties and their country names 
    parties_with_countries = pandas.merge(parties, country_codes, left_on='DIVISION_ID', right_on='alpha-2', how='left')

    # save to csv for debugging
    parties_with_countries.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/parties_with_countries_{year}.csv', index=False)


    # Merge all national parties results results in one csv
    # Get all files with results for each country
    list_of_parties = glob.glob(f'/home/mhetac/Documents/GitHub/data15003/project/data/eu_parliament/{year}/results-parties*.csv', recursive=True)

    # Read and store each file into a list of DataFrames
    parties_df = [pandas.read_csv(party, sep=';') for party in list_of_parties]

    # Concatenate them into a single DataFrame
    all_parties_merged = pandas.concat(parties_df, ignore_index=True)

    # save to csv for debugging
    all_parties_merged.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/all_parties_merged_{year}.csv', index=False, sep=';')


    # Merge parties with election results 
    # with parties with countries
    parties_countries_percentage = pandas.merge(parties_with_countries, all_parties_merged, left_on='ID', right_on='PARTY_ID', how='left')

    # save to csv for debugging
    parties_countries_percentage.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/parties_countries_percentage_{year}.csv', index=False, sep=';')

merge_parties_countries_votepercentage(2024)


# 2004, 1999 do not have usable data
# merge_parties_countries_votepercentage(1999)

