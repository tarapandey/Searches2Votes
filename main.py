from serpapi import GoogleSearch
import pandas as pd
import numpy as np

params = {
    "engine": "google_trends",
    "q": "zombies",
    "date": "2024-01-01 2024-11-05",
    "data_type": "GEO_MAP_0",
    "geo": "US",
    "api_key": "API-KEY"
}

search = GoogleSearch(params)
results = search.get_dict()

region_data = results.get("interest_by_region", [])

data = {
    entry["location"]: entry["value"]
    for entry in region_data
}

# Create the DataFrame
df = pd.DataFrame.from_dict(data, orient="index", columns=["zombies"])
df.index.name = "geoName"

election_data = pd.read_excel('election_results')
state_codes = pd.read_csv('map_data.csv')
election_data = election_data[:51]

#creating merged_df that includes the vote counts
merged_df = pd.merge(election_data, state_codes, on='STATE', how='left')
merged_df = merged_df.fillna(0)
merged_df = pd.merge(merged_df, df, on='geoName', how='left')

#finding the number of votes for Trump/Harris proportional to total votes in each state
merged_df['HARRIS FRAC TOTAL'] = merged_df['HARRIS']/merged_df['TOTAL VOTES'].sum()
merged_df['TRUMP FRAC TOTAL'] = merged_df['TRUMP']/merged_df['TOTAL VOTES'].sum()

#correlation of Harris votes with 'zombies' searches
correlation = merged_df['HARRIS FRAC TOTAL'].corr(merged_df['zombies'])
print(correlation)