import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


# -----------------------------
# 1. Load the cleaned Airbnb CSV
# -----------------------------

df = pd.read_csv("data/christchurch_listings_clean.csv")

print("Dataset loaded successfully.")
print("Rows in dataset:", len(df))


# -----------------------------
# 2. Koordinates API settings
# -----------------------------

API_KEY = "2ef18a6e28154d0cb4abee56df55da73"
LAYER_ID = 98970


# -----------------------------
# 3. Function to query SA2 area
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
# 4. Keep only unique coordinates
# -----------------------------

unique_coords = (
    df[["latitude", "longitude"]]
    .dropna()
    .drop_duplicates()
)

coords = list(
    unique_coords.itertuples(
        index=False,
        name=None
    )
)

print("Unique coordinates to query:", len(coords))


# -----------------------------
# 5. Function used by the threads
# -----------------------------

def query_coordinate(coord):

    latitude, longitude = coord

    return get_area_info(
        latitude,
        longitude
    )


# -----------------------------
# 6. Query Koordinates in parallel
# -----------------------------

with ThreadPoolExecutor(max_workers=8) as executor:

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


# -----------------------------
# 7. Create coordinate → SA2 lookup
# -----------------------------

area_lookup = {
    coord: result
    for coord, result in zip(
        coords,
        results
    )
}


# -----------------------------
# 8. Add SA2 information to dataframe
# -----------------------------

def lookup_area(row):

    lat = row["latitude"]
    lon = row["longitude"]

    if pd.isna(lat) or pd.isna(lon):
        return pd.Series([None, None])

    return pd.Series(
        area_lookup.get(
            (lat, lon),
            (None, None)
        )
    )


df[
    ["area_code", "area_name"]
] = df.apply(
    lookup_area,
    axis=1
)


# -----------------------------
# 9. Check the results
# -----------------------------

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


# -----------------------------
# 10. Save the final dataset
# -----------------------------

df.to_csv(
    "data/christchurch_listings_with_area_codes.csv",
    index=False
)

print(
    "Dataset saved successfully as "
    "'christchurch_listings_with_area_codes.csv'"
)