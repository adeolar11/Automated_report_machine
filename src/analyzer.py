import pandas as pd


# ---------------------------------
# RECENT WEEK
# ---------------------------------

def get_recent_week(df):

    end_date = df["Order_Date"].max()

    start_date = (
        end_date - pd.Timedelta(days=6)
    )

    recent_week = df[
        (df["Order_Date"] >= start_date)
        &
        (df["Order_Date"] <= end_date)
    ].copy()

    return recent_week


# ---------------------------------
# BUSINESS METRICS
# ---------------------------------

def calculate_metrics(df):

    total_revenue = df["Revenue"].sum()

    total_orders = len(df)

    total_quantity = df["Quantity"].sum()

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    top_region = (
        df.groupby("Country")["Revenue"]
        .sum()
        .idxmax()
        if not df.empty
        else "N/A"
    )

    top_product = (
        df.groupby("Product_Name")["Quantity"]
        .sum()
        .idxmax()
        if not df.empty
        else "N/A"
    )

    holiday_revenue = df.loc[
        df["is_holiday"],
        "Revenue"
    ].sum()

    non_holiday_revenue = df.loc[
        ~df["is_holiday"],
        "Revenue"
    ].sum()

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "top_region": top_region,
        "top_product": top_product,
        "holiday_revenue": holiday_revenue,
        "non_holiday_revenue": non_holiday_revenue
    }


# ---------------------------------
# CATEGORY SALES
# ---------------------------------

def revenue_by_category(df):

    return (
        df.groupby("Product_Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )


# ---------------------------------
# TOP PRODUCTS
# ---------------------------------

def top_products(df, n=5):

    return (
        df.groupby("Product_Name")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


# ---------------------------------
# DAILY REVENUE
# ---------------------------------

def daily_revenue(df):

    return (
        df.groupby(
            df["Order_Date"].dt.floor("D")
        )["Revenue"]
        .sum()
        .sort_index()
    )


# ---------------------------------
# DAY OF WEEK SALES
# ---------------------------------

def sales_by_day_of_week(df):

    order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    result = (
        df.groupby(
            df["Order_Date"].dt.day_name()
        )["Revenue"]
        .sum()
    )

    return result.reindex(order)