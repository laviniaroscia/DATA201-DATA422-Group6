""" Rental analysis for Week 9 """

import pandas as pd
import matplotlib.pyplot as plt

from join_datasets import join_listings_and_bonds

def calculate_rental_price_gaps(df):

    df = df[df["minimum_nights"] <= 7].copy()

    df["long_term_price_per_night"] = (
        df["Median Rent"] / 7
    ).round(2)

    df["price_gap"] = (
        df["price"] - df["long_term_price_per_night"]
    ).round(2)

    return df


def summarise_price_gaps(df):

    gap_by_area = (
        df.groupby("area_name")
        .agg(
            median_gap=("price_gap", "median"),
            number_of_listings=("id", "nunique")
        )
    )

    # Keep areas with enough listings
    gap_by_area = gap_by_area[
        gap_by_area["number_of_listings"] >= 10
    ]

    # Remove areas without a valid price gap
    gap_by_area = gap_by_area.dropna(
        subset=["median_gap"]
    )

    # Sort from largest to smallest gap
    gap_by_area = gap_by_area.sort_values(
        "median_gap",
        ascending=False
    )

    return gap_by_area

def plot_median_price_gap(gap_by_area):

    top_areas = gap_by_area.head(30)

    ax = top_areas["median_gap"].plot(
        kind="bar",
        figsize=(14, 7),
        legend=False
    )

    ax.set_title("Median Price Gap Between Short-Term and Long-Term Rentals by Area")
    ax.set_xlabel("Area")
    ax.set_ylabel("Median Price Gap ($ per night)")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        "out/images/rental_price_gap_by_area.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()

def main():

    df = join_listings_and_bonds()

    df = calculate_rental_price_gaps(df)

    gap_by_area = summarise_price_gaps(df)

    print(gap_by_area.head(30))

    plot_median_price_gap(gap_by_area)


if __name__ == "__main__":
    main()