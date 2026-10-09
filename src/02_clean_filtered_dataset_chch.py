''' Clean the filtered dataset for Christchurch '''

# Load libraries / packages
import pandas as pd

# Input and output parameters
input_csv = "out/filtered_dataset.csv"
output_csv = "out/christchurch_listings_clean.csv"

def clean_airbnb_data():

    # Load the dataset
    christchurch = pd.read_csv(input_csv)

    # Drop unnecessary columns
    columns_to_drop = [
        "name",
        "host_name",
        "neighbourhood_group",
        "last_review",
        "reviews_per_month",
        "number_of_reviews_ltm",
        "license"
    ]

    christchurch_clean = christchurch.drop(
        columns=columns_to_drop
    )

    # Check the result
    print(christchurch_clean.head())
    print("======================================================================================")
    print("Shape of the new dataset: ", christchurch_clean.shape)
    print(christchurch_clean.columns)

    # Check data types
    print("======================================================================================")
    print("Data types:")
    print(christchurch_clean.dtypes)

    # Check missing values
    print("======================================================================================")
    print("Number of missing values:")
    print(christchurch_clean.isna().sum())

    # Check duplicate rows
    print("======================================================================================")
    print(
        "Duplicate rows:",
        christchurch_clean.duplicated().sum()
    )

    # Check duplicate listing IDs
    print(
        "Duplicate IDs:",
        christchurch_clean["id"].duplicated().sum()
    )

    # Check statistics of important columns
    print("======================================================================================")
    print(
        christchurch_clean[
            [
                "price",
                "minimum_nights",
                "number_of_reviews",
                "availability_365",
                "latitude",
                "longitude"
            ]
        ].describe()
    )

    # Look if duplicates have the same id-date combination
    duplicate_id_date = christchurch_clean.duplicated(
        subset=["id", "date"]
    ).sum()

    print("======================================================================================")
    print(
        "Duplicate ID-date combinations:",
        duplicate_id_date
    )

    # Check quantiles of price
    print("======================================================================================")
    print(
        christchurch_clean["price"].quantile(
            [
                0.90,
                0.95,
                0.99,
                0.995,
                0.999
            ]
        )
    )

    print(
        christchurch_clean.nlargest(
            20,
            "price"
        )[
            [
                "id",
                "date",
                "neighbourhood",
                "room_type",
                "price"
            ]
        ]
    )

    # Check counts
    print("======================================================================================")
    print("Room types:")
    print(
        christchurch_clean[
            "room_type"
        ].value_counts()
    )

    print("\nDates:")
    print(
        christchurch_clean[
            "date"
        ].value_counts().sort_index()
    )

    print("\nNeighbourhoods:")
    print(
        christchurch_clean[
            "neighbourhood"
        ].value_counts()
    )

    # Check invalid values
    print("======================================================================================")
    print("Invalid availability values:")
    print(
        (~christchurch_clean[
            "availability_365"
        ].between(0, 365)).sum()
    )

    print("\nInvalid minimum nights:")
    print(
        (
            christchurch_clean[
                "minimum_nights"
            ] <= 0
        ).sum()
    )

    print("\nInvalid prices:")
    print(
        (
            christchurch_clean[
                "price"
            ] <= 0
        ).sum()
    )

    # Save the new dataset
    christchurch_clean.to_csv(
        output_csv,
        index=False
    )

    print(
        f"\nClean Christchurch dataset saved to {output_csv}"
    )

    return christchurch_clean


if __name__ == "__main__":
    clean_airbnb_data()