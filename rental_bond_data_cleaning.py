""" Rental bond data cleaning for Week 8 """

import pandas as pd
import numpy as np

file_path = 'data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv'

""" Clean the rental bond dataset. """
def clean_bond_dataset():

    # Read the csv file
    bond_df = pd.read_csv(file_path)

    # Uncomment the lines below to view the dataset overview before timeframe filtering
    # print("\nBefore Data Cleaning (All Data): Rental Bond Dataset")
    # display_dataset_overview(bond_df)

    # Update column data types
    bond_df['TimeFrame'] = pd.to_datetime(bond_df['TimeFrame'])

    #display_dataset_overview(bond_df)    

    # Apply timeframe filtering.
    filtered_data = filter_timeframe(bond_df)
    # Use the full dataset if no filtered records are returned.   
    if (len(filtered_data) == 0):  
        filtered_data = bond_df

    #Duplicate Records
    print("Duplicate rows:", filtered_data.duplicated().sum())

    print("\nBefore Data Cleaning (After Timeframe Filtering): Rental Bond Dataset")
    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)

    print("\nAfter Data Cleaning (After Timeframe Filtering)")
    #Dropped Log Std Dev Weekly Rent as it is difficult to interpret from a business perspective
    #and provides limited information compared with other rent metrics. 
    filtered_data = filtered_data.drop(columns=['Log Std Dev Weekly Rent'])

    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)

    # 94 records out of a total of 27,212 with missing Location Id were retained because
    # they represent only 0.35% of the dataset. These records also have missing values in
    # Median Rent, Geometric Mean Rent, Upper Quartile Rent, and Lower Quartile Rent.
    # However, they still contain valid information in Dwelling Type, Number Of Beds,
    # Total Bonds, Active Bonds, and Closed Bonds.

    #Create a reference table using records with valid Location Id and Number Of Beds.
    #This table is used to identify matching Number Of Beds values based on
    #Location Id, Dwelling Type, and Median Rent for imputation purposes.
    beds_reference = (
        filtered_data[
            (filtered_data['Location Id'].notna()) &
            (filtered_data['Number Of Beds'].notna())
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent', 'Number Of Beds']
        ]
         .drop_duplicates()
    )

    print("\nLookup records for Number Of Beds imputation:", beds_reference.shape)    

    # Display sample combinations where multiple Number Of Beds values exist for the same
    # Location Id, Dwelling Type, and Median Rent. These combinations are ambiguous
    # and cannot be used for direct Number Of Beds imputation.

    print("\nSome reference combinations that cannot be used for imputation:")
    print(
        beds_reference
        .groupby(['Location Id', 'Dwelling Type', 'Median Rent'])
        ['Number Of Beds']
        .nunique()
        .reset_index(name='Unique_Bed_Count')
        .query('Unique_Bed_Count > 1')
        .head(10)
    )    

    # Calculate the number of unique Number Of Beds values for each
    # Location Id, Dwelling Type, and Median Rent combination.
    # A Unique_Bed_Count of 1 indicates the combination can be used for imputation.

    temp_df = (
        beds_reference
        .groupby(['Location Id', 'Dwelling Type', 'Median Rent'])
        ['Number Of Beds']
        .nunique()
        .reset_index(name='Unique_Bed_Count')
    )
    
    print("\nReference combinations for Number Of Beds imputation")
    print((temp_df['Unique_Bed_Count'] == 1).sum())

    print("Ambiguous reference combinations:")
    print((temp_df['Unique_Bed_Count'] > 1).sum())    

    # Identify unique combinations with missing Number Of Beds that have a valid Location Id 
    # for imputation.
    print("\nUnique missing combinations for Number Of Beds imputation:")
    print(
        filtered_data[
            (filtered_data['Number Of Beds'].isna()) &
            (filtered_data['Location Id'].notna())
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent']
        ].drop_duplicates().shape
    )

    # Keep a copy of the original Number Of Beds values before imputation.
    filtered_data['Org_Number_Of_Beds'] = filtered_data['Number Of Beds']

    # Loop through records with missing Number Of Beds and a valid Location Id.
    for index, row in filtered_data[
        (filtered_data['Number Of Beds'].isna()) &
        (filtered_data['Location Id'].notna())
        ].iterrows():

        # Find matching reference records using Location Id,
        # Dwelling Type, and Median Rent.
        match = beds_reference[
            (beds_reference['Location Id'] == row['Location Id']) &
            (beds_reference['Dwelling Type'] == row['Dwelling Type']) &
            (beds_reference['Median Rent'] == row['Median Rent'])
            ]

        # Impute Number Of Beds only when exactly one matching
        # reference record is found.
        if len(match) == 1:

            old_value = row['Number Of Beds']
            new_value = match.iloc[0]['Number Of Beds']

            filtered_data.at[index, 'Number Of Beds'] = new_value

            """ print(
                f"Row {index}: Number Of Beds updated "
                f"from {old_value} to {new_value}"
            ) """

    before_impute = filtered_data['Org_Number_Of_Beds'].isna().sum()
    after_impute = filtered_data['Number Of Beds'].isna().sum()

    print("Number Of Beds missing values before imputation:", before_impute)
    print("Number Of Beds missing values after imputation:", after_impute)
    print("Number Of Beds values imputed:", before_impute - after_impute)     

    # Sanity check: Specify the number of imputed records to review.
    rows_to_check = int(input("\nEnter number of updated records to check (0 = show all): "))
    # Identify records where Number Of Beds was updated during imputation.
    updated_records = filtered_data[
        filtered_data['Org_Number_Of_Beds'].fillna('NULL')
            !=
            filtered_data['Number Of Beds'].fillna('NULL')
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent',
            'Org_Number_Of_Beds', 'Number Of Beds']
        ]

    print("Sanity check: Records where Number Of Beds was updated during imputation:")
    if rows_to_check > 0:
        print(updated_records.head(rows_to_check).to_string(index=False))
    else:
        print(updated_records.to_string(index=False))

    print("\nOutliers Detection:")
    numeric_columns = [
        'Total Bonds',
        'Active Bonds',
        'Closed Bonds',
        'Median Rent',
        'Geometric Mean Rent',
        'Upper Quartile Rent',
        'Lower Quartile Rent'
    ]

    for column in numeric_columns:

        Q1 = filtered_data[column].quantile(0.25)
        Q3 = filtered_data[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_count = len(
            filtered_data[
                (filtered_data[column] < lower_bound) |
                (filtered_data[column] > upper_bound)
            ]
        )

        print(
            f"{column} outliers: {outlier_count} "
            f"({round((outlier_count / len(filtered_data)) * 100, 2)}%)"
        )

    
    # Drop the temporary column used for imputation validation.
    filtered_data = filtered_data.drop(columns=['Org_Number_Of_Beds'])

    # Display the final dataset overview and summary statistics after data cleaning.
    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)

    # Return the cleaned rental bond dataset.
    return filtered_data


""" Display dataset overview. """
def display_dataset_overview(df):
    
    print("\nDataset overview")
    print("Dataset shape:", df.shape)
    print(df.dtypes.to_frame("Data Type").join([df.count().rename("Count")
    , df.isnull().sum().rename("Missing Values"), df.nunique().rename("Unique Values")]))  
        
""" Display summary statistics """
def display_summary_statistics(df):
    
    print("\nSummary statistics for all columns")
    print("Summary statistics for numeric data:")
    summ_numeric_data = df.describe(include=[np.number]).T  
    print(summ_numeric_data)
    print("Summary statistics for categorical data:")  
    summ_category_data = df.describe(include=['object', 'category', 'str']).T   
    print(summ_category_data)        


""" Filter dataset by timeframe. """
def filter_timeframe(df):
    
    filtered_df = []  
    """ Rental bond data cleaning for Week 8 """
# Timeframe matched to Deliverable 3 (Christchurch listings) dataset.
# Dropped: overlaps with other rent columns, hard to interpret.
# Impute beds only when Location Id + Dwelling Type + Median Rent
# gives exactly one match (avoids guessing on ambiguous cases).
# [X] of [Y] missing beds imputed; rest left missing (no unique match).
# Outliers flagged (IQR method), not removed — could be real, not errors.
import pandas as pd
import numpy as np

file_path = 'data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv'

""" Clean the rental bond dataset. """
def clean_bond_dataset():

    
    bond_df = pd.read_csv(file_path)


    bond_df['TimeFrame'] = pd.to_datetime(bond_df['TimeFrame'])

    
    filtered_data = filter_timeframe(bond_df)
    
    if (len(filtered_data) == 0):  
        filtered_data = bond_df

    
    print("Duplicate rows:", filtered_data.duplicated().sum())

    print("\nBefore Data Cleaning (After Timeframe Filtering): Rental Bond Dataset")
    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)

    print("\nAfter Data Cleaning (After Timeframe Filtering)")
    
    filtered_data = filtered_data.drop(columns=['Log Std Dev Weekly Rent'])

    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)


    beds_reference = (
        filtered_data[
            (filtered_data['Location Id'].notna()) &
            (filtered_data['Number Of Beds'].notna())
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent', 'Number Of Beds']
        ]
         .drop_duplicates()
    )

    print("\nLookup records for Number Of Beds imputation:", beds_reference.shape)    



    print("\nSome reference combinations that cannot be used for imputation:")
    print(
        beds_reference
        .groupby(['Location Id', 'Dwelling Type', 'Median Rent'])
        ['Number Of Beds']
        .nunique()
        .reset_index(name='Unique_Bed_Count')
        .query('Unique_Bed_Count > 1')
        .head(10)
    )    

    
    temp_df = (
        beds_reference
        .groupby(['Location Id', 'Dwelling Type', 'Median Rent'])
        ['Number Of Beds']
        .nunique()
        .reset_index(name='Unique_Bed_Count')
    )
    
    print("\nReference combinations for Number Of Beds imputation")
    print((temp_df['Unique_Bed_Count'] == 1).sum())

    print("Ambiguous reference combinations:")
    print((temp_df['Unique_Bed_Count'] > 1).sum())    

    
    print("\nUnique missing combinations for Number Of Beds imputation:")
    print(
        filtered_data[
            (filtered_data['Number Of Beds'].isna()) &
            (filtered_data['Location Id'].notna())
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent']
        ].drop_duplicates().shape
    )


    filtered_data['Org_Number_Of_Beds'] = filtered_data['Number Of Beds']

    
    for index, row in filtered_data[
        (filtered_data['Number Of Beds'].isna()) &
        (filtered_data['Location Id'].notna())
        ].iterrows():

        
        match = beds_reference[
            (beds_reference['Location Id'] == row['Location Id']) &
            (beds_reference['Dwelling Type'] == row['Dwelling Type']) &
            (beds_reference['Median Rent'] == row['Median Rent'])
            ]

        
        if len(match) == 1:

            old_value = row['Number Of Beds']
            new_value = match.iloc[0]['Number Of Beds']

            filtered_data.at[index, 'Number Of Beds'] = new_value

            """ print(
                f"Row {index}: Number Of Beds updated "
                f"from {old_value} to {new_value}"
            ) """

    before_impute = filtered_data['Org_Number_Of_Beds'].isna().sum()
    after_impute = filtered_data['Number Of Beds'].isna().sum()

    print("Number Of Beds missing values before imputation:", before_impute)
    print("Number Of Beds missing values after imputation:", after_impute)
    print("Number Of Beds values imputed:", before_impute - after_impute)     

    
    rows_to_check = int(input("\nEnter number of updated records to check (0 = show all): "))
    
    updated_records = filtered_data[
        filtered_data['Org_Number_Of_Beds'].fillna('NULL')
            !=
            filtered_data['Number Of Beds'].fillna('NULL')
        ][
            ['Location Id', 'Dwelling Type', 'Median Rent',
            'Org_Number_Of_Beds', 'Number Of Beds']
        ]

    print("Sanity check: Records where Number Of Beds was updated during imputation:")
    if rows_to_check > 0:
        print(updated_records.head(rows_to_check).to_string(index=False))
    else:
        print(updated_records.to_string(index=False))

    print("\nOutliers Detection:")
    numeric_columns = [
        'Total Bonds',
        'Active Bonds',
        'Closed Bonds',
        'Median Rent',
        'Geometric Mean Rent',
        'Upper Quartile Rent',
        'Lower Quartile Rent'
    ]

    for column in numeric_columns:

        Q1 = filtered_data[column].quantile(0.25)
        Q3 = filtered_data[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_count = len(
            filtered_data[
                (filtered_data[column] < lower_bound) |
                (filtered_data[column] > upper_bound)
            ]
        )

        print(
            f"{column} outliers: {outlier_count} "
            f"({round((outlier_count / len(filtered_data)) * 100, 2)}%)"
        )

    
    
    filtered_data = filtered_data.drop(columns=['Org_Number_Of_Beds'])

    
    display_dataset_overview(filtered_data)
    display_summary_statistics(filtered_data)

    
    filtered_data.to_csv("data/bond_data_clean.csv.gz", index=False, compression="gzip")
    print("\nSaved cleaned dataset to data/bond_data_clean.csv.gz")

    
    return filtered_data


""" Display dataset overview. """
def display_dataset_overview(df):
    
    print("\nDataset overview")
    print("Dataset shape:", df.shape)
    print(df.dtypes.to_frame("Data Type").join([df.count().rename("Count")
    , df.isnull().sum().rename("Missing Values"), df.nunique().rename("Unique Values")]))  
        
""" Display summary statistics """
def display_summary_statistics(df):
    
    print("\nSummary statistics for all columns")
    print("Summary statistics for numeric data:")
    summ_numeric_data = df.describe(include=[np.number]).T  
    print(summ_numeric_data)
    print("Summary statistics for categorical data:")  
    summ_category_data = df.describe(include=['object', 'category', 'str']).T   
    print(summ_category_data)        


""" Filter dataset by timeframe. """
def filter_timeframe(df):
    
    START_DATE = pd.Timestamp('2025-10-01')
    END_DATE = pd.Timestamp('2026-04-30')

    filtered_df = df[
        (df['TimeFrame'] >= START_DATE) &
        (df['TimeFrame'] <= END_DATE)
    ].copy()

    print(
        f"\nTimeframe filter: kept {len(filtered_df):,} of {len(df):,} rows "
        f"({START_DATE.date()} to {END_DATE.date()})"
    )

    return filtered_df


""" Start data cleaning process. """
clean_bond_dataset()

