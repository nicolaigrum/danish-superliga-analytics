import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# Page config
st.set_page_config(
    page_title="Danish Superliga Analytics",
    page_icon="⚽",
    layout="wide"
)

# Initialize connection to Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["connections"]["supabase"]["url"]
    key = st.secrets["connections"]["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

# Title and description
st.title("Danish Superliga Analytics Dashboard")
st.markdown("""
This dashboard provides analytics and insights for the Danish Superliga 2024-2025 season.
Data is automatically updated daily from FotMob.
""")

# Sidebar filters
st.sidebar.title("Filters")
season = st.sidebar.selectbox("Season", ["2024-2025"])

# Get data from Supabase
@st.cache_data(ttl=3600)
def load_matches():
    response = supabase.table("matches").select("*").eq("season", "2024-2025").execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

@st.cache_data(ttl=3600)
def load_teams():
    response = supabase.table("teams").select("*").execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

@st.cache_data(ttl=3600)
def load_events():
    response = supabase.table("events").select("*").execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

try:
    matches_df = load_matches()
    teams_df = load_teams()
    events_df = load_events()

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["League Overview", "Team Analysis", "Player Stats"])

    with tab1:
        st.header("League Overview")
        
        if matches_df.empty:
            st.info("No match data available yet. Data will be populated once the scraper runs.")
        else:
            # League table
            st.subheader("League Table")
            st.dataframe(matches_df)
            
            # Recent matches
            st.subheader("Recent Matches")
            recent_matches = matches_df.sort_values("match_date", ascending=False).head(5)
            st.dataframe(recent_matches)

    with tab2:
        st.header("Team Analysis")
        
        if teams_df.empty:
            st.info("No team data available yet. Data will be populated once the scraper runs.")
        else:
            # Team selector
            selected_team = st.selectbox("Select Team", teams_df["name"].unique())
            
            # Team stats
            if selected_team:
                team_matches = matches_df[
                    (matches_df["home_team_id"] == selected_team) |
                    (matches_df["away_team_id"] == selected_team)
                ]
                
                # Display team stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Matches Played", len(team_matches))

    with tab3:
        st.header("Player Stats")
        
        if events_df.empty:
            st.info("No player data available yet. Data will be populated once the scraper runs.")
        else:
            # Player search and detailed stats
            player_name = st.text_input("Search Player")
            if player_name:
                st.info("Player search functionality coming soon!")

except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.info("Please check your database connection settings.") 