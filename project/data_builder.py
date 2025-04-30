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



    # OSS: this wont work before having output at line circa 101

    ## add random political temperature to each one
    ## parties_countries_percentage['TEMPERATURE'] = numpy.random.uniform(-2, 2, size=len(parties_countries_percentage))

    # take parties with their scores 
    parties_scored = pandas.read_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/Ai/parties_scored_{year}.csv', sep=';')

    # join on LABEL the whole thing plus temperatures df 
    parties_countries_percentage = pandas.merge(parties_countries_percentage, parties_scored, left_on='LABEL', right_on='LABEL', how='outer')


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
    parties_countries_percentage[['LABEL', 'name', 'VOTES_PERCENT', 'TEMPERATURE', 'WEIGHTED_TEMP']].to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/debug_for_votes_{year}_parties.csv', index=False, sep=';')


    # Get unique, non-null LABEL values
    list_of_parties = parties_countries_percentage['LABEL'].dropna().unique()
    list_of_parties_df = pandas.DataFrame(list_of_parties, columns=['LABEL'])
    list_of_parties_df.to_csv(f'/home/mhetac/Documents/GitHub/data15003/project/data/build/list_of_parties_{year}.csv', index=False, sep=';')


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



def build_net_earnings():
    earnings_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/annual_net_earnings.csv', sep=',')

    filtered_earnings= earnings_df[(earnings_df['estruct']=='Net earning') & (earnings_df['currency']=='Euro') & (earnings_df['ecase']=='Single person without children earning 100% of the average earning')]

    filtered_earnings = filtered_earnings[['geo', 'currency', 'TIME_PERIOD', 'OBS_VALUE']]

    filtered_earnings.rename(columns={'geo': 'COUNTRY_NAME', 'currency': 'CURRENCY', 'TIME_PERIOD': 'YEAR', 'OBS_VALUE': 'NET_EARNINGS'}, inplace=True)

    filtered_earnings.to_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_net_earnings.csv', index=False, sep=';')

def build_immigration():
    migri_df = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/immigration.csv', sep=',')

    filtered_migri = migri_df[(migri_df['age']=='Total') & (migri_df['sex']=='Total') & (migri_df['agedef']=='Age reached during the year')]

    filtered_migri = filtered_migri[['geo', 'TIME_PERIOD', 'OBS_VALUE']]
    filtered_migri.rename(columns={'geo': 'COUNTRY_NAME', 'TIME_PERIOD': 'YEAR', 'OBS_VALUE': 'IMMIGRATION'}, inplace=True)

    # remove useless rows
    filtered_migri = filtered_migri[filtered_migri['COUNTRY_NAME'] != 'European Union - 27 countries (from 2020)']


    # Calculate average immigration per year
    avg_df = filtered_migri.groupby('YEAR', as_index=False)['IMMIGRATION'].mean()

    # Add a placeholder country name
    avg_df['COUNTRY_NAME'] = 'Europe Average'

    # Reorder columns to match original DataFrame
    avg_df = avg_df[['COUNTRY_NAME', 'YEAR', 'IMMIGRATION']]

    # Append to original DataFrame
    filtered_migri = pandas.concat([filtered_migri, avg_df], ignore_index=True)

    filtered_migri.to_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/annual_immigration.csv', index=False, sep=';')

# build_data(2024)
# build_data(2019)
# build_data(2014)
# build_data(2009)
# 
# merge_all()
# 
# build_net_earnings()

build_immigration()