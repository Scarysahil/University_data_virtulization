# pages/03_demand.py — YOUR new page (BBD squiggle level 3: demand story)
import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, sidebar_filters

# ─────────────────────────────────────────────────────────────────────────────
# Load data + shared sidebar
# One call to sidebar_filters gives you the SAME sidebar as pages 1 and 2 —
# and the filter choices carried over from them, for free.
# Then add a question title + caption.
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# A persisted widget of your own
# e.g. a radio or selectbox to focus on one room type, key='sel_room'
#   - initialise the key in session_state once
#   - keep it alive: st.session_state.sel_room = st.session_state.sel_room
#   - GUARD: if the saved value was filtered out, fall back to a valid option
#     BEFORE creating the widget
# TEST: pick a value, visit page 1, change a filter, come back — your choice
# must still be selected (or gracefully replaced if filtered out).
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# KPI row (st.columns(3)) about the focused selection
# e.g. listings, median reviews/month vs filtered market, median price
# 5-second test: the metrics alone should answer the page's question
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE


st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# One chart — demand story
# Suggestion: px.scatter of price vs reviews_per_month (reviews as a demand
# proxy), highlight column for your focused selection.
# BBD REQUIREMENTS:
#   - Name the colour type in a comment (highlight: blue vs grey)
#   - No red-green, no pies, no packed bubbles
# SWD REQUIREMENTS:
#   - White background, Arial font, insight title, use_container_width=True
# px REQUIREMENT:
#   - Start from px, highlight column + color_discrete_map — no go.Figure()
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE
