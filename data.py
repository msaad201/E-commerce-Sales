from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "Mid_project_amazon_sales_cleaned.parquet"
REQUIRED_COLUMNS = {
    "Product_Name",
    "rating",
    "number_of_reviews",
    "Revenue_last_month",
    "Price_after_Discount",
    "listed_price",
    "is_sponsored",
    "is_couponed",
    "is_available",
    "delivery",
    "image_url",
    "product_url",
    "Order_Placed",
    "Dicount_percentage_(%)",
    "Best_seller",
    "delivery_days",
}
CATEGORICAL_COLUMNS = (
    "Product_Name",
    "is_sponsored",
    "is_couponed",
    "is_available",
    "delivery",
    "Best_seller",
)


@st.cache_data(show_spinner="Loading Amazon product data...")
def load_data() -> pd.DataFrame:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Could not find the cleaned dataset: {DATA_PATH}")

    products = pd.read_parquet(DATA_PATH)
    missing_columns = sorted(REQUIRED_COLUMNS.difference(products.columns))
    if missing_columns:
        raise ValueError(
            "The cleaned dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    products = products.copy()
    products["Order_Placed"] = pd.to_datetime(products["Order_Placed"], errors="coerce")
    for column in CATEGORICAL_COLUMNS:
        products[column] = (
            products[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
            .fillna("Unknown")
        )

    return products


def filter_by_shared_controls(products: pd.DataFrame) -> pd.DataFrame:
    if products.empty:
        return products

    st.sidebar.markdown("### Shared filters")
    filtered = products
    filter_columns = (
        ("Delivery", "delivery"),
        ("Sponsored status", "is_sponsored"),
        ("Availability", "is_available"),
    )
    for label, column in filter_columns:
        options = sorted(products[column].dropna().unique().tolist())
        selected = st.sidebar.selectbox(
            label,
            ["All"] + options,
            key=f"shared-filter-{column}",
        )
        if selected != "All":
            filtered = filtered[filtered[column] == selected]

    valid_dates = products["Order_Placed"].dropna()
    if not valid_dates.empty:
        minimum_date = valid_dates.min().date()
        maximum_date = valid_dates.max().date()
        selected_dates = st.sidebar.date_input(
            "Collection date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
            key="shared-filter-order-dates",
        )
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
            if isinstance(start_date, date) and isinstance(end_date, date):
                order_dates = filtered["Order_Placed"].dt.date
                filtered = filtered[
                    order_dates.notna()
                    & (order_dates >= start_date)
                    & (order_dates <= end_date)
                ]
    else:
        st.sidebar.caption("No valid collection dates are available to filter.")

    return filtered
