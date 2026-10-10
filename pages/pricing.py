import streamlit as st

st.set_page_config(
    page_title="Pricing and Discounts | Amazon Product Analytics",
    page_icon=":material/sell:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import plotly.express as px

from app_helpers import start_page
from theme import PALETTE, render_chart, section_heading


products = start_page(
    "pricing",
    "Pricing and Discounts",
    "Explore discount levels, listed prices, and their relationship to estimated sales.",
)

section_heading(
    "Discount Percentage vs. Monthly Sales",
    "Uses the original discount grouping and monthly sales-estimate sum.",
)
sales_with_discount = (
    products.groupby("Dicount_percentage_(%)", as_index=False)["Revenue_last_month"]
    .sum(min_count=1)
    .sort_values("Dicount_percentage_(%)")
    .dropna(subset=["Revenue_last_month"])
    .rename(
        columns={
            "Dicount_percentage_(%)": "Discount percentage (%)",
            "Revenue_last_month": "Monthly sales estimate",
        }
    )
)
chart_choice = st.radio(
    "Chart",
    ["Histogram", "Line"],
    horizontal=True,
    key="discount-sales-chart",
)
if st.button("Show Chart", key="show-discount-sales"):
    if sales_with_discount.empty:
        st.info("There are no discount records for the selected filters.")
    else:
        if chart_choice == "Histogram":
            fig = px.histogram(
                sales_with_discount,
                x="Discount percentage (%)",
                y="Monthly sales estimate",
                title="Estimated monthly sales distribution by discount percentage",
                color_discrete_sequence=[PALETTE["blue"]],
            )
        else:
            fig = px.line(
                sales_with_discount,
                x="Discount percentage (%)",
                y="Monthly sales estimate",
                title="Estimated monthly sales by discount percentage",
                markers=True,
                color_discrete_sequence=[PALETTE["blue"]],
            )
        fig.update_traces(
            hovertemplate="Discount: %{x}%<br>Sales estimate: %{y:,.0f}<extra></extra>"
        )
        render_chart(
            fig,
            "Compare the existing combined monthly sales estimate across discount levels.",
        )

section_heading(
    "Most Expensive Products",
    "The original ranking counts non-missing listed-price records per product.",
)
expensive_products = (
    products.groupby("Product_Name")["listed_price"]
    .count()
    .reset_index()
    .sort_values(by="listed_price", ascending=False)
)
top_product_count = st.slider(
    "Select number of products to show",
    1,
    40,
    10,
    key="expensive-products-top-n",
)
display_style = st.radio(
    "Select style",
    ["Chart", "Table"],
    horizontal=True,
    key="expensive-products-style",
)
if st.button("Show Chart", key="show-expensive-products"):
    top_products = expensive_products.head(top_product_count)
    if top_products.empty:
        st.info("No product price records match the current filters.")
    elif display_style == "Table":
        st.dataframe(top_products, width="stretch", hide_index=True)
    else:
        fig = px.bar(
            top_products,
            x="Product_Name",
            y="listed_price",
            title="Products by listed-price record count",
            labels={
                "Product_Name": "Product",
                "listed_price": "Listed-price record count",
            },
            color_discrete_sequence=[PALETTE["purple"]],
        )
        fig.update_layout(xaxis_tickangle=-35)
        render_chart(
            fig,
            "This preserves the original count-based ranking; it is not sorted by price amount.",
        )
