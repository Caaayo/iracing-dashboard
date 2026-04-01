import streamlit as st
from processing.results import load_races

st.set_page_config(
    page_title="iRacing Dashboard",
    layout="wide"
)

st.title("🏎️ sudiT iRacing Dashboard 🏎️")

races = load_races()

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


