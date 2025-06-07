import streamlit as st
import pandas as pd
import plotly.express as px
from st_supabase_connection import SupabaseConnection

# Page config
st.set_page_config(
    page_title="Danish Superliga Analytics",
    page_icon="⚽",
    layout="wide"
)

# Initialize connection to Supabase
conn = st.connection("supabase", type=SupabaseConnection)

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
    response = conn.query("matches", "SELECT * FROM matches WHERE season = '2024-2025'").execute()
    return pd.DataFrame(response.data)

@st.cache_data(ttl=3600)
def load_teams():
    response = conn.query("teams", "SELECT * FROM teams").execute()
    return pd.DataFrame(response.data)

@st.cache_data(ttl=3600)
def load_events():
    response = conn.query("events", "SELECT * FROM events").execute()
    return pd.DataFrame(response.data)

try:
    matches_df = load_matches()
    teams_df = load_teams()
    events_df = load_events()

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["League Overview", "Team Analysis", "Player Stats"])

    with tab1:
        st.header("League Overview")
        
        # League table
        if not matches_df.empty:
            # Calculate points and create league table
            league_table = pd.DataFrame()
            # Add league table calculation logic here
            st.subheader("League Table")
            st.dataframe(league_table)
            
            # Recent matches
            st.subheader("Recent Matches")
            recent_matches = matches_df.sort_values("match_date", ascending=False).head(5)
            st.dataframe(recent_matches)
            
            # Goals per match trend
            st.subheader("Goals per Match Trend")
            # Add goals trend visualization here using plotly

    with tab2:
        st.header("Team Analysis")
        
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
            # Add more team metrics
            
            # Team form chart
            st.subheader("Team Form")
            # Add form visualization here

    with tab3:
        st.header("Player Stats")
        
        # Top scorers
        st.subheader("Top Scorers")
        # Add top scorers table and chart
        
        # Player search and detailed stats
        player_name = st.text_input("Search Player")
        if player_name:
            # Add player stats display logic here
            pass

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please make sure your Supabase connection is properly configured in .streamlit/secrets.toml") 