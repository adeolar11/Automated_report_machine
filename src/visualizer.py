import os
import matplotlib.pyplot as plt

from .config import COLORS, CHART_DIR
from .analyzer import (
    revenue_by_category,
    top_products,
    daily_revenue,
    sales_by_day_of_week
)


plt.style.use("seaborn-v0_8-whitegrid")


def create_report_charts(df):

    os.makedirs(
        CHART_DIR,
        exist_ok=True
    )

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(16, 10)
    )

    fig.suptitle(
        "WEEKLY SALES PERFORMANCE REPORT",
        fontsize=18,
        fontweight="bold"
    )

    # ---------------------------------
    # CHART 1
    # ---------------------------------

    category_data = revenue_by_category(df)

    axes[0, 0].barh(
        category_data.index,
        category_data.values,
        color=COLORS
    )

    axes[0, 0].set_title(
        "Revenue by Product Category"
    )

    axes[0, 0].set_xlabel(
        "Revenue ($)"
    )

    axes[0, 0].invert_yaxis()


    # ---------------------------------
    # CHART 2
    # ---------------------------------

    product_data = top_products(df)

    axes[0, 1].barh(
        product_data.index,
        product_data.values,
        color=COLORS[2]
    )

    axes[0, 1].set_title(
        "Top 5 Products"
    )

    axes[0, 1].set_xlabel(
        "Quantity Sold"
    )

    axes[0, 1].invert_yaxis()


    # ---------------------------------
    # CHART 3
    # ---------------------------------

    daily = daily_revenue(df)

    axes[0, 2].plot(
        daily.index,
        daily.values,
        marker="o",
        linewidth=2
    )

    axes[0, 2].set_title(
        "Daily Revenue Trend"
    )

    axes[0, 2].set_xlabel("Date")

    axes[0, 2].set_ylabel(
        "Revenue ($)"
    )

    axes[0, 2].tick_params(
        axis="x",
        rotation=45
    )


    # ---------------------------------
    # HOLIDAY SALES
    # ---------------------------------

    holiday_days = (
        df[df["is_holiday"]]
        .groupby(
            df.loc[
                df["is_holiday"],
                "Order_Date"
            ].dt.floor("D")
        )["Revenue"]
        .sum()
    )

    if not holiday_days.empty:

        axes[0, 2].scatter(
            holiday_days.index,
            holiday_days.values,
            color="red",
            s=60,
            label="Holiday"
        )

        axes[0, 2].legend()


    # ---------------------------------
    # CHART 4
    # ---------------------------------

    holiday_revenue = df.loc[
        df["is_holiday"],
        "Revenue"
    ].sum()

    non_holiday_revenue = df.loc[
        ~df["is_holiday"],
        "Revenue"
    ].sum()

    axes[1, 0].bar(
        ["Non-Holiday", "Holiday"],
        [
            non_holiday_revenue,
            holiday_revenue
        ]
    )

    axes[1, 0].set_title(
        "Holiday vs Non-Holiday Revenue"
    )

    axes[1, 0].set_ylabel(
        "Revenue ($)"
    )


    # ---------------------------------
    # CHART 5
    # ---------------------------------

    avg = (
        df.groupby("Quantity")["Revenue"]
        .mean()
    )

    axes[1, 1].plot(
        avg.index,
        avg.values,
        marker="o"
    )

    axes[1, 1].set_title(
        "Average Revenue by Order Size"
    )

    axes[1, 1].set_xlabel(
        "Quantity"
    )

    axes[1, 1].set_ylabel(
        "Average Revenue ($)"
    )


    # ---------------------------------
    # CHART 6 - KPI
    # ---------------------------------

    total_revenue = df["Revenue"].sum()

    total_orders = len(df)

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    top_region = (
        df.groupby("Country")["Revenue"]
        .sum()
        .idxmax()
    )

    top_product = (
        df.groupby("Product_Name")["Quantity"]
        .sum()
        .idxmax()
    )

    holiday_revenue = df.loc[
        df["is_holiday"],
        "Revenue"
    ].sum()

    non_holiday_revenue = df.loc[
        ~df["is_holiday"],
        "Revenue"
    ].sum()

    axes[1, 2].axis("off")

    summary = f"""
TOTAL REVENUE
${total_revenue:,.2f}

TOTAL ORDERS
{total_orders:,}

AVERAGE ORDER VALUE
${avg_order_value:,.2f}

TOP REGION
{top_region}

TOP PRODUCT
{top_product}

HOLIDAY REVENUE
${holiday_revenue:,.2f}

NON-HOLIDAY REVENUE
${non_holiday_revenue:,.2f}
"""

    axes[1, 2].text(
        0.05,
        0.5,
        summary,
        fontsize=11,
        verticalalignment="center",
        bbox=dict(
            facecolor="lightgrey",
            edgecolor="black",
            boxstyle="round,pad=1"
        )
    )


    # ---------------------------------
    # SAVE
    # ---------------------------------

    plt.tight_layout(
        rect=[0, 0, 1, 0.96]
    )

    output_path = os.path.join(
        CHART_DIR,
        "weekly_report.png"
    )

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    return output_path