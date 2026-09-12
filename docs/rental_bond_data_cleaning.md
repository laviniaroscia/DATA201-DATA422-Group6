# Rental Bond Data Cleaning

## Duplicate Records
Duplicate records were checked across all columns in the dataset.
Result:
- Duplicate rows found: 0
No duplicate records were identified; therefore, no duplicate rows were removed.

## Drop Log Std Dev Weekly Rent
Dropped Log Std Dev Weekly Rent as it is difficult to interpret from a business
perspective and provides limited information compared with other rent metrics.

## Missing Location Id
94 records out of a total of 27,212 with missing Location Id were retained
because they represent only 0.35% of the dataset. These records also have missing
values in Median Rent, Geometric Mean Rent, Upper Quartile Rent, and Lower
Quartile Rent. However, they still contain valid information in Dwelling Type,
Number Of Beds, Total Bonds, Active Bonds, and Closed Bonds.

## Number Of Beds Imputation

### Create Reference Records
A reference table was created using records with valid Location Id and Number Of Beds. This table is used to identify matching Number Of Beds values based on Location Id, Dwelling Type, and Median Rent for imputation purposes.

### Validate Reference Combinations
Calculate the number of unique Number Of Beds values for each Location Id, Dwelling Type, and Median Rent combination.
- Unique_Bed_Count = 1 indicates the combination can be used as a reference for imputation.
- Unique_Bed_Count > 1 indicates the combination cannot be used as a reference for imputation.

### Identify Missing Combinations
Identify unique combinations with missing Number Of Beds that have a valid
Location Id for imputation.

### Perform Imputation
- Keep a copy of the original Number Of Beds values before imputation.
- Loop through records with missing Number Of Beds and a valid Location Id.
- Find matching reference records using Location Id, Dwelling Type, and Median Rent.
- Impute Number Of Beds only when exactly one matching reference record is found.

### Results
- Missing Number Of Beds before imputation: 890
- Missing Number Of Beds after imputation: 722
- Number Of Beds values imputed: 168

### Sanity Check
Displayed records where Number Of Beds was updated during imputation by comparing the original values stored in Org_Number_Of_Beds with the imputed values in Number Of Beds.

## Outlier Detection
Potential outliers were identified using the IQR (Interquartile Range) method across the numerical variables.

Outlier percentages ranged from 4.14% to 7.89% of the dataset.
As the dataset contains rental bond and rent information, extreme values may represent genuine observations rather than data quality issues. Therefore, the identified outliers were retained in the dataset.

### Clean Up
The temporary column Org_Number_Of_Beds, created to preserve the original values
of Number Of Beds for validation and sanity checking during imputation, was
dropped after the imputation process was verified.