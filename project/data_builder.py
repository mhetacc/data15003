import pandas 

# Step 1: Merge `parties.csv` and `country_codes.csv` on `DIVISION_ID = alpha-2`
parties = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/eu_parliament/2024/parties.csv', sep=';')
country_codes = pandas.read_csv('/home/mhetac/Documents/GitHub/data15003/project/data/country_codes.csv', sep=';')

# Merge on DIVISION_ID and alpha-2
parties_with_countries = pandas.merge(parties, country_codes, left_on='DIVISION_ID', right_on='alpha-2', how='left')

parties_with_countries.to_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/parties_with_countries.csv', index=False)


# Step 2: Merge the new `parties.csv` with each `result-parties-country.csv` on `ID = PARTY_ID`
# Assuming there are multiple `result-parties-country.csv` files
#import glob
#
#result_files = glob.glob('/home/mhetac/Documents/GitHub/data15003/project/data/eu_parliament/2024/result-parties-*.csv')
#merged_results = []
#
#for file in result_files:
#    result_data = pandas.read_csv(file)
#    merged_result = pandas.merge(parties_with_countries, result_data, left_on='ID', right_on='PARTY_ID')
#    merged_results.append(merged_result)
#
## Combine all merged results into a single DataFrame
#final_data = pandas.concat(merged_results, ignore_index=True)
#
## Step 3: Add a `year` column to all data
#final_data['year'] = 2024  # Add the current year
#
## Save the final dataset to a CSV file
#final_data.to_csv('/home/mhetac/Documents/GitHub/data15003/project/data/build/2024_dataset.csv', index=False)
#
#print("Merged dataset saved to 'final_dataset.csv'")