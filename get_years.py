#Imports
import pandas as pd
# packages helpful for webscraping
import requests
from bs4 import BeautifulSoup

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# Loop through the years 1993 to 2023 (can adjust year range to what we need)
for year in range(1993, 2024):
    url = f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    # Find table with class 'wikitable'
    wikitables = soup.findAll("table", {'class': 'wikitable'})
    if not wikitables:
        continue
    
    tbl = wikitables[0]
    
    # Create a list to hold the data for the current year
    data = []
    
    # Iterate through the rows of the table
    for row in tbl.findAll("tr"):
        cols = row.findAll(["td", "th"])
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    # Create a DataFrame from the data
    year_df = pd.DataFrame(data[1:], columns=data[0])
    year_df['Year'] = year  # Add a column for the year
    
    # Append the current year's DataFrame to the all_data DataFrame
    all_data = pd.concat([all_data, year_df], ignore_index=True)

# Save the DataFrame to a CSV file
all_data.to_csv('billboard_year_end_hot_100_singles_1993_2023.csv', index=False)