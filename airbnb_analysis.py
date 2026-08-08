import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from data_filtering import all_data

""" Summary statistics for all columns """
def plot_summary_statistics():

    if (len(all_data) == 0):
        print("No data.")
        return       

    #Summary statistics for all columns
    print("\nDataset Shape:", all_data.shape)     

    print(all_data.dtypes.to_frame("Data Type").join([all_data.count().rename("Count")
    , all_data.isnull().sum().rename("Missing Values"), all_data.nunique().rename("Unique Values")]))
   
    print("Summary statistics for numeric data:")
    summ_numberic_data = all_data.describe(include=[np.number]).T  
    print(summ_numberic_data)

    print("Summary statistics for categorial data:")  
    summ_category_data = all_data[[ 'name', 'host_name', 'neighbourhood_group',
       'neighbourhood', 'room_type', 'last_review','date']].describe().T   
    print(summ_category_data)
 


""" Highest numbers of reviews (filter top 10%)  """
def highest_number_of_reviews_10_percent():

    if (len(all_data) == 0):
        print("No data.")
        return    

    top_10_percent = all_data[all_data['number_of_reviews'] > all_data['number_of_reviews'].quantile(0.9)].sort_values('number_of_reviews', ascending=False)
    print("\nHighest Number of Reviews (Top 10%)", "\nTotal numer of properties:", len(top_10_percent), "\nToal of Reviews:", top_10_percent["number_of_reviews"].sum(),"\n")

    print("Properties with the highest numbers of reviews (Top 10%)")
    print(top_10_percent[['id','neighbourhood_group','price','number_of_reviews','last_review']].head(20).to_string())
    
    
plot_summary_statistics()
highest_number_of_reviews_10_percent()