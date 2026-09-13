# DATA201-DATA422 Data Wrangling Project - Group 6

## Dataset 1

**Source:** https://insideairbnb.com/get-the-data/ New Zealand, 19th of June 2026

**Number of rows:** 50932 without the header\
**Number of columns:** 18\
**Column 1:** id --> id of the listing\
**Column 2:** name --> AirBnB name on the listing\
**Column 3:** host_id\
**Column 4:** host_name\
**Column 5:** neighbourhood_group --> city district\
**Column 6:** neighbourhood --> actual neighbourhood\
**Column 7:** latitude\
**Column 8:** longitude\
**Column 9:** room_type --> entire home or just private room\
**Column 10:** price\
**Column 11:** minimum_nights\
**Column 12:** number_of_reviews\
**Column 13:** last_review\
**Column 14:** reviews_per_month\
**Column 15:** calculated_host_listings_count --> how many listings the host has\
**Column 16:** availability_365 --> when is it available\
**Column 17:** number_of_reviews_ltm --> number of reviews in the last 12 month\
**Column 18:** license --> permit/registration number

## Dataset 2

**Source:** [Tenancy Services – Rental Bond Data](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/)

**Number of rows:** 226080 without the header\
**Number of columns:** 12\
| `TimeFrame` | The quarter summarised, based on tenancy start date. |\
| `Location Id` | Geographic area code. Per the source, area definitions use the SA2-2019 classification from Statistics NZ. |\
| `Dwelling Type` | Type of rental property (ALL, House, Apartment, Boarding house, Flat). |\
| `Number Of Beds` | Bedroom count category. |\
| `Total Bonds` | Total number of bonds lodged for that group. |\
| `Active Bonds` | Number of tenancies still ongoing. |\
| `Closed Bonds` | Number of tenancies that have ended. |\
| `Median Rent` | Middle weekly rent value for the group. |\
| `Geometric Mean Rent` | Alternative measure to the median, used because rents cluster at round numbers, which can make plain medians plateau over time. |\
| `Upper Quartile Rent` | Synthetic 75th-percentile rent, modelled assuming a log-normal rent distribution. |\
| `Lower Quartile Rent` | Synthetic 25th-percentile rent, calculated the same way. |\
| `Log Std Dev Weekly Rent` | Standard deviation of the log of weekly rent, indicating how spread out rents are within the group. |\
## Bond Dataset Cleaning

- **Timeframe:** [START_DATE]–[END_DATE], matched to Deliverable 3 dataset. Kept [X]/[Y] rows.
- **Dropped:** `Log Std Dev Weekly Rent` (redundant with other rent columns).
- **Imputed:** `Number Of Beds`, using Location Id + Dwelling Type + Median Rent matches ([X] imputed, [W] left missing — no unique match).
- **Duplicates:** [N] found, [kept/dropped].
- **Outliers:** Flagged via IQR, not removed (may be genuine).
- **Kept:** `Location Id`, `TimeFrame` (for next week's merge).
