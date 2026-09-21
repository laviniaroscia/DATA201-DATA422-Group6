""" Compare Airbnb listings and rental bonds by area code """

import pandas as pd
from join_datasets import join_listings_and_bonds

# Take the joined datasets
merged_df = join_listings_and_bonds()

# Count the number of unique Airbnb listings by area code and area name
airbnb_by_area = (merged_df.groupby(["area_code", "area_name"])["id"].nunique().reset_index(name="airbnb_count")
)
print(airbnb_by_area.head())

# Find the "ALL" dwelling type and "ALL" number of beds in the merged dataset
print(merged_df["Dwelling Type"].unique())
print(merged_df["Number Of Beds"].unique())


rentals = merged_df[merged_df["Dwelling Type"] == "ALL"].copy()

rentals = merged_df[(merged_df["Dwelling Type"] == "ALL") & (merged_df["Number Of Beds"] == "ALL")].copy()
rentals = rentals.drop_duplicates(subset=["Location Id", "TimeFrame"])

# Count the average number of active rental bonds by area code
rentals_by_area = (rentals.groupby("Location Id")["Active Bonds"].mean().reset_index(name="rentals_count"))

# Merge the two datasets on area code and location id
comparison = pd.merge(airbnb_by_area, rentals_by_area, left_on = "area_code", right_on="Location Id", how="inner")

# Printing the comparison of Airbnb listings and rental bonds by area code
comparison = comparison[["area_code", "area_name", "airbnb_count", "rentals_count"]]
print(comparison.head())