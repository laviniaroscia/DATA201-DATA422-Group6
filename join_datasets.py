import pandas as pd

""" Join together both datasets on the area code and time. """
def join_listings_and_bonds():

    listings_path = 'data/christchurch_listings_with_area_codes.csv'
    bonds_path = 'data/bond_data_clean.csv'

    listings = pd.read_csv(listings_path)
    bonds = pd.read_csv(bonds_path)

    bonds["Location Id"] = bonds["Location Id"].fillna(0)
    bonds["Location Id"] = bonds["Location Id"].astype("int64")
    
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