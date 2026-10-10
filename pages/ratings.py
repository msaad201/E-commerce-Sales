import streamlit as st

st.set_page_config(
    page_title="Ratings and Reviews | Amazon Product Analytics",
    page_icon=":material/star:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
import plotly.express as px

from app_helpers import start_page
from theme import PALETTE, render_chart, render_kpi_cards, section_heading


products = start_page(
    "ratings",
    "Ratings and Reviews",
    "Understand customer ratings, review volume, and how feedback varies by product group.",
)

average_rating = products["rating"].mean()
total_reviews = products["number_of_reviews"].sum(min_count=1)
reviewed_products = products["number_of_reviews"].gt(0).sum()
best_seller_rating = products.loc[
    products["Best_seller"] == "Best Seller", "rating"
].mean()
render_kpi_cards(
    [
        (
            "Average rating",
            f"{average_rating:.2f} / 5" if pd.notna(average_rating) else "—",
            "Mean product rating in the filtered data",
            "star",
        ),
        (
            "Total reviews",
            f"{total_reviews:,.0f}" if pd.notna(total_reviews) else "—",
            "Sum of listed review counts",
            "review",
        ),
        ("Products with reviews", f"{reviewed_products:,}", "Products with at least one review", "grid"),
        (
            "Best Seller rating",
            f"{best_seller_rating:.2f} / 5" if pd.notna(best_seller_rating) else "—",
            "Average rating for Best Seller listings",
            "award",
        ),
    ]
)

section_heading("Rating distribution", "Each bar shows the number of products at a rating.")
rating_rows = products.dropna(subset=["rating"])
if rating_rows.empty:
    st.info("No rating values are available for the current filters.")
else:
    fig = px.histogram(
        rating_rows,
        x="rating",
        nbins=20,
        title="Product rating distribution",
        labels={"rating": "Rating (out of 5)", "count": "Products"},
        color_discrete_sequence=[PALETTE["blue"]],
    )
    fig.update_traces(hovertemplate="Rating range: %{x}<br>Products: %{y}<extra></extra>")
    render_chart(
        fig,
        f"The filtered products have an average rating of {average_rating:.2f} out of 5."
        if pd.notna(average_rating)
        else "No rating values are available to calculate an average.",
    )

section_heading(
    "Rating and review volume",
    "Compare product ratings with the number of reviews attached to each listing.",
)
rating_review_rows = products.dropna(subset=["rating", "number_of_reviews"])
if rating_review_rows.empty:
    st.info("No rating and review-count pairs are available for the current filters.")
else:
    fig = px.scatter(
        rating_review_rows,
        x="number_of_reviews",
        y="rating",
        color="Best_seller",
        color_discrete_sequence=PALETTE["chart"],
        title="Ratings versus review counts",
        labels={
            "number_of_reviews": "Number of reviews",
            "rating": "Rating (out of 5)",
            "Best_seller": "Best Seller status",
        },
        hover_data=["Product_Name"],
        opacity=0.62,
    )
    fig.update_xaxes(type="log")
    render_chart(
        fig,
        "The logarithmic review axis makes both newer and highly reviewed products visible.",
    )

section_heading("Average rating by Best Seller status")
ratings_by_badge = (
    products.dropna(subset=["rating"])
    .groupby("Best_seller", as_index=False)["rating"]
    .mean()
    .rename(columns={"Best_seller": "Best Seller status", "rating": "Average rating"})
)
if ratings_by_badge.empty:
    st.info("No product ratings match the current filters.")
else:
    fig = px.bar(
        ratings_by_badge,
        x="Best Seller status",
        y="Average rating",
        color="Best Seller status",
        color_discrete_sequence=PALETTE["chart"],
    )
    fig.update_yaxes(range=[0, 5])
    render_chart(
        fig,
        "Compare average product ratings for listings with and without a Best Seller badge.",
    )
