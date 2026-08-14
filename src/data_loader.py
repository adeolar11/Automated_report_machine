import pandas as pd
import urllib.request
import json

from .config import DATA_FILE, HOLIDAY_API_URL, COUNTRY_CODES


# ---------------------------------
# LOAD CSV
# ---------------------------------

def load_data(file_path=DATA_FILE):

    print(f"Attempting to load file from: {file_path}")

    try:
        df = pd.read_csv(file_path)

        print(f"Loaded {len(df)} rows of sales data")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Error loading dataset: {error}"
        )


# ---------------------------------
# CLEAN DATES
# ---------------------------------

def clean_dates(df):

    if "Order_Date" not in df.columns:
        raise KeyError(
            "Order_Date column is missing."
        )

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Order_Date"]
    ).copy()

    return df


# ---------------------------------
# REMOVE DUPLICATES
# ---------------------------------

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates().copy()

    removed = before - len(df)

    print(f"Removed {removed} duplicate rows")

    return df


# ---------------------------------
# FILL MISSING VALUES
# ---------------------------------

def fill_median_by_group(
    df,
    column,
    group_col
):

    if column not in df.columns:
        return df

    if group_col not in df.columns:
        return df

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = (
        df.groupby(group_col)[column]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )

    return df


# ---------------------------------
# PAYMENT METHOD
# ---------------------------------

def clean_payment_method(df):

    if "Payment_Method" not in df.columns:
        return df

    df["Payment_Method"] = (
        df["Payment_Method"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["Payment_Method"] = df[
        "Payment_Method"
    ].replace(
        to_replace=r"(?i)^upi$",
        value="U.P.I",
        regex=True
    )

    return df


# ---------------------------------
# COUNTRY CLEANING
# ---------------------------------

def clean_country_names(df):

    if "Country" not in df.columns:
        return df

    df["Country"] = (
        df["Country"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    country_key = (
        df["Country"]
        .str.replace(
            r"[\.\-\s]",
            "",
            regex=True
        )
    )

    country_mapping = {

        "CA": "Canada",
        "CAN": "Canada",
        "CANADA": "Canada",

        "AU": "Australia",
        "AUS": "Australia",
        "AUSTRALIA": "Australia",

        "US": "United States",
        "USA": "United States",
        "UNITEDSTATES": "United States",

        "DE": "Germany",
        "DEU": "Germany",
        "GERMANY": "Germany",

        "UK": "United Kingdom",
        "GB": "United Kingdom",
        "GBR": "United Kingdom",
        "UNITEDKINGDOM": "United Kingdom",

        "IN": "India",
        "IND": "India",
        "INDIA": "India",

        "AE": "U.A.E",
        "ARE": "U.A.E",
        "UAE": "U.A.E",
        "UNITEDARABEMIRATES": "U.A.E"
    }

    df["Country"] = (
        country_key
        .map(country_mapping)
        .fillna(
            df["Country"].str.title()
        )
    )

    return df


# ---------------------------------
# REVENUE
# ---------------------------------

def calculate_revenue(df):

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["Unit_Price_USD"] = pd.to_numeric(
        df["Unit_Price_USD"],
        errors="coerce"
    )

    df["Revenue"] = (
        df["Quantity"]
        * df["Unit_Price_USD"]
    )

    return df


# ---------------------------------
# FETCH HOLIDAYS
# ---------------------------------

def fetch_holidays(
    year,
    country_code
):

    url = (
        f"{HOLIDAY_API_URL}/"
        f"{year}/"
        f"{country_code}"
    )

    try:

        with urllib.request.urlopen(
            url,
            timeout=30
        ) as response:

            data = response.read()

        return json.loads(
            data.decode("utf-8")
        )

    except Exception as error:

        print(
            f"Holiday API error "
            f"for {country_code} {year}: "
            f"{error}"
        )

        return []


# ---------------------------------
# FETCH ALL HOLIDAYS
# ---------------------------------

def fetch_all_holidays(df):

    all_holidays = []

    countries = (
        df["Country"]
        .dropna()
        .unique()
    )

    years = (
        df["Order_Date"]
        .dt.year
        .dropna()
        .unique()
    )

    for country in countries:

        country_code = COUNTRY_CODES.get(
            country
        )

        if not country_code:

            print(
                f"No country code found for {country}"
            )

            continue

        for year in years:

            print(
                f"Fetching holidays: "
                f"{country} - {year}"
            )

            holidays = fetch_holidays(
                int(year),
                country_code
            )

            for holiday in holidays:

                all_holidays.append({
                    "date": holiday.get("date"),
                    "Country": country,
                    "localName": holiday.get(
                        "localName"
                    )
                })

    return pd.DataFrame(
        all_holidays
    )


# ---------------------------------
# MERGE HOLIDAYS
# ---------------------------------

def merge_holidays(
    df,
    df_holidays
):

    if df_holidays.empty:

        df["is_holiday"] = False
        df["localName"] = None

        return df

    df_holidays["date"] = pd.to_datetime(
        df_holidays["date"],
        errors="coerce"
    )

    df_holidays = df_holidays.dropna(
        subset=["date"]
    )

    df = df.merge(
        df_holidays,
        how="left",
        left_on=[
            "Order_Date",
            "Country"
        ],
        right_on=[
            "date",
            "Country"
        ]
    )

    df["is_holiday"] = (
        df["localName"].notna()
    )

    df = df.drop(
        columns=["date"],
        errors="ignore"
    )

    return df


# ---------------------------------
# COMPLETE DATA PREPARATION
# ---------------------------------

def prepare_data():

    df = load_data()

    df = clean_dates(df)

    df = remove_duplicates(df)

    df = fill_median_by_group(
        df,
        "Quantity",
        "Product_Name"
    )

    df = fill_median_by_group(
        df,
        "Discount_Percent",
        "Product_Name"
    )

    df = fill_median_by_group(
        df,
        "Customer_Rating",
        "Product_Name"
    )

    df = clean_payment_method(df)

    df = clean_country_names(df)

    df = calculate_revenue(df)

    print("Fetching holidays...")

    holidays = fetch_all_holidays(df)

    df = merge_holidays(
        df,
        holidays
    )

    df = remove_duplicates(df)

    return df