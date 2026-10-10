import streamlit as st

st.set_page_config(
    page_title="Amazon Product Analytics",
    page_icon=":material/storefront:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
import plotly.express as px

from app_helpers import start_page
from theme import PALETTE, render_chart, render_kpi_cards, section_heading


products = start_page(
    "overview",
    "Amazon Product Overview",
    "A clear view of product listings, estimated sales, and delivery performance.",
)
source = products

product_count = source["Product_Name"].nunique()
estimated_sales = source["Revenue_last_month"].sum(min_count=1)
best_sellers = (source["Best_seller"] == "Best Seller").sum()
longest_delivery = source["delivery_days"].max()

render_kpi_cards(
    [
        ("Products", f"{product_count:,}", "Unique product listings", "grid"),
        (
            "Monthly sales estimate",
            f"{estimated_sales:,.0f}" if pd.notna(estimated_sales) else "—",
            "Sum of the source sales-volume estimate; not currency",
            "chart",
        ),
        (
            "Best Sellers",
            f"{best_sellers:,}",
            f"Out of {len(source):,} filtered listings",
            "award",
        ),
        (
            "Longest delivery",
            f"{longest_delivery:,.0f} days" if pd.notna(longest_delivery) else "—",
            "Maximum listed delivery time",
            "truck",
        ),
    ]
)

section_heading("Sales over collection dates", "A daily view of the existing monthly sales estimate.")
daily_sales = (
    source.assign(Collection_date=source["Order_Placed"].dt.date)
    .groupby("Collection_date", as_index=False)["Revenue_last_month"]
    .sum(min_count=1)
    .sort_values("Collection_date")
    .dropna(subset=["Revenue_last_month"])
)
daily_sales = daily_sales.rename(columns={"Revenue_last_month": "Monthly sales estimate"})
if daily_sales.empty:
    st.info("No dated product records match the current filters.")
else:
    fig = px.line(
        daily_sales,
        x="Collection_date",
        y="Monthly sales estimate",
        markers=True,
        color_discrete_sequence=[PALETTE["blue"]],
        title="Estimated monthly sales by collection date",
    )
    render_chart(
        fig,
        "The line shows how the combined monthly sales estimate varies across collection dates.",
    )

section_heading("Daily Revenue", "Keep the original day-of-month selector and matching product table.")
days = source["Order_Placed"].dt.day.dropna().unique().tolist()
selected_day = st.selectbox("Day", ["All Days"] + days, key="daily-revenue-day")
day_rows = (
    source
    if selected_day == "All Days"
    else source[source["Order_Placed"].dt.day == selected_day]
)
if day_rows.empty:
    st.info("No product records were collected on that day in the current filtered data.")
else:
    st.dataframe(day_rows, width="stretch", hide_index=True)

with st.expander("Project data notes"):
    st.markdown(
        "`Revenue_last_month` is an approximate monthly sales-volume value derived "
        "from the listing's bought-in-last-month label; it is not revenue in dollars. "
        "The charts retain the project's existing column and aggregation."
    )
    readme_path = __import__("pathlib").Path(__file__).with_name("README.md")
    if readme_path.exists():
        st.markdown(readme_path.read_text(encoding="utf-8"))
