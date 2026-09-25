""" AirBnB analysis for Week 5 """

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from data_filtering import all_data

def plot_summary_statistics():
    """ Summary statistics for all columns """

    if (len(all_data) == 0):
        print("No data.")
        return       

    # Summary statistics for all columns
    print("\nDataset Shape:", all_data.shape)     

    print(all_data.dtypes.to_frame("Data Type").join([all_data.count().rename("Count")
    , all_data.isnull().sum().rename("Missing Values"), all_data.nunique().rename("Unique Values")]))
   
    print("Summary statistics for numeric data:")
    summ_numeric_data = all_data.describe(include=[np.number]).T  
    print(summ_numeric_data)

    print("Summary statistics for categorical data:")  
    summ_category_data = all_data[[ 'name', 'host_name', 'neighbourhood_group',
       'neighbourhood', 'room_type', 'last_review','date']].describe().T   
    print(summ_category_data)

def price_distribution():
    """ Plot the price distribution for Christchurch """

    # Check the data to see outliers
    print("Shape of prices:")
    print(all_data["price"].describe())

    # Remove missing values from the prices
    prices = all_data["price"].dropna()

    # Remove the outliers
    upper_limit = prices.quantile(0.99)
    prices_filtered = prices[prices <= upper_limit]

    # Plot the distribution 
    plt.hist(prices_filtered, bins=30)

    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.title("Distribution of Airbnb Prices in Christchurch")

    plt.show()

def days_since_last_review():
    """ Plot the distribution of days since last review """

    # Create scrape date
    scrape_date = pd.to_datetime("2026-06-19")

    # Convert data type
    all_data["last_review"] = pd.to_datetime(all_data["last_review"])

    # Find the number of days since last review
    all_data["days_since_last_review"] = (
        scrape_date - all_data["last_review"]
    ).dt.days

    # Check the new feature
    print("Shape of days since last review:")
    print(all_data["days_since_last_review"].describe())

    # Remove missing values
    review_days = all_data["days_since_last_review"].dropna()

    # Remove the outliers
    upper_limit = review_days.quantile(0.99)

    review_days_filtered = review_days[
        review_days <= upper_limit
    ]

    # Plot the distribution
    plt.hist(review_days_filtered, bins=30)

    plt.xlabel("Days Since Last Review")
    plt.ylabel("Frequency")
    plt.title("Distribution of Days Since Last Review")

    plt.show()

def highest_number_of_reviews_10_percent():
    """ Highest numbers of reviews (filter top 10%)  """

    if (len(all_data) == 0):
        print("No data.")
        return    

    top_10_percent = all_data[all_data['number_of_reviews'] > all_data['number_of_reviews'].quantile(0.9)].sort_values('number_of_reviews', ascending=False)
    print("\nHighest Number of Reviews (Top 10%)", "\nTotal number of properties:", len(top_10_percent), "\nTotal of Reviews:", top_10_percent["number_of_reviews"].sum(),"\n")

    print("Properties with the highest numbers of reviews (Top 10%)")
    print(top_10_percent[['id','neighbourhood_group','price','number_of_reviews','last_review']].head(20).to_string())
    
def main():  
    """ Main function """ 

    plot_summary_statistics()
    price_distribution()
    days_since_last_review()
    highest_number_of_reviews_10_percent()

main()