"""
Step 1: Query the Koordinates Vector Query API to get the SA2 (Statistical Area 2)
area code for every AirBnB listing's lat/lon, using the "Statistical Area 2 2026"
layer (id 123515) - the same layer used for the Location Id mapping in the task.

Run this LOCALLY (not in Claude's sandbox - that environment can't reach
koordinates.com). Needs: pip install pandas requests

Output: christchurch_listings_with_area_code.csv
    -> same as christchurch_listings_clean.csv, plus a new `area_code` column.

Upload that output file back to Claude to continue the join + analysis.
"""

import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---- CONFIG ----
API_KEY = "5511e5cf31c645b7a13dc91b1048b212"   # your Koordinates key
LAYER_ID = 123515                               # Statistical Area 2 - 2026
INPUT_CSV = "data/christchurch_listings_clean.csv"
OUTPUT_CSV = "christchurch_listings_with_area_code.csv"
SLEEP_BETWEEN_CALLS = 0   # be polite to the API; adjust if you hit rate limits

BASE_URL = "https://koordinates.com/services/query/v1/vector.json"


def get_area_code(x, y, session):
    """Query the vector API for a single point and return the SA2 code (or None)."""
    params = {
        "key": API_KEY,
        "layer": LAYER_ID,
        "x": x,
        "y": y,
        "max_results": 1,
        "radius": 50,  # metres - small buffer in case point sits exactly on a boundary
        "geometry": "false",  # we don't need the polygon geometry back, just properties
        "with_field_names": "true",
    }
    try:
        resp = session.get(BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        layer_data = data.get("vectorQuery", {}).get("layers", {}).get(str(LAYER_ID), {})
        features = layer_data.get("features", [])
        if not features:
            return None
        props = features[0]["properties"]
        # The SA2 code field is named like "SA22026_V1_00" in this layer.
        # Try the expected name first, then fall back to searching for any
        # field that looks like an SA2 code, in case Koordinates names it
        # slightly differently.
        for key in props:
            if key.upper().startswith("SA22026") and "NAME" not in key.upper():
                return props[key]
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ! request failed for ({x}, {y}): {e}")
        return None


def main():
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} rows from {INPUT_CSV}")

    unique_coords = df[["latitude", "longitude"]].drop_duplicates().reset_index(drop=True)
    print(f"{len(unique_coords)} unique lat/lon pairs to query")

    session = requests.Session()
    coord_to_area = {}

    for i, row in unique_coords.iterrows():
        lat, lon = row["latitude"], row["longitude"]
        area_code = get_area_code(lon, lat, session)  # NOTE: API wants x=lon, y=lat
        coord_to_area[(lat, lon)] = area_code

        if (i + 1) % 100 == 0 or (i + 1) == len(unique_coords):
            print(f"  queried {i + 1}/{len(unique_coords)}")

        time.sleep(SLEEP_BETWEEN_CALLS)

    df["area_code"] = df.apply(
        lambda r: coord_to_area.get((r["latitude"], r["longitude"])), axis=1
    )

    n_missing = df["area_code"].isna().sum()
    print(f"Done. {n_missing} of {len(df)} rows had no area code returned "
          f"(likely points just offshore/outside NZ SA2 boundaries).")

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()