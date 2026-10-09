""" Airbnb analysis """

# Load libraries / packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Input and output parameters
input_csv = "out/filtered_dataset.csv"
output_price_distribution_img = "out/images/airbnb_price_distribution.png"
output_review_distribution_img = "out/images/days_since_last_review.png"


def plot_summary_statistics(data):
    """ Summary statistics for all columns """

    if len(data) == 0:
        print("No data.")
        return

    print("\nDataset Shape:", data.shape)

    print(
        data.dtypes.to_frame("Data Type").join([
            data.count().rename("Count"),
            data.isnull().sum().rename("Missing Values"),
            data.nunique().rename("Unique Values")
        ])
    )

    print("\nSummary statistics for numeric data:")
    summ_numeric_data = data.describe(include=[np.number]).T
    print(summ_numeric_data)

    print("\nSummary statistics for categorical data:")
    summ_category_data = data[
        [
            "name",
            "host_name",
            "neighbourhood_group",
            "neighbourhood",
            "room_type",
            "last_review",
            "date"
        ]
    ].describe().T

    print(summ_category_data)


def price_distribution(data):
    """ Plot the price distribution for Christchurch """

    print("\nShape of prices:")
    print(data["price"].describe())

    # Remove missing values
    prices = data["price"].dropna()

    # Remove outliers from visualisation
    upper_limit = prices.quantile(0.99)
    prices_filtered = prices[prices <= upper_limit]

    # Plot distribution
    plt.figure(figsize=(10, 6))
    plt.hist(prices_filtered, bins=30)

    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.title("Distribution of Airbnb Prices in Christchurch")

    plt.tight_layout()

    plt.savefig(
        output_price_distribution_img,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def days_since_last_review(data):
    """ Plot the distribution of days since last review """

    # Convert dates
    data["scrape_date"] = pd.to_datetime(
        data["scrape_date"]
    )

    data["last_review"] = pd.to_datetime(
        data["last_review"]
    )

    # Calculate days since last review
    data["days_since_last_review"] = (
        data["scrape_date"]
        - data["last_review"]
    ).dt.days

    # Check the new feature
    print("\nShape of days since last review:")
    print(
        data["days_since_last_review"].describe()
    )

    # Remove missing values
    review_days = (
        data["days_since_last_review"]
        .dropna()
    )

    # Remove outliers from visualisation
    upper_limit = review_days.quantile(0.99)

    review_days_filtered = review_days[
        review_days <= upper_limit
    ]

    # Plot distribution
    plt.figure(figsize=(10, 6))
    plt.hist(review_days_filtered, bins=30)

    plt.xlabel("Days Since Last Review")
    plt.ylabel("Frequency")
    plt.title("Distribution of Days Since Last Review")

    plt.tight_layout()

    plt.savefig(
        output_review_distribution_img,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def highest_number_of_reviews_10_percent(data):
    """ Highest numbers of reviews (filter top 10%) """

    if len(data) == 0:
        print("No data.")
        return

    top_10_percent = data[
        data["number_of_reviews"]
        > data["number_of_reviews"].quantile(0.9)
    ].sort_values(
        "number_of_reviews",
        ascending=False
    )

    print(
        "\nHighest Number of Reviews (Top 10%)",
        "\nTotal number of properties:",
        len(top_10_percent),
        "\nTotal of Reviews:",
        top_10_percent["number_of_reviews"].sum(),
        "\n"
    )

    print(
        "Properties with the highest numbers of reviews (Top 10%)"
    )

    print(
        top_10_percent[
            [
                "id",
                "neighbourhood_group",
                "price",
                "number_of_reviews",
                "last_review"
            ]
        ].head(20).to_string()
    )


def run_airbnb_analysis():
    """ Run all Airbnb analyses """

    print(f"\nLoading Airbnb data from {input_csv}...")

    data = pd.read_csv(input_csv)

    plot_summary_statistics(data)
    price_distribution(data)
    days_since_last_review(data)
    highest_number_of_reviews_10_percent(data)

    print("\nAirbnb analysis completed.")


if __name__ == "__main__":
    run_airbnb_analysis()