import streamlit as st

st.set_page_config(
    page_title="Delivery | Amazon Product Analytics",
    page_icon=":material/local_shipping:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import plotly.express as px

from app_helpers import start_page
from theme import PALETTE, render_chart, section_heading


products = start_page(
    "delivery",
    "Delivery and Promotion",
    "Compare delivery options and sponsored placements using the existing sales calculations.",
)

delivery_options = products["delivery"].dropna().unique().tolist()
sponsored_options = products["is_sponsored"].dropna().unique().tolist()
delivery_choice = st.selectbox(
    "Delivery type",
    ["ALL Data"] + delivery_options,
    key="delivery-analysis-type",
)
sponsored_choice = st.selectbox(
    "Sponsored status",
    ["ALL Data"] + sponsored_options,
    key="sponsored-analysis-type",
)

col_delivery, col_sponsored = st.columns(2)

section_heading(
    "Delivery Type and Its Effect on Sales",
    "Select a delivery type to view its product rows and sales estimate.",
)
delivery_rows = (
    products
    if delivery_choice == "ALL Data"
    else products[products["delivery"] == delivery_choice]
)
with col_delivery:
    if delivery_rows.empty:
        st.info("No product records match this delivery type.")
    else:
        st.dataframe(delivery_rows, width="stretch", hide_index=True)
        if delivery_choice != "ALL Data":
            delivery_revenue = delivery_rows.dropna(subset=["Revenue_last_month"])
            if delivery_revenue.empty:
                st.info("No monthly sales estimates are available for this delivery type.")
            else:
                fig = px.bar(
                    delivery_revenue,
                    x="delivery",
                    y="Revenue_last_month",
                    title="Monthly sales estimate by delivery type",
                    labels={
                        "delivery": "Delivery type",
                        "Revenue_last_month": "Monthly sales estimate",
                    },
                    color_discrete_sequence=[PALETTE["blue"]],
                )
                render_chart(
                    fig,
                    "The bar reports the existing sales estimate for the selected delivery type.",
                )
            pie_data = (
                products.groupby("delivery", as_index=False)["Revenue_last_month"]
                .sum(min_count=1)
                .dropna(subset=["Revenue_last_month"])
            )
            pie_data = pie_data.rename(columns={"Revenue_last_month": "Monthly sales estimate"})
            if pie_data.empty:
                st.info("No monthly sales estimates are available for the delivery share chart.")
            elif len(pie_data) <= 8:
                fig = px.pie(
                    pie_data,
                    names="delivery",
                    values="Monthly sales estimate",
                    title="Sales estimate by delivery type",
                    color_discrete_sequence=PALETTE["chart"],
                    hole=0.42,
                )
                render_chart(
                    fig,
                    "Share of the filtered sales estimate across delivery types.",
                    height=390,
                )
            else:
                st.info("The delivery share chart is hidden because there are too many categories.")

with col_sponsored:
    sponsored_rows = (
        products
        if sponsored_choice == "ALL Data"
        else products[products["is_sponsored"] == sponsored_choice]
    )
    if sponsored_rows.empty:
        st.info("No product records match this sponsored status.")
    else:
        st.dataframe(sponsored_rows, width="stretch", hide_index=True)
        if sponsored_choice != "ALL Data":
            sponsored_revenue = sponsored_rows.dropna(subset=["Revenue_last_month"])
            if sponsored_revenue.empty:
                st.info("No monthly sales estimates are available for this sponsored status.")
            else:
                fig = px.bar(
                    sponsored_revenue,
                    x="is_sponsored",
                    y="Revenue_last_month",
                    title="Monthly sales estimate by sponsored status",
                    labels={
                        "is_sponsored": "Sponsored status",
                        "Revenue_last_month": "Monthly sales estimate",
                    },
                    color_discrete_sequence=[PALETTE["purple"]],
                )
                render_chart(
                    fig,
                    "The bar reports the existing sales estimate for the selected sponsored status.",
                )
            pie_data = (
                products.groupby("is_sponsored", as_index=False)["Revenue_last_month"]
                .sum(min_count=1)
                .dropna(subset=["Revenue_last_month"])
            )
            pie_data = pie_data.rename(columns={"Revenue_last_month": "Monthly sales estimate"})
            if pie_data.empty:
                st.info("No monthly sales estimates are available for the sponsored share chart.")
            elif len(pie_data) <= 8:
                fig = px.pie(
                    pie_data,
                    names="is_sponsored",
                    values="Monthly sales estimate",
                    title="Sales estimate by sponsored status",
                    color_discrete_sequence=PALETTE["chart"],
                    hole=0.42,
                )
                render_chart(
                    fig,
                    "Share of the filtered sales estimate across sponsored-status groups.",
                    height=390,
                )
            else:
                st.info("The sponsored share chart is hidden because there are too many categories.")
