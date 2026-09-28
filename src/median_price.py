"""
Deliverable 5 — median AirBnB price in Christchurch Central
(SA2 / Location ID 326600).

Input: christchurch_listings_with_area_codes.csv
       (produced by Lavinia's get_area_codes.py — must be run locally,
       since it hits the Koordinates API)
"""

CHRISTCHURCH_CENTRAL_ID = 326600

input_csv = "out/christchurch_listings_with_area_codes.csv"

import pandas as pd

def main():
    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} rows from {input_csv}")

    # area_code can come back as a string or float depending on how the
    # API/CSV round-trip handled it — coerce to numeric so the filter works
    df["area_code"] = pd.to_numeric(df["area_code"], errors="coerce")

    central = df[df["area_code"] == CHRISTCHURCH_CENTRAL_ID]
    print(f"{len(central)} listings found in Christchurch Central "
          f"(ID {CHRISTCHURCH_CENTRAL_ID})")

    if len(central) == 0:
        print("No listings matched — check that area_code was populated "
              "correctly, or that IDs are being compared as the same type.")
        return

    median_price = central["price"].median()
    print(f"\nMedian AirBnB price in Christchurch Central: ${median_price:.2f}")

    print("\nFull price summary for Christchurch Central:")
    print(central["price"].describe())


if __name__ == "__main__":
    main()
