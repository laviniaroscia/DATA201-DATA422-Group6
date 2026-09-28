""" Join Airbnb listing data and rental bond data on area code and time. """

input_airbnb_csv = "out/christchurch_listings_with_area_codes.csv"
input_rental_bond_csv = "out/bond_data_clean.csv"

import pandas as pd

""" Join together both datasets on the area code and time. """
def join_listings_and_bonds():

    listings = pd.read_csv(input_airbnb_csv)
    bonds = pd.read_csv(input_rental_bond_csv)

    bonds["Location Id"] = bonds["Location Id"].fillna(0)
    bonds["Location Id"] = bonds["Location Id"].astype("int64")

    listings["area_code"] = listings["area_code"].fillna(0)
    listings["area_code"] = listings["area_code"].astype("int64")
    
    listings["date"] = pd.to_datetime(
        listings["date"],
        format="%B %Y"
    )

    bonds["TimeFrame"] = pd.to_datetime(
        bonds["TimeFrame"]
    )    

    merged_df = pd.merge(
        listings,
        bonds,
        left_on=["area_code", "date"],
        right_on=["Location Id", "TimeFrame"],
        how="left"
    )    

    return merged_df

    

""" Start joining dataset"""
join_listings_and_bonds()