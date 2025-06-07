import os
from typing import Dict, List
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class SupabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials in environment variables")
        self.client: Client = create_client(url, key)

    def upsert_teams(self, teams_data: List[Dict]) -> None:
        """Upsert team data into the teams table."""
        try:
            self.client.table("teams").upsert(teams_data).execute()
        except Exception as e:
            print(f"Error upserting teams: {e}")

    def upsert_players(self, players_data: List[Dict]) -> None:
        """Upsert player data into the players table."""
        try:
            self.client.table("players").upsert(players_data).execute()
        except Exception as e:
            print(f"Error upserting players: {e}")

    def upsert_matches(self, matches_data: List[Dict]) -> None:
        """Upsert match data into the matches table."""
        try:
            self.client.table("matches").upsert(matches_data).execute()
        except Exception as e:
            print(f"Error upserting matches: {e}")

    def upsert_events(self, events_data: List[Dict]) -> None:
        """Upsert event data into the events table."""
        try:
            self.client.table("events").upsert(events_data).execute()
        except Exception as e:
            print(f"Error upserting events: {e}")

    def get_matches_by_season(self, season: str) -> List[Dict]:
        """Get all matches for a specific season."""
        try:
            response = self.client.table("matches").select("*").eq("season", season).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return []

    def get_team_matches(self, team_id: str) -> List[Dict]:
        """Get all matches for a specific team."""
        try:
            response = self.client.table("matches").select("*").or_(
                f"home_team_id.eq.{team_id},away_team_id.eq.{team_id}"
            ).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching team matches: {e}")
            return []

    def get_player_events(self, player_id: str) -> List[Dict]:
        """Get all events for a specific player."""
        try:
            response = self.client.table("events").select("*").eq("player_id", player_id).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching player events: {e}")
            return []

    def get_match_events(self, match_id: str) -> List[Dict]:
        """Get all events for a specific match."""
        try:
            response = self.client.table("events").select("*").eq("match_id", match_id).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching match events: {e}")
            return [] 