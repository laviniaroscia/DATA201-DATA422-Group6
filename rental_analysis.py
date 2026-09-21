""" Rental analysis for Week 9 """

import pandas as pd
import matplotlib.pyplot as plt

from join_datasets import join_listings_and_bonds

def find_largest_rental_price_gaps(df):

    df["long_term_price_per_night"] = (df["Median Rent"] / 7).round(2) 

    df["price_gap"] = (df["price"]  - df["long_term_price_per_night"]).round(2)

    largest_gap_by_area = (
        df.groupby("area_code")["price_gap"]
        .max()
        .sort_values(ascending=False)
        .to_frame()
    )

    return largest_gap_by_area    

def plot_price_gap_distribution(df):
    ax = df.head(50).plot(
        kind="bar",
        figsize=(12, 6),
        legend=False
    )

    ax.set_title("Largest Rental Price Gaps by Area Code")
    ax.set_xlabel("Area Code")
    ax.set_ylabel("Price Gap ($ per night)")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():

    df = join_listings_and_bonds()

    largest_gap_by_area = find_largest_rental_price_gaps(df)

    print(largest_gap_by_area.head(50))

    plot_price_gap_distribution(largest_gap_by_area)


if __name__ == "__main__":
    main()
