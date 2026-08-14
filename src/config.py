import os

# ---------------------------------
# BASE DIRECTORIES
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")


# ---------------------------------
# FILE PATHS
# ---------------------------------

DATA_FILE = os.path.join(
    DATA_DIR,
    "ecommerce_retail_transactions_raw.csv"
)


# ---------------------------------
# API SETTINGS
# ---------------------------------

HOLIDAY_API_URL = "https://date.nager.at/api/v3/PublicHolidays"


# Country codes used by the holiday API
COUNTRY_CODES = {
    "Canada": "CA",
    "United States": "US",
    "India": "IN",
    "U.A.E": "AE",
    "Germany": "DE",
    "United Kingdom": "GB",
    "Australia": "AU"
}


# ---------------------------------
# EMAIL SETTINGS
# ---------------------------------

ENV_FILE = os.path.join(BASE_DIR, ".env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

RECIPIENTS = os.getenv("RECIPIENTS", "")


# ---------------------------------
# CHART SETTINGS
# ---------------------------------

COLORS = [
    "#2C3E50",
    "#E74C3C",
    "#3498DB",
    "#2ECC71",
    "#F39C12"
]