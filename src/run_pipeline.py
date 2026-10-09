""" Run the complete data wrangling and analysis pipeline. """

from importlib import import_module

filter_airbnb_data = import_module("01_data_filtering").filter_airbnb_data
clean_airbnb_data = import_module("02_clean_filtered_dataset_chch").clean_airbnb_data
clean_bond_dataset = import_module("03_rental_bond_data_cleaning").clean_bond_dataset
run_airbnb_analysis = import_module("04_airbnb_analysis").run_airbnb_analysis
add_area_codes = import_module("05_get_area_codes").add_area_codes
run_rental_analysis = import_module("08_rental_analysis").run_rental_analysis
run_location_comparison = import_module("09_compare_location").run_location_comparison
run_median_price_analysis = import_module("07_median_price").run_median_price_analysis


def run_pipeline():
    ''' Run the complete pipeline '''

    print("\n========================================")
    print("STARTING DATA WRANGLING PIPELINE")
    print("========================================")

    # 1. Filter monthly Airbnb datasets
    print("\n========================================")
    print("[1/8] Filtering Airbnb data...")
    print("========================================")
    filter_airbnb_data()

    # 2. Clean Christchurch Airbnb dataset
    print("\n========================================")
    print("[2/8] Cleaning Airbnb data...")
    print("========================================")
    clean_airbnb_data()

    # 3. Clean rental bond dataset
    print("\n========================================")
    print("[3/8] Cleaning rental bond data...")
    print("========================================")
    clean_bond_dataset()

    # 4. Run Airbnb analysis
    print("\n========================================")
    print("[4/8] Running Airbnb analysis...")
    print("========================================")
    run_airbnb_analysis()

    # 5. Add SA2 area codes
    print("\n========================================")
    print("[5/8] Adding SA2 area codes...")
    print("========================================")
    add_area_codes()

    # 6. Calculate median Airbnb price in Christchurch Central
    print("\n========================================")
    print("[6/8] Calculating Christchurch Central median price...")
    print("========================================")
    run_median_price_analysis()

    # 7. Analyse Airbnb vs long-term rental prices
    print("\n========================================")
    print("[7/8] Running rental price analysis...")
    print("========================================")
    run_rental_analysis()

    # 8. Compare Airbnb and long-term rental properties
    print("\n========================================")
    print("[8/8] Comparing property counts for each location...")
    print("========================================")
    run_location_comparison()

    print("\n========================================")
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("========================================")


if __name__ == "__main__":
    run_pipeline()