''' Filtering csv files '''

import pandas as pd

# Create a dictionary with file path and date
FILES_DATES = {
    "data/Oct2025.csv": "October 2025",
    "data/Nov2025.csv": "November 2025",
    "data/Dec2025.csv": "December 2025",
    "data/Jan2026.csv": "January 2026",
    "data/Feb2026.csv": "February 2026",
    "data/Mar2026.csv": "March 2026",
    "data/Apr2026.csv": "April 2026",
    "data/May2026.csv": "May 2026",
    "data/Jun2026.csv": "June 2026"
}

# Create the dataframe
df = []

# Go through the dictionary to create the dataframe
for file_path, date in FILES_DATES.items():

    # Read the csv file
    dataset = pd.read_csv(file_path)

    # Filter for Christchurch City
    filtered_data = dataset[dataset["neighbourhood_group"] == "Christchurch City"]

    # Add column for month + year
    filtered_data["date"] = date

    # Put everything in the dataframe list
    df.append(filtered_data)

# Concatenate the dataframes in a single one
concat_dataset = pd.concat(df, ignore_index=True)

# Write the final csv file
concat_dataset.to_csv("data/filtered_dataset.csv", index=False)

all_data = []

all_data = concat_dataset