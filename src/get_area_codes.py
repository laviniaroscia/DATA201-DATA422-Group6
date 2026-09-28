""" Retrieve area codes for Airbnb listings by matching their latitude and longitude coordinates
using the Koordinates API. """

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
from dotenv import load_dotenv

input_csv = "out/christchurch_listings_clean.csv"
output_csv = "out/christchurch_listings_with_area_codes.csv"
lookup_csv = "out/area_code_lookup.csv"

load_dotenv()

API_KEY = os.getenv("KOORDINATES_API_KEY")

if not API_KEY:
    raise ValueError(
        "KOORDINATES_API_KEY not found. "
        "Add it to the .env file in the project root."
    )

LAYER_ID = 98970


# -----------------------------
# Function to query SA2 area
# -----------------------------

def get_area_info(latitude, longitude):

    url = "https://koordinates.com/services/query/v1/vector.json"

    params = {
        "key": API_KEY,
        "layer": LAYER_ID,
        "x": longitude,
        "y": latitude,
        "max_results": 1,
        "radius": 0,
        "geometry": "false",
        "with_field_names": "true"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        features = data[
            "vectorQuery"
        ][
            "layers"
        ][
            str(LAYER_ID)
        ][
            "features"
        ]

        # No SA2 area found
        if not features:
            return None, None

        properties = features[0]["properties"]

        area_code = properties["SA22019_V1_00"]
        area_name = properties["SA22019_V1_00_NAME"]

        return area_code, area_name

    except requests.RequestException as e:
        print(
            f"Error for {latitude}, {longitude}: {e}"
        )

        return None, None


# -----------------------------
# Function used by the threads
# -----------------------------

def query_coordinate(coord):

    latitude, longitude = coord

    return get_area_info(
        latitude,
        longitude
    )


# -----------------------------
# Main area-code processing
# -----------------------------

def add_area_codes():

    # Load cleaned Airbnb CSV
    df = pd.read_csv(input_csv)

    print("\nDataset loaded successfully.")
    print("Rows in dataset:", len(df))

    # Keep only unique coordinates
    unique_coords = (
        df[["latitude", "longitude"]]
        .dropna()
        .drop_duplicates()
    )

    print(
        "Unique coordinates in dataset:",
        len(unique_coords)
    )

    # Load existing coordinate lookup if available
    try:
        lookup_df = pd.read_csv(lookup_csv)

        print(
            "Coordinates already stored:",
            len(lookup_df)
        )

    except FileNotFoundError:

        lookup_df = pd.DataFrame(
            columns=[
                "latitude",
                "longitude",
                "area_code",
                "area_name"
            ]
        )

        print("No existing coordinate lookup found.")

    # Find coordinates that have not been queried yet
    coords_to_query = unique_coords.merge(
        lookup_df[
            ["latitude", "longitude"]
        ],
        on=["latitude", "longitude"],
        how="left",
        indicator=True
    )

    coords_to_query = coords_to_query[
        coords_to_query["_merge"] == "left_only"
    ][
        ["latitude", "longitude"]
    ]

    coords = list(
        coords_to_query.itertuples(
            index=False,
            name=None
        )
    )

    print(
        "New coordinates to query:",
        len(coords)
    )

    # Query only new coordinates
    if coords:

        with ThreadPoolExecutor(
            max_workers=8
        ) as executor:

            results = list(
                tqdm(
                    executor.map(
                        query_coordinate,
                        coords
                    ),
                    total=len(coords),
                    desc="Querying Koordinates"
                )
            )

        # Create dataframe with new results
        new_lookup = pd.DataFrame(
            [
                {
                    "latitude": coord[0],
                    "longitude": coord[1],
                    "area_code": result[0],
                    "area_name": result[1]
                }
                for coord, result in zip(
                    coords,
                    results
                )
            ]
        )

        # Add new results to existing lookup
        lookup_df = pd.concat(
            [
                lookup_df,
                new_lookup
            ],
            ignore_index=True
        )

        # Save updated lookup
        lookup_df.to_csv(
            lookup_csv,
            index=False
        )

        print(
            "Coordinate lookup updated."
        )

    else:
        print(
            "No new coordinates to query."
        )

    # Add area information to full Airbnb dataset
    df = df.merge(
        lookup_df,
        on=[
            "latitude",
            "longitude"
        ],
        how="left"
    )

    # Check results
    print(
        df[
            [
                "latitude",
                "longitude",
                "area_code",
                "area_name"
            ]
        ].head(10)
    )

    print(
        "Missing area codes:",
        df["area_code"].isna().sum()
    )

    # Save final dataset
    df.to_csv(
        output_csv,
        index=False
    )

    print(
        "Dataset saved successfully as "
        "'christchurch_listings_with_area_codes.csv'"
    )

    return df


if __name__ == "__main__":
    add_area_codes()