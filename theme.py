from html import escape
from pathlib import Path
from typing import Sequence

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import streamlit.components.v1 as components


PALETTE = {
    "background": "#0B0F17",
    "surface": "#151B27",
    "surface_muted": "#1B2433",
    "text": "#E8EDF7",
    "text_muted": "#A0AEC2",
    "border": "#2B3546",
    "blue": "#82A6FF",
    "blue_dark": "#B2C7FF",
    "blue_soft": "#202D49",
    "purple": "#B19AFF",
    "purple_soft": "#28223F",
    "gradient_blue": "#172239",
    "cyan": "#69CDE0",
    "teal": "#69C9B1",
    "gold": "#F1C477",
    "rose": "#F093A4",
    "grid": "#293447",
    "chart": ["#82A6FF", "#B19AFF", "#69CDE0", "#69C9B1", "#F1C477", "#F093A4"],
}
FONT_STACK = '"Segoe UI", "Segoe UI Variable", Arial, sans-serif'
FONT_STACK_ATTRIBUTE = escape(FONT_STACK, quote=True)
CSS_PATH = Path(__file__).parent / ".streamlit" / "style.css"

PAGE_LINKS = (
    ("overview", "Overview", "home_page.py", ":material/space_dashboard:"),
    ("pricing", "Pricing and Discounts", "pages/pricing.py", ":material/sell:"),
    ("delivery", "Delivery", "pages/delivery.py", ":material/local_shipping:"),
    ("ratings", "Ratings and Reviews", "pages/ratings.py", ":material/star:"),
    ("explorer", "Data Explorer", "pages/data_explorer.py", ":material/table_view:"),
)

HEADER_ICONS = {
    "overview": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "pricing": '<path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "delivery": '<path d="M10 17h4V5H2v12h3"/><path d="M14 9h4l4 4v4h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="16.5" cy="17.5" r="2.5"/>',
    "ratings": '<path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "explorer": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 4v16"/>',
}

KPI_ICONS = {
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="m8.2 13.5-1.3 8L12 19l5.1 2.5-1.3-8"/>',
    "truck": '<path d="M10 17h4V5H2v12h3"/><path d="M14 9h4l4 4v4h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="16.5" cy="17.5" r="2.5"/>',
    "star": '<path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "review": '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8z"/>',
    "tag": '<path d="M20.6 13.4 11 3.8H4v7l9.6 9.6a2 2 0 0 0 2.8 0l4.2-4.2a2 2 0 0 0 0-2.8z"/><circle cx="7.5" cy="7.5" r=".7"/>',
}


def _css_variables() -> str:
    variables = {
        "app-bg": PALETTE["background"],
        "surface": PALETTE["surface"],
        "surface-muted": PALETTE["surface_muted"],
        "text": PALETTE["text"],
        "text-muted": PALETTE["text_muted"],
        "border": PALETTE["border"],
        "blue": PALETTE["blue"],
        "blue-dark": PALETTE["blue_dark"],
        "purple": PALETTE["purple"],
        "grid": PALETTE["grid"],
        "font-stack": FONT_STACK,
    }
    return ":root{" + "".join(
        f"--{name}:{value};" for name, value in variables.items()
    ) + "color-scheme:dark;}"


def apply_theme() -> None:
    pio.templates["copilot_dark"] = go.layout.Template(
        layout=go.Layout(
            colorway=PALETTE["chart"],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": FONT_STACK, "color": PALETTE["text"]},
            xaxis={
                "gridcolor": PALETTE["grid"],
                "linecolor": PALETTE["border"],
                "zerolinecolor": PALETTE["border"],
                "title_standoff": 12,
            },
            yaxis={
                "gridcolor": PALETTE["grid"],
                "linecolor": PALETTE["border"],
                "zerolinecolor": PALETTE["border"],
                "title_standoff": 12,
            },
            hoverlabel={
                "bgcolor": PALETTE["surface"],
                "bordercolor": PALETTE["border"],
                "font": {"family": FONT_STACK, "color": PALETTE["text"]},
            },
        )
    )
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{_css_variables()}{css}</style>",
        unsafe_allow_html=True,
    )


def render_sidebar(active_page: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
          <span class="sidebar-brand-mark">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 7.5 12 3l8 4.5v9L12 21l-8-4.5z"
                fill="none" stroke="{PALETTE['blue']}" stroke-width="1.7"/>
              <path d="m4.5 7.7 7.5 4.2 7.5-4.2M12 12v8.3"
                fill="none" stroke="{PALETTE['purple']}" stroke-width="1.7"/>
            </svg>
          </span>
          <span><strong>Amazon Insights</strong><small>Product analytics</small></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("##### Workspace")
    for page_id, label, path, icon in PAGE_LINKS:
        st.sidebar.page_link(
            path,
            label=label,
            icon=icon,
        )
    active_label = next(
        label for page_id, label, _, _ in PAGE_LINKS if page_id == active_page
    )
    st.sidebar.markdown(
        f'<p class="sidebar-current">Viewing: {escape(active_label)}</p>',
        unsafe_allow_html=True,
    )
    st.sidebar.divider()


def render_page_header(page_id: str, title: str, subtitle: str) -> None:
    icon = HEADER_ICONS[page_id]
    html = f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="rounded-3xl shadow-sm p-7 md:p-9 mb-5"
         style="font-family:{FONT_STACK_ATTRIBUTE};border:1px solid {PALETTE['border']};
         background:linear-gradient(115deg,{PALETTE['surface']} 42%,
         {PALETTE['gradient_blue']} 77%,{PALETTE['purple_soft']} 100%);">
      <div class="flex items-center gap-5">
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center shrink-0"
             style="background:linear-gradient(135deg,{PALETTE['blue']},{PALETTE['purple']});">
          <svg viewBox="0 0 24 24" width="27" height="27" fill="none"
               stroke="white" stroke-width="1.7" stroke-linecap="round"
               stroke-linejoin="round" aria-hidden="true">{icon}</svg>
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-widest mb-1"
             style="color:{PALETTE['blue_dark']}">Amazon product analytics</p>
          <h1 class="text-3xl md:text-4xl font-semibold tracking-tight m-0"
              style="color:{PALETTE['text']}">{escape(title)}</h1>
          <p class="text-sm md:text-base mt-2 mb-0"
             style="color:{PALETTE['text_muted']}">{escape(subtitle)}</p>
        </div>
      </div>
    </div>
    """
    components.html(html, height=180, scrolling=False)


def render_kpi_cards(items: Sequence[tuple[str, str, str, str]]) -> None:
    cards = []
    for label, value, detail, icon_name in items:
        icon = KPI_ICONS[icon_name]
        cards.append(
            f"""
            <div class="rounded-2xl shadow-sm p-5 min-h-36"
                 style="background:{PALETTE['surface']};border:1px solid {PALETTE['border']}">
              <div class="flex items-center justify-between gap-3">
                <p class="text-sm font-medium m-0"
                   style="color:{PALETTE['text_muted']}">{escape(label)}</p>
                <span class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                      style="background:{PALETTE['blue_soft']};color:{PALETTE['blue']}">
                  <svg viewBox="0 0 24 24" width="19" height="19" fill="none"
                       stroke="currentColor" stroke-width="1.7" stroke-linecap="round"
                       stroke-linejoin="round" aria-hidden="true">{icon}</svg>
                </span>
              </div>
              <p class="text-2xl font-semibold tracking-tight mt-4 mb-1"
                 style="color:{PALETTE['text']}">{escape(value)}</p>
              <p class="text-xs leading-relaxed m-0"
                 style="color:{PALETTE['text_muted']}">{escape(detail)}</p>
            </div>
            """
        )
    html = f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4"
         style="font-family:{FONT_STACK_ATTRIBUTE}">
      {''.join(cards)}
    </div>
    """
    components.html(html, height=300, scrolling=False)


def section_heading(title: str, description: str | None = None) -> None:
    safe_title = escape(title)
    detail = (
        f'<p class="section-description">{escape(description)}</p>'
        if description
        else ""
    )
    st.markdown(
        f'<div class="section-heading"><h2>{safe_title}</h2>{detail}</div>',
        unsafe_allow_html=True,
    )


def render_chart(
    figure: go.Figure,
    takeaway: str,
    *,
    height: int = 420,
    key: str | None = None,
) -> None:
    figure.update_layout(
        template="copilot_dark",
        height=height,
        margin={"l": 24, "r": 20, "t": 62, "b": 32},
        title={"x": 0.02, "xanchor": "left", "font": {"size": 18}},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        hovermode="closest",
    )
    with st.container(border=True):
        st.plotly_chart(figure, width="stretch", key=key)
        st.caption(takeaway)
