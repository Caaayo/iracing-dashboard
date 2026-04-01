import pandas as pd
import streamlit as st
import plotly.express as px
from processing.results import load_races

st.set_page_config(
    page_title="iRacing Dashboard",
    layout="wide"
)

st.title("🏎️ sudiT iRacing Dashboard 🏎️")

races = load_races()

races["season"] = races["season_year"].astype(str) + " " + "S" + races["season_quarter"].astype(str)
unique_season = races["season"].unique()
recent_season = (
    races.sort_values("season", ascending=False)
    ["season"]
    .drop_duplicates()
    .head(1)
    .tolist()
)


# Converts "start_time" to a date
races["start_time"] = pd.to_datetime(races["start_time"])

unique_series = races["series_name"].unique()
recent_series = (
    races.sort_values("start_time", ascending=False)
    ["series_name"]
    .drop_duplicates()
    .head(3)
    .tolist()
)


with st.expander("Debug / Data Overview"):
    st.write("List of Columns:", races.columns)
    st.write("Available Seasons:", unique_season)
    st.write("Available Series:", unique_series)

races["pos_delta"] = races["starting_position_in_class"] - races["finish_position_in_class"]

st.sidebar.title("Filters")

season = st.sidebar.multiselect(
    "Season",
    unique_season,
    default=recent_season
)
series = st.sidebar.multiselect(
    "Series",
    unique_series,
    default=recent_series
)


races = races[races["season"].isin(season)]
races = races[races["series_name"].isin(series)]

col1, col2, col3 = st.columns(3)

# Get the total number of races done
with col1: 
    st.metric("Total Races", len(races))
    
# Get the average finishing position
with col2:
    st.metric("Avg Finish Position", round(races["finish_position"].mean(), 1))

# Get the total number of accidents
with col3:
    st.metric("Total Accidents", races["incidents"].sum())

st.dataframe(races)


fig = px.line(
    races.sort_values("start_time"),
    x="start_time",
    y="finish_position_in_class",
    markers=True,
    title="Finishing Positions Over Time"
)

# Style the line and markers
fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8),
    customdata=races.sort_values("start_time")[["starting_position_in_class", "pos_delta","series_name", "track_name", "incidents"]],
    hovertemplate=
        "<b>Date:</b> %{x}<br>" +
        "<b>Start:</b> %{customdata[0]}<br>" +
        "<b>Finish:</b> %{y}<br>" +
        "<b>Delta:</b> %{customdata[1]:+}<br>" +
        "<b>Series:</b> %{customdata[2]}<br>" +
        "<b>Track:</b> %{customdata[3]}<br>" +
        "<b>Incidents:</b> %{customdata[4]}<br>" +
        "<extra></extra>"
)

# Reverse Y-axis so P1 is at the top
# Get the max finish position
max_pos = races["finish_position_in_class"].max()

fig.update_yaxes(
    autorange="reversed",
    title="Finish Position",
    range=[max_pos, 0],  # top is 0, bottom is max position
    tick0=0,
    dtick=1,
    showline=True
)

fig.update_xaxes(
    title="Day"
)

# Clean layout
fig.update_layout(
    template="plotly_dark",
    title=dict(x=0.02),
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# Line chart of iRating over time
# fig_irating = px.line(races, x="start_time", y="irating", title="iRating over Time")
# st.plotly_chart(fig_irating, use_container_width=True)