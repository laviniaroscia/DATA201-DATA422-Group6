# Design Principles Document: Data Filtering Pipeline

*This document was generated with AI assistance from GitHub Copilot.*

## 1. Inputs to the Pipeline

The pipeline reads nine CSV files using the following file-to-month mapping:

| CSV file | Month-Year value |
|---|---|
| `data/Oct2025.csv` | October 2025 |
| `data/Nov2025.csv` | November 2025 |
| `data/Dec2025.csv` | December 2025 |
| `data/Jan2026.csv` | January 2026 |
| `data/Feb2026.csv` | February 2026 |
| `data/Mar2026.csv` | March 2026 |
| `data/Apr2026.csv` | April 2026 |
| `data/May2026.csv` | May 2026 |
| `data/Jun2026.csv` | June 2026 |

## 2. Outputs from the Pipeline

The pipeline produces `filtered_dataset.csv` in the `out` directory. It contains Christchurch City records from October 2025 to June 2026, with a `date` column identifying each month's data.

## 3. Main Steps in the Pipeline

The pipeline iterates through the `files_dates` mapping, which links each monthly CSV file to its corresponding Month-Year label. For each file, it reads the data, retains records where `neighbourhood_group` is `Christchurch City`, adds a `date` column using that file's label, and appends the filtered records to a list. After all nine files have been processed, the combined dataset is saved to `output_csv`, which points to `filtered_dataset.csv` in the `out` directory.

## 4. Coding and Software Strategies

The coding strategy is to organize imports, inputs, and outputs as distinct parts. In `data_filtering.py`, pandas is imported for CSV handling; `files_dates` pairs each input CSV path with its Month-Year label; and `output_csv` specifies `filtered_dataset.csv` in the `out` directory. This follows the "no magic numbers" principle from Week 9 lecture, which recommends defining parameters with clear names near the top of a file rather than hardcoding values inline.
