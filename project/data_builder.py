import pandas 
import glob
import numpy 
from sklearn.preprocessing import MinMaxScaler

def build_data(year, transformed=False):
    """
    Merge parties with country names and votes percentage for the given year.
    If transformed=True it will look into 2004 and 1999 folders for the transformed party election results.
    Then it will assign a random temperature to each party and compute the weighted average temperature per country.
    Finally, it will do some other stuff to get the final dataframe, which looks like this (temperature normalized to [0,100]): COUNTRY_CODE;YEAR;TEMPERATURE;COUNTRY_NAME
    """

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
    parties_merged = pandas.concat(parties_df, ignore_index=True)

    # save to csv for debugging
    parties_merged.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/parties_merged_{year}.csv', index=False, sep=';')


    # Merge parties with election results 
    # with parties with countries
    parties_countries_percentage = pandas.merge(parties_with_countries, parties_merged, left_on='ID', right_on='PARTY_ID', how='left')

    # add random political temperature to each one
    parties_countries_percentage['TEMPERATURE'] = numpy.random.uniform(-2, 2, size=len(parties_countries_percentage))

    # drop useless rows
    parties_countries_percentage.dropna(subset=['VOTES_PERCENT'], inplace=True)

    # compute weighted temperature
    parties_countries_percentage['WEIGHTED_TEMP'] = parties_countries_percentage['VOTES_PERCENT'] * parties_countries_percentage['TEMPERATURE']

    # calculate total weighted temperature and total votes per country
    weighted_sums = parties_countries_percentage.groupby('alpha-2')['WEIGHTED_TEMP'].sum()
    votes_sums = parties_countries_percentage.groupby('alpha-2')['VOTES_PERCENT'].sum()

    # compute the weighted average temperature per country
    country_temps = (weighted_sums / votes_sums).reset_index(name='TEMPERATURE')

    # add year 
    country_temps['YEAR'] = year

    # normalize to [0, 100]
    scaler = MinMaxScaler(feature_range=(0, 100))
    country_temps['TEMP_NORMALIZED'] = scaler.fit_transform(country_temps[['TEMPERATURE']])

    # add country names
    name_map = parties_countries_percentage.groupby('alpha-2')['name'].first()
    country_temps['COUNTRY_NAME'] = country_temps['alpha-2'].map(name_map)

    # drop and rename columns
    country_temps.rename(columns={'alpha-2': 'COUNTRY_CODE'}, inplace=True) 
    country_temps.drop(columns=['TEMPERATURE'], inplace=True)
    country_temps.rename(columns={'TEMP_NORMALIZED': 'TEMPERATURE'}, inplace=True) 
    # reorder columns
    country_temps = country_temps[['COUNTRY_CODE', 'COUNTRY_NAME', 'YEAR', 'TEMPERATURE']]



    # save to csv for debugging
    country_temps.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/country_temps_{year}.csv', index=False, sep=';')

    # save to csv for debugging
    parties_countries_percentage.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/parties_countries_percentage_{year}.csv', index=False, sep=';')


    



    ##  # OSS: none of this is needed since we are not using AIs to do a correct grading
    ##  # Get a list of all parties, save it to dataframe
    ##  # Get unique, non-null LABEL values
    ##  list_of_parties = parties_countries_percentage['LABEL'].dropna().unique()
  
    ##  # Convert to a DataFrame
    ##  list_of_parties_df = pandas.DataFrame(list_of_parties, columns=['LABEL'])
  
    ##  # add random political temperature to each one
    ##  list_of_parties_df['TEMPERATURE'] = numpy.random.uniform(-2, 2, size=len(list_of_parties_df))
  
    ##  # Save to CSV
    ##  list_of_parties_df.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/list_of_parties_{year}.csv', index=False, sep=';')
def merge_all():
    """
    Merge all data from all years into one dataframe
    """


    # Get all files with results for each country
    countries_temp = glob.glob('/home/mhetac/Documents/GitHub/data15003/project/data/build/country_temps_*.csv', recursive=True)

    # Read and store each file into a list of DataFrames
    countries_merged = [pandas.read_csv(country, sep=';') for country in countries_temp]


    # Concatenate them into a single DataFrame
    countries_temp_all_merged = pandas.concat(countries_merged, ignore_index=True)

    # save to csv for debugging
    countries_temp_all_merged.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/countries_temp_all_merged.csv', index=False, sep=';')

build_data(2024)
build_data(2019)
build_data(2014)
build_data(2009)

merge_all()