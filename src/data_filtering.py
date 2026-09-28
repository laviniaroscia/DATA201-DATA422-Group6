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


def filter_airbnb_data():
    ''' Filter AirBnB data '''

    data_folder = Path("data")
    output_csv = "out/filtered_dataset.csv"

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

    # Create dataframe list
    df = []

    # Go through all CSV files
    for file_path in csv_files:

        # Extract month and year from filename
        date = datetime.strptime(
            file_path.stem, "%b%Y"
        ).strftime("%B %Y")

        # Read CSV
        dataset = pd.read_csv(file_path)

        # Filter for Christchurch City
        filtered_data = dataset[
            dataset["neighbourhood_group"] == "Christchurch City"
        ].copy()

        # Add month + year
        filtered_data["date"] = date

        # Add scrape date
        filtered_data["scrape_date"] = scrape_dates[date]

        # Add dataframe to list
        df.append(filtered_data)

    # Concatenate all months
    concat_dataset = pd.concat(
        df,
        ignore_index=True
    )

    # Save final dataset
    concat_dataset.to_csv(
        output_csv,
        index=False
    )

    print(f"Filtered dataset saved to {output_csv}")

    return concat_dataset


if __name__ == "__main__":
    filter_airbnb_data()