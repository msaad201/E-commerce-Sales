import streamlit as st

st.set_page_config(
    page_title="Data Explorer | Amazon Product Analytics",
    page_icon=":material/table_view:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import plotly.express as px

from app_helpers import start_page
from theme import PALETTE, render_chart, section_heading


products = start_page(
    "explorer",
    "Data Explorer",
    "Inspect numeric distributions, category counts, and individual product listings.",
)

numeric_columns = products.select_dtypes(include="number").columns.tolist()
categorical_columns = products.select_dtypes(include=["object", "string"]).columns.drop(
    ["Product_Name", "product_url", "image_url"], errors="ignore"
)

tab_numeric, tab_categorical = st.tabs(["Numerical Analysis", "Categorical Analysis"])

with tab_numeric:
    section_heading("Showing Distribution & Outliers")
    if not numeric_columns:
        st.info("No numeric columns are available for analysis.")
    else:
        numeric_column = st.selectbox(
            "Column",
            numeric_columns,
            key="numeric-analysis-column",
        )
        numeric_chart = st.radio(
            "Chart",
            ["Histogram", "Box Plot"],
            horizontal=True,
            key="numeric-analysis-chart",
        )
        if st.button("Show Chart", key="show-numeric-chart"):
            values = products[numeric_column].dropna()
            if values.empty:
                st.info("This column has no numeric values for the current filters.")
            elif numeric_chart == "Histogram":
                fig = px.histogram(
                    products,
                    x=numeric_column,
                    title=f"Distribution of {numeric_column}",
                    color_discrete_sequence=[PALETTE["blue"]],
                )
                render_chart(
                    fig,
                    f"The histogram shows the distribution of {len(values):,} non-missing values.",
                )
            else:
                fig = px.box(
                    products,
                    y=numeric_column,
                    title=f"Distribution and outliers for {numeric_column}",
                    points="outliers",
                    color_discrete_sequence=[PALETTE["purple"]],
                )
                render_chart(
                    fig,
                    f"The box plot summarizes the median, spread, and outliers for "
                    f"{len(values):,} non-missing values.",
                )

with tab_categorical:
    section_heading("Number of repetitions")
    if categorical_columns.empty:
        st.info("No categorical columns are available for analysis.")
    else:
        categorical_column = st.selectbox(
            "Column",
            categorical_columns.tolist(),
            key="categorical-analysis-column",
        )
        categorical_chart = st.radio(
            "Chart",
            ["Histogram", "Pie"],
            horizontal=True,
            key="categorical-analysis-chart",
        )
        if st.button("Show Chart", key="show-categorical-chart"):
            category_counts = (
                products[categorical_column]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .rename_axis(categorical_column)
                .reset_index(name="Product count")
            )
            if category_counts.empty:
                st.info("This category has no values for the current filters.")
            else:
                if categorical_chart == "Histogram":
                    frequent_categories = set(
                        category_counts.head(20)[categorical_column].tolist()
                    )
                    if len(category_counts) > 20:
                        histogram_values = products[categorical_column].fillna("Unknown").astype(str)
                        histogram_values = histogram_values.where(
                            histogram_values.isin(frequent_categories), "Other"
                        )
                    else:
                        histogram_values = products[categorical_column].fillna("Unknown").astype(str)
                    fig = px.histogram(
                        histogram_values.to_frame(name=categorical_column),
                        x=categorical_column,
                        title=f"Product counts by {categorical_column}",
                        text_auto=True,
                        color_discrete_sequence=[PALETTE["blue"]],
                    )
                    fig.update_xaxes(categoryorder="total descending", tickangle=-30)
                    takeaway = (
                        f"Shows the {min(20, len(category_counts))} most frequent categories"
                        + (" and combines the remainder as Other." if len(category_counts) > 20 else ".")
                    )
                    render_chart(fig, takeaway)
                else:
                    pie_counts = category_counts
                    if len(category_counts) > 8:
                        pie_counts = category_counts.head(7).copy()
                        pie_counts.loc[len(pie_counts)] = [
                            "Other",
                            category_counts.iloc[7:]["Product count"].sum(),
                        ]
                    fig = px.pie(
                        pie_counts,
                        names=categorical_column,
                        values="Product count",
                        title=f"Product share by {categorical_column}",
                        color_discrete_sequence=PALETTE["chart"],
                        hole=0.42,
                    )
                    render_chart(
                        fig,
                        "The chart shows the leading groups; remaining groups are combined as Other when needed.",
                        height=390,
                    )

section_heading("Product image", "Preview the selected listing when an image URL is available.")
product_names = products["Product_Name"].dropna().unique().tolist()
selected_product = st.selectbox(
    "Product name",
    product_names,
    key="product-image-name",
)
selected_rows = products[products["Product_Name"] == selected_product]
if selected_rows.empty:
    st.info("No product record matches this selection.")
else:
    image_url = selected_rows["image_url"].dropna()
    if image_url.empty or not str(image_url.iloc[0]).strip():
        st.info("No product image is available for this listing.")
    else:
        st.image(str(image_url.iloc[0]), width=360)
    product_url = selected_rows["product_url"].dropna()
    if not product_url.empty and str(product_url.iloc[0]).strip():
        st.link_button("Open product listing", str(product_url.iloc[0]))

section_heading("Filtered product data")
st.dataframe(products, width="stretch", hide_index=True)
