
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌱", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(r"co2_emissions.csv")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌱 CO2 Emissions Explorer")
st.caption("Source: Our World in Data — ourworldindata.org/co2-emissions")

# ── TASK 1: Sidebar with 5 widgets ────────────────────────────────────────────
#   a) st.selectbox for Region (with 'All')
#   b) st.multiselect for Countries (updates based on region — chained)
#   c) st.date_input for date range (two-handle; convert years to Jan-1 dates)
#   d) st.radio for Metric: "Total CO2 (Mt)" vs "CO2 per capita"
#   e) st.checkbox labelled "Show only top emitter highlighted"
#
# Guards:
#   - empty countries → st.warning + st.stop()
#   - incomplete date_input → st.warning + st.stop()
# Convert date_input result to pd.Timestamp before filtering.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    # YOUR CODE HERE

    # a) Region selectbox
    regions = ["All"] + sorted(df["Region"].unique())
    selected_region = st.selectbox("Select Region", regions)

    # b) Country multiselect (chained)
    if selected_region == "All":
        countries = sorted(df["Country"].unique())
    else:
        countries = sorted(df[df["Region"] == selected_region]["Country"].unique())

    selected_countries = st.multiselect("Select Countries", countries)

    # Guard: empty countries
    if not selected_countries:
        st.warning("Please select at least one country.")
        st.stop()

    # c) Date range input
    min_year, max_year = df["Year"].min(), df["Year"].max()
    start_date, end_date = st.date_input(
        "Select Year Range",
        value=(pd.Timestamp(f"{min_year}-01-01"), pd.Timestamp(f"{max_year}-01-01")),
        min_value=pd.Timestamp(f"{min_year}-01-01"),
        max_value=pd.Timestamp(f"{max_year}-01-01")
    )

    # Guard: incomplete date input
    if not start_date or not end_date:
        st.warning("Please select a valid date range.")
        st.stop()

    start_ts, end_ts = pd.Timestamp(start_date), pd.Timestamp(end_date)

    # d) Metric radio
    metric = st.radio("Select Metric", ["Total CO2 (Mt)", "CO2 per capita"])

    # e) Checkbox
    highlight_top = st.checkbox("Show only top emitter highlighted")


# ───────────────────────────────────────────────────────────────
# FILTERING
# ───────────────────────────────────────────────────────────────
filtered = df[
    (df["Country"].isin(selected_countries)) &
    (df["Date"] >= start_ts) &
    (df["Date"] <= end_ts)
]

metric_col = "CO2_Mt" if metric == "Total CO2 (Mt)" else "CO2_per_capita"

# filtered = ...  # apply all filters and store here


# ── TASK 2: Filter summary caption ────────────────────────────────────────────
# Show: "X countries | Region | Date range | Metric"
# BBD rule: always show users how many records match current filters
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE
st.caption(
    f"**{len(selected_countries)} countries** | "
    f"**Region:** {selected_region} | "
    f"**{start_ts.year} → {end_ts.year}** | "
    f"**Metric:** {metric}**"
)

# ── TASK 3: Two charts reacting to ALL filters ────────────────────────────────
#   Left: line chart — selected metric over time, one line per country
#         If "Show only top emitter highlighted" checkbox is on:
#           - grey all lines except the highest emitter in the date range
#           - label that country at the end of its line (SWD grey-and-highlight)
#   Right: bar chart — ranking for the last year in selected date range
#
# BBD colour requirement: name the colour type in a comment next to each chart
# SWD requirements: white background, insight title, use_container_width=True
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    # Line chart
    # YOUR CODE HERE
    pass
with col_left:
    st.subheader("Trend Over Time")

    line_df = filtered.copy()

    # Highlight logic
    if highlight_top:
        # Find top emitter in selected range
        totals = line_df.groupby("Country")[metric_col].sum().sort_values(ascending=False)
        top_country = totals.index[0]

        line_df["opacity"] = line_df["Country"].apply(lambda c: 1.0 if c == top_country else 0.2)
        color_discrete_map = {c: ("#1f77b4" if c == top_country else "lightgrey") for c in selected_countries}

        fig_line = px.line(
            line_df,
            x="Date",
            y=metric_col,
            color="Country",
            color_discrete_map=color_discrete_map,
            opacity=line_df["opacity"],
            title="Emissions Over Time (Highlighted Top Emitter)",  # SWD insight title
        )
    else:
        fig_line = px.line(
            line_df,
            x="Date",
            y=metric_col,
            color="Country",
            title="Emissions Over Time",  # SWD insight title
        )

    fig_line.update_layout(
        plot_bgcolor="white",  # SWD white background
        paper_bgcolor="white",
        legend_title_text="Country"
    )

    st.plotly_chart(fig_line, use_container_width=True)  # BBD: full width

with col_right:
    # Bar chart
    # YOUR CODE HERE
    pass
st.subheader("Ranking in Last Year")

last_year = end_ts.year
bar_df = filtered[filtered["Year"] == last_year]

bar_df = bar_df.groupby("Country")[metric_col].sum().reset_index()
bar_df = bar_df.sort_values(metric_col, ascending=False)

fig_bar = px.bar(
        bar_df,
        x=metric_col,
        y="Country",
        orientation="h",
        title=f"Ranking in {last_year}",  # SWD insight title
        color="Country",  # BBD categorical colour
    )

fig_bar.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis={'categoryorder': 'total ascending'}
    )

st.plotly_chart(fig_bar, use_container_width=True)


# ── EXTENSION: KPI row above the charts ───────────────────────────────────────
#   - Total CO2 in last year of selected range (sum across selected countries)
#   - % change from first to last year
#   - Country with highest emissions in last year
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE (optional)
k1, k2, k3 = st.columns(3)

last_year_df = filtered[filtered["Year"] == last_year]
first_year_df = filtered[filtered["Year"] == start_ts.year]

total_last = last_year_df[metric_col].sum()
total_first = first_year_df[metric_col].sum()
pct_change = ((total_last - total_first) / total_first) * 100 if total_first != 0 else 0

top_country_last = last_year_df.groupby("Country")[metric_col].sum().idxmax()

k1.metric("Total CO₂ (Last Year)", f"{total_last:,.2f}")
k2.metric("% Change", f"{pct_change:.2f}%")
k3.metric("Top Emitter", top_country_last)