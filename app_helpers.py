import pandas as pd
import streamlit as st

from data import filter_by_shared_controls, load_data
from theme import apply_theme, render_page_header, render_sidebar


def start_page(page_id: str, title: str, subtitle: str) -> pd.DataFrame:
    apply_theme()
    products = load_data()
    render_sidebar(page_id)
    filtered = filter_by_shared_controls(products)
    render_page_header(page_id, title, subtitle)

    if filtered.empty:
        st.info("No products match these filters. Adjust the shared filters in the sidebar.")
        st.stop()

    return filtered
