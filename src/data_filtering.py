''' Filtering csv files '''

import pandas as pd
from pathlib import Path
from datetime import datetime

# Get the scrape dates for later analysis
scrape_dates = {
    "October 2025": "2025-10-05",
    "November 2025": "2025-11-07",
    "December 2025": "2025-12-11",
    "January 2026": "2026-01-16",
    "February 2026": "2026-02-13",
    "March 2026": "2026-03-17",
    "April 2026": "2026-04-16",
    "May 2026": "2026-05-23",
    "June 2026": "2026-06-19",
    "July 2026": "2026-07-12",
    "August 2026": "2026-08-13"
}

data_folder = Path("data")

# Find only monthly Airbnb CSV files
csv_files = []

for file_path in data_folder.glob("*.csv"):
    try:
        datetime.strptime(file_path.stem, "%b%Y")
        csv_files.append(file_path)
    except ValueError:
        pass

# Sort files chronologically
csv_files.sort(
    key=lambda file: datetime.strptime(file.stem, "%b%Y")
)

# Check which files were found
print(f"Airbnb files found: {len(csv_files)}")

for file_path in csv_files:
    date = datetime.strptime(
        file_path.stem, "%b%Y"
    ).strftime("%B %Y")
    
    print(f" - {date}")

output_csv = "out/filtered_dataset.csv"

all_christchurch_data = []

# Create the dataframe
df = []

# Go through all CSV files
for file_path in csv_files:

    # Extract month and year from filename
    # Example: Aug2026.csv -> August 2026
    date = datetime.strptime(file_path.stem, "%b%Y").strftime("%B %Y")

    # Read the CSV file
    dataset = pd.read_csv(file_path)

    # Filter for Christchurch City
    filtered_data = dataset[
        dataset["neighbourhood_group"] == "Christchurch City"
    ].copy()

    # Add column for month + year
    filtered_data["date"] = date

    # Add column with scrape date
    filtered_data["scrape_date"] = scrape_dates[date]

    # Add to dataframe list
    df.append(filtered_data)

# Concatenate all months
concat_dataset = pd.concat(df, ignore_index=True)

# Write the final CSV file
concat_dataset.to_csv(output_csv, index=False)

all_christchurch_data = concat_dataset