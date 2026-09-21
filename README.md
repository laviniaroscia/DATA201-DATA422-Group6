# DATA201-DATA422 Data Wrangling Project - Group 6

This project combines Airbnb listing data with New Zealand Rental Bond data
to compare short-term and long-term rental patterns across Christchurch.

The analysis focuses on rental prices, geographic differences, and the number
of properties available in different Statistical Area 2 (SA2) locations.

---

## Dataset 1 — Airbnb Listings

**Source:** [Inside Airbnb](https://insideairbnb.com/get-the-data/)  
**Location:** Christchurch, New Zealand  
**Dataset date:** 19 June 2026  
**Original size:** 50,932 rows × 18 columns

| Column | Description |
|---|---|
| `id` | Unique Airbnb listing identifier |
| `name` | Listing name |
| `host_id` | Unique host identifier |
| `host_name` | Host name |
| `neighbourhood_group` | Higher-level geographic grouping |
| `neighbourhood` | Neighbourhood of the listing |
| `latitude` | Listing latitude |
| `longitude` | Listing longitude |
| `room_type` | Type of accommodation, such as entire home or private room |
| `price` | Airbnb nightly price |
| `minimum_nights` | Minimum number of nights required for a booking |
| `number_of_reviews` | Total number of reviews |
| `last_review` | Date of the most recent review |
| `reviews_per_month` | Average number of reviews per month |
| `calculated_host_listings_count` | Number of listings associated with the host |
| `availability_365` | Number of days available during the next 365 days |
| `number_of_reviews_ltm` | Number of reviews in the last 12 months |
| `license` | Permit or registration information |

---

## Airbnb Data Cleaning

The Airbnb dataset had already been filtered to Christchurch before the main
analysis. The cleaning process focused on retaining variables relevant to
rental price, availability, property type, and geographic analysis.

### Removed columns

The following columns were removed because they were not required for the
planned analysis:

- `name`
- `host_name`
- `neighbourhood_group`
- `last_review`
- `reviews_per_month`
- `number_of_reviews_ltm`
- `license`

`neighbourhood_group` was removed because the dataset had already been filtered
to Christchurch, so it did not provide useful additional geographic variation.

Latitude and longitude were retained for geographic matching.

### Missing values

Most retained variables contained no missing values.

The main exceptions were:

- `price`: 10,667 missing values
- `minimum_nights`: 37 missing values

Rows with missing prices were retained because a listing may still be useful
when analysing the number and geographic distribution of Airbnb properties.
Missing prices are excluded only when a price-specific analysis is performed.

The small number of missing `minimum_nights` values was also retained because
this variable was not required for every analysis.

### Duplicate checks

No completely duplicated rows were found.

Although some Airbnb `id` values appeared multiple times, this was expected
because the dataset contains observations from multiple dates.

The combination of `id` and `date` was checked and no duplicate
`id`–`date` records were found.

### Invalid values and outliers

The following checks were performed:

- `availability_365` was confirmed to fall between 0 and 365
- `minimum_nights` contained no values below 1
- `price` contained no zero or negative values
- latitude and longitude values were retained for geographic analysis

Airbnb prices contained several extreme values. These observations were
retained because there was no objective threshold for identifying them as
incorrect records.

For later price comparisons, median values were therefore preferred over means
where appropriate because they are less sensitive to extreme prices.

---

## Dataset 2 — Rental Bond Data

**Source:** [Tenancy Services — Rental Bond Data](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/)  
**Original size:** 226,080 rows × 12 columns

| Column | Description |
|---|---|
| `TimeFrame` | Quarter summarised, based on tenancy start date |
| `Location Id` | SA2 geographic area identifier |
| `Dwelling Type` | Rental property category such as house, apartment, flat, or boarding house |
| `Number Of Beds` | Bedroom-count category |
| `Total Bonds` | Number of tenancies opened during the timeframe |
| `Active Bonds` | Number of tenancies still active |
| `Closed Bonds` | Number of tenancies that have ended |
| `Median Rent` | Median weekly rent for the group |
| `Geometric Mean Rent` | Alternative rental-price measure using the geometric mean |
| `Upper Quartile Rent` | Estimated 75th-percentile weekly rent |
| `Lower Quartile Rent` | Estimated 25th-percentile weekly rent |
| `Log Std Dev Weekly Rent` | Measure of the spread of weekly rental prices |

---

## Rental Bond Data Cleaning

### Initial dataset

The original Rental Bond dataset contained:

- **226,080 rows**
- **12 columns**

### Data types

`TimeFrame` was converted from a string to a datetime value so that the dataset
could be filtered and aligned with the Airbnb observation periods.

### Timeframe filtering

Only the period relevant to the Airbnb analysis was retained:

**1 October 2025 to 30 April 2026**

This reduced the dataset from:

**226,080 rows → 27,212 rows**

All 12 columns were retained because they contained potentially useful
information for rental-price and property-count analyses.

### Duplicate records

Duplicate rows were checked across all columns.

**Duplicate rows found: 0**

No records were removed as duplicates.

### Missing `Location Id`

There were **94 rows** with missing `Location Id`, representing approximately
**0.35%** of the filtered dataset.

These rows were retained because they still contained useful information for:

- `Dwelling Type`
- `Number Of Beds`
- `Total Bonds`
- `Active Bonds`
- `Closed Bonds`

The same records also contained missing rent statistics, including `Median Rent`,
`Geometric Mean Rent`, `Upper Quartile Rent`, and `Lower Quartile Rent`.

### `Number Of Beds` imputation

The dataset initially contained **890 missing values** in `Number Of Beds`.

A reference table was created from records containing valid values for:

- `Location Id`
- `Dwelling Type`
- `Median Rent`
- `Number Of Beds`

For each combination of `Location Id`, `Dwelling Type`, and `Median Rent`, the
number of unique bedroom categories was checked.

A missing `Number Of Beds` value was imputed only when the matching combination
mapped to exactly one bedroom category.

#### Imputation results

- Missing before imputation: **890**
- Values successfully imputed: **168**
- Missing after imputation: **722**

The original values were temporarily preserved in `Org_Number_Of_Beds` so that
the imputed records could be validated. This temporary column was removed after
the validation was completed.

### Invalid values

No negative values were found in the bond-count or rental-price variables.

`Total Bonds`, `Active Bonds`, and `Closed Bonds` were not directly compared as
a consistency rule because they represent different aspects of bond activity.

### Outlier detection

Potential outliers in the numerical variables were identified using the
Interquartile Range (IQR) method.

Depending on the variable, approximately **4.14% to 7.89%** of observations were
identified as potential outliers.

These observations were retained because high bond counts or rental prices may
represent genuine characteristics of particular areas rather than data errors.

### Cleaned output

After the cleaning and validation steps were completed, the processed Rental
Bond dataset was saved for use in the subsequent analyses.

---

## Median Airbnb Price in Christchurch Central

Christchurch Central was identified using **Location ID 326600**.

The Airbnb dataset was filtered using the corresponding `area_code`, and the
median listing price was calculated from the `price` column.

**Median Airbnb price in Christchurch Central: $239.00 per night**

The median was used rather than the mean because Airbnb prices can contain
extreme values that may distort the average.

---

## Short-term vs Long-term Rental Price Gap

To compare short-term and long-term rental prices, Airbnb listings with a
`minimum_nights` value of 7 or less were treated as short-term rentals.

The weekly median rent from the rental bond dataset was converted to a nightly
price:

`long-term nightly price = Median Rent / 7`

The rental price gap was then calculated as:

`price gap = Airbnb nightly price - long-term nightly price`

To reduce the influence of extreme Airbnb price outliers, the median price gap
was calculated for each area. Only areas with at least 10 unique listings were
included.

The largest median gap was observed in **Sumner**, with a median short-term
premium of approximately **$196 per night** across **78 listings**.

The next largest gaps were observed in:
- **Malvern:** ~$170 per night
- **Christchurch Central-West:** ~$158 per night
- **Addington North:** ~$157 per night
- **Christchurch Central:** ~$153 per night

![Median rental price gap by area](images/rental_price_gap_by_area.png)

---

## Number of Airbnb vs Long-Term Rental Properties for each location

To compare the number of Airbnb and long-term rental properties across Christchurch, the Airbnb and Rental Bond datasets were aligned by geographic area and quarter.

Airbnb monthly observations were converted to quarter start dates so they could be matched with the quarterly `TimeFrame` values in the Rental Bond dataset.

For Airbnb listings, the number of unique `id` values was counted for each area and quarter.

For long-term rentals, the Rental Bond dataset was filtered to:

- `Dwelling Type = ALL`
- `Number Of Beds = ALL`

The `Active Bonds` value was then used as the number of active long-term rental tenancies for each area.

The geographic match was performed using:

- Airbnb `area_code`
- Rental Bond `Location Id`

The comparison was carried out separately for each quarter to avoid mixing observations from different time periods.

The latest available quarter was **April–June 2026**.

![Airbnb vs Long-Term Rental Properties](images/airbnb_vs_long_term_properties.png)