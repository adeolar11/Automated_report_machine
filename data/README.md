# Data Folder

This folder contains the input datasets used by the automated reporting system.

## Required File

The main input file should be:

`ecommerce_retail_transactions_raw.csv`

## Expected Columns

The dataset should contain the following columns:

- Order_ID
- Order_Date
- Product_Name
- Product_Category
- Quantity
- Unit_Price_USD
- Discount_Percent
- Customer_Rating
- Payment_Method
- Country

## Notes

The reporting system automatically:

1. Loads the CSV file.
2. Cleans dates.
3. Removes duplicate records.
4. Handles missing numerical values.
5. Standardises country names.
6. Calculates Revenue.
7. Fetches public holidays using the Nager.Date API.
8. Matches holidays based on country and date.