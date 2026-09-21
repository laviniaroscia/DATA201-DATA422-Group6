""" Compare Airbnb listings and rental bonds by area code """

import pandas as pd
import matplotlib.pyplot as plt

def compare_property_counts(airbnb, bonds):

    airbnb = airbnb.copy()
    bonds = bonds.copy()

    # Convert Airbnb monthly dates to quarter start dates
    airbnb["quarter"] = (
        pd.to_datetime(
            airbnb["date"],
            format="%B %Y"
        )
        .dt.to_period("Q")
        .dt.start_time
    )

    # Convert bond timeframe to datetime
    bonds["TimeFrame"] = pd.to_datetime(
        bonds["TimeFrame"]
    )

    # Make area codes consistent
    airbnb["area_code"] = pd.to_numeric(
        airbnb["area_code"],
        errors="coerce"
    ).astype("Int64")

    bonds["Location Id"] = pd.to_numeric(
        bonds["Location Id"],
        errors="coerce"
    ).astype("Int64")

    # Airbnb counts
    airbnb_counts = (
        airbnb
        .groupby(
            ["quarter", "area_code", "area_name"]
        )["id"]
        .nunique()
        .reset_index(
            name="airbnb_properties"
        )
    )

    # Keep only total bond values
    bond_all = bonds[
        (bonds["Dwelling Type"] == "ALL") &
        (bonds["Number Of Beds"] == "ALL")
    ].copy()

    bond_counts = (
        bond_all[
            [
                "TimeFrame",
                "Location Id",
                "Active Bonds"
            ]
        ]
        .rename(
            columns={
                "TimeFrame": "quarter",
                "Location Id": "area_code",
                "Active Bonds": "rental_properties"
            }
        )
    )

    # Merge Airbnb and bond counts
    comparison = airbnb_counts.merge(
        bond_counts,
        on=["quarter", "area_code"],
        how="inner"
    )

    comparison = comparison.sort_values(
        ["quarter", "airbnb_properties"],
        ascending=[True, False]
    )

    return comparison

def plot_property_counts(comparison):

    latest_quarter = comparison["quarter"].max()

    latest = comparison[
        comparison["quarter"] == latest_quarter
    ].copy()

    latest = latest.sort_values(
        "airbnb_properties",
        ascending=False
    ).head(30)

    latest = latest.set_index("area_name")

    ax = latest[
        ["airbnb_properties", "rental_properties"]
    ].plot(
        kind="bar",
        figsize=(14, 7)
    )

    ax.set_title(
        f"Airbnb vs Long-Term Rental Properties by Area "
        f"({latest_quarter.strftime('%b %Y')})"
    )

    ax.set_xlabel("Area")
    ax.set_ylabel("Number of Properties")

    ax.legend(
        ["Airbnb", "Long-term rentals"]
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(
        "images/airbnb_vs_long_term_properties.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def main():

    airbnb = pd.read_csv(
        "data/christchurch_listings_with_area_codes.csv"
    )

    bonds = pd.read_csv(
        "data/bond_data_clean.csv"
    )

    comparison = compare_property_counts(
        airbnb,
        bonds
    )

    print(comparison)

    plot_property_counts(comparison)


if __name__ == "__main__":
    main()