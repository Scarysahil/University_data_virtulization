import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Tech Employment Trends (2001–2025)",
    page_icon="📊",
    layout="wide"
)

COLOR_CONTEXT = "#B0B0B0"
COLOR_HIGHLIGHT = "#0072B2"
COLOR_HIGHLIGHT2 = "#D55E00"
COLOR_HIGHLIGHT3 = "#009E73"

BIG_TECH = ['Apple', 'Microsoft', 'Alphabet', 'Amazon', 'Meta']
MATURE = ['Apple', 'Microsoft', 'Oracle', 'SAP', 'Intel', 'AMD', 'Adobe']
RECENT_IPO = ['Airbnb', 'Snap', 'Pinterest', 'Block', 'Lyft', 'Uber', 'Stripe']


def clean_layout(fig, title, height=450):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        height=height,
        margin=dict(t=70)
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor='#333')
    fig.update_yaxes(showgrid=True, gridcolor='#EEEEEE', showline=True, linecolor='#333')
    return fig

@st.cache_data
def load_data():
    df = pd.read_csv("tech_employment_2000_2025.csv")
    df['layoff_rate_pct'] = (df['layoffs'] / df['employees_start'].replace(0, np.nan)) * 100
    df['segment'] = np.where(df['company'].isin(BIG_TECH), 'Big Tech', 'Smaller/Newer Firms')
    df['company_type'] = np.select(
        [df['company'].isin(MATURE), df['company'].isin(RECENT_IPO)],
        ['Mature', 'Recent IPO'], default='Other'
    )
    df['revenue_per_employee_m'] = (df['revenue_billions_usd'] * 1000) / df['employees_end']
    df_sorted = df.sort_values(['company', 'year']).copy()
    df_sorted['revenue_growth_pct'] = df_sorted.groupby('company')['revenue_billions_usd'].pct_change() * 100
    df_sorted['headcount_growth_pct'] = df_sorted.groupby('company')['employees_end'].pct_change() * 100
    df_sorted['efficiency_gap'] = df_sorted['revenue_growth_pct'] - df_sorted['headcount_growth_pct']
    return df_sorted


df_full = load_data()

st.title("📊 Tech Employment Trends (2001–2025)")
st.markdown(
    "Exploring hiring, layoffs, and efficiency across 25 major tech companies, "
    "connected to US macroeconomic conditions. Final Individual Project — Data Visualization."
)


st.sidebar.header("Filters")

year_range = st.sidebar.slider(
    "Year range",
    int(df_full['year'].min()), int(df_full['year'].max()),
    (int(df_full['year'].min()), int(df_full['year'].max()))
)

all_companies = sorted(df_full['company'].unique())
selected_companies = st.sidebar.multiselect(
    "Companies (leave empty = all)",
    all_companies,
    default=[]
)

segment_filter = st.sidebar.radio(
    "Company grouping view",
    ["All companies", "Big Tech vs. Smaller/Newer", "Mature vs. Recent IPO"]
)


df = df_full[(df_full['year'] >= year_range[0]) & (df_full['year'] <= year_range[1])]
if selected_companies:
    df = df[df['company'].isin(selected_companies)]

st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_layoffs = int(df['layoffs'].sum())
total_hires = int(df['new_hires'].sum())
avg_layoff_rate = df['layoff_rate_pct'].mean()
avg_efficiency_gap = df['efficiency_gap'].mean()

col1.metric("Total Layoffs", f"{total_layoffs:,}")
col2.metric("Total New Hires", f"{total_hires:,}")
col3.metric("Avg. Layoff Rate", f"{avg_layoff_rate:.1f}%")
col4.metric("Avg. Efficiency Gap", f"{avg_efficiency_gap:.1f} pp",
            help="Revenue growth % minus headcount growth %. Positive = growing revenue faster than headcount.")

st.divider()

# -----------------------------
# Tabs to organize curated charts
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📉 Layoffs & Macro Context", "⚡ Efficiency & Revenue", "🏢 Company Comparisons"])

# --- TAB 1 ---
with tab1:
    st.subheader("How do layoffs relate to the broader economy?")

    yearly = df.groupby('year').agg(
        avg_layoff_rate=('layoff_rate_pct', 'mean'),
        unemployment=('unemployment_rate_us_pct', 'mean'),
        avg_hiring=('hiring_rate_pct', 'mean'),
        avg_attrition=('attrition_rate_pct', 'mean')
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=yearly['year'], y=yearly['avg_layoff_rate'],
                                   mode='lines+markers', name='Avg. Layoff Rate (%)',
                                   line=dict(color=COLOR_HIGHLIGHT2, width=3)))
        fig1.add_trace(go.Bar(x=yearly['year'], y=yearly['unemployment'],
                               name='US Unemployment (%)', marker_color=COLOR_CONTEXT,
                               opacity=0.35, yaxis='y2'))
        fig1.update_layout(
            yaxis=dict(title='Avg. Layoff Rate (%)'),
            yaxis2=dict(title='US Unemployment (%)', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', y=-0.25)
        )
        fig1 = clean_layout(fig1, "Layoffs track — but lag — US unemployment")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=yearly['year'], y=yearly['avg_hiring'], name='Hiring Rate (%)',
                                   fill='tozeroy', line=dict(color=COLOR_HIGHLIGHT, width=2)))
        fig2.add_trace(go.Scatter(x=yearly['year'], y=yearly['avg_attrition'], name='Attrition Rate (%)',
                                   fill='tozeroy', line=dict(color=COLOR_HIGHLIGHT2, width=2)))
        fig2 = clean_layout(fig2, "Hiring booms are followed by attrition waves ~1-2 years later")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Shock comparison: which companies cut deepest?")
    shocks = {'2008 Financial Crisis': (2008, 2009), '2020 Pandemic': (2020, 2020), '2022-23 Efficiency Era': (2022, 2023)}
    records = []
    for label, (start, end) in shocks.items():
        sub = df_full[(df_full['year'] >= start) & (df_full['year'] <= end)]
        grp = sub.groupby('company')['net_change'].sum().reset_index()
        grp['shock'] = label
        records.append(grp)
    shock_df = pd.concat(records)
    top_cutters = shock_df.sort_values('net_change').groupby('shock').head(5)

    fig3 = px.bar(top_cutters, x='net_change', y='company', color='shock', orientation='h',
                  color_discrete_sequence=[COLOR_HIGHLIGHT, COLOR_HIGHLIGHT2, COLOR_HIGHLIGHT3],
                  facet_col='shock', facet_col_wrap=1,
                  labels={'net_change': 'Net Employee Change'})
    fig3.update_yaxes(matches=None)
    fig3 = clean_layout(fig3, "2022-23 cuts were broader across more companies than 2008 or 2020", height=650)
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 2 ---
with tab2:
    st.subheader("Are companies growing revenue faster than headcount?")

    df_full['era'] = np.where(df_full['year'] >= 2022, '2022-2025 ("Efficiency Era")', 'Pre-2022')
    plot_df = df_full[(df_full['year'] >= year_range[0]) & (df_full['year'] <= year_range[1])].dropna(subset=['efficiency_gap'])
    if selected_companies:
        plot_df = plot_df[plot_df['company'].isin(selected_companies)]

    c1, c2 = st.columns(2)
    with c1:
        fig4 = px.box(plot_df, x='era', y='efficiency_gap', color='era',
                      color_discrete_map={'2022-2025 ("Efficiency Era")': COLOR_HIGHLIGHT2, 'Pre-2022': COLOR_CONTEXT},
                      labels={'era': 'Era', 'efficiency_gap': 'Revenue − Headcount Growth (pp)'})
        fig4.update_layout(showlegend=False)
        fig4 = clean_layout(fig4, "The 2022+ era shows revenue outpacing headcount more consistently")
        st.plotly_chart(fig4, use_container_width=True)

    with c2:
        focus = st.multiselect("Highlight companies for revenue/employee trend",
                                all_companies, default=['Meta', 'Amazon', 'Salesforce', 'Snap'])
        sub = df[df['company'].isin(focus)] if focus else df
        fig5 = px.line(sub, x='year', y='revenue_per_employee_m', color='company',
                        labels={'revenue_per_employee_m': 'Revenue per Employee ($M)'})
        fig5 = clean_layout(fig5, "Revenue-per-employee often jumps after layoff waves")
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Does the stock market react to layoffs?")
    fig6 = px.scatter(df, x='layoff_rate_pct', y='stock_price_change_pct',
                       color='segment', color_discrete_map={'Big Tech': COLOR_HIGHLIGHT, 'Smaller/Newer Firms': COLOR_HIGHLIGHT2},
                       trendline='ols', hover_data=['company', 'year'],
                       labels={'layoff_rate_pct': 'Layoff Rate (%)', 'stock_price_change_pct': 'Stock Price Change (%)'})
    fig6 = clean_layout(fig6, "Layoff rate shows only a weak same-year link to stock performance")
    st.plotly_chart(fig6, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.subheader("Volatility: who hires/fires the most erratically?")
    vol = df.groupby('company')['net_change'].agg(['std', 'mean']).reset_index()
    vol.columns = ['company', 'volatility', 'avg_net_change']

    fig7 = px.scatter(vol, x='avg_net_change', y='volatility', text='company',
                       color='volatility', color_continuous_scale=['#B0B0B0', '#0072B2'],
                       labels={'avg_net_change': 'Avg. Net Employee Change / Year', 'volatility': 'Volatility (Std Dev)'})
    fig7.update_traces(textposition='top center', marker=dict(size=10))
    fig7 = clean_layout(fig7, "Amazon and Meta show the highest hiring volatility", height=550)
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Mature companies vs. recently-IPO'd companies")
    comp = df_full[(df_full['company_type'] != 'Other') &
                    (df_full['year'] >= year_range[0]) & (df_full['year'] <= year_range[1])]
    comp_agg = comp.groupby(['company_type', 'year'])['layoff_rate_pct'].mean().reset_index()

    fig8 = px.line(comp_agg, x='year', y='layoff_rate_pct', color='company_type',
                    color_discrete_map={'Mature': COLOR_CONTEXT, 'Recent IPO': COLOR_HIGHLIGHT2},
                    labels={'layoff_rate_pct': 'Avg. Layoff Rate (%)', 'company_type': 'Company Type'})
    fig8 = clean_layout(fig8, "Recently-IPO'd companies show sharper, more volatile layoff spikes")
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("#### Raw data (filtered)")
    st.dataframe(df[['company', 'year', 'employees_end', 'new_hires', 'layoffs',
                      'revenue_billions_usd', 'stock_price_change_pct']].sort_values(['company', 'year']),
                 use_container_width=True, height=300)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Data Visualization Final Project · Summer 2026 · Built with Streamlit + Plotly")