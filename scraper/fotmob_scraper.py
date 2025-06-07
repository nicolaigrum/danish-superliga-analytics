import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from database.db_operations import SupabaseManager

class FotMobScraper:
    def __init__(self):
        self.base_url = "https://www.fotmob.com"
        self.api_url = "https://www.fotmob.com/api"
        # Danish Superliga league ID for FotMob
        self.league_id = "73"  # This needs to be verified
        self.season = "2024-2025"
        self.data_dir = "data"
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Setup Chrome options for Selenium
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize database manager
        self.db = SupabaseManager()
        
    def _get_driver(self) -> webdriver.Chrome:
        """Initialize and return a Chrome WebDriver instance."""
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=self.chrome_options)
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make an API request to FotMob."""
        url = f"{self.api_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_league_matches(self) -> List[Dict]:
        """Fetch all matches for the Danish Superliga."""
        try:
            # This endpoint needs to be verified with actual FotMob API structure
            endpoint = f"leagues/{self.league_id}/matches"
            data = self._make_request(endpoint)
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.data_dir}/matches_raw_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            
            # Update database
            if data:
                self.db.upsert_matches(data)
            
            return data
        except Exception as e:
            print(f"Error fetching league matches: {e}")
            return []
    
    def get_team_info(self, team_id: str) -> Dict:
        """Fetch detailed information about a team."""
        try:
            endpoint = f"teams/{team_id}"
            data = self._make_request(endpoint)
            
            # Update database
            if data:
                self.db.upsert_teams([data])
            
            return data
        except Exception as e:
            print(f"Error fetching team info for {team_id}: {e}")
            return {}
    
    def get_player_info(self, player_id: str) -> Dict:
        """Fetch detailed information about a player."""
        try:
            endpoint = f"players/{player_id}"
            data = self._make_request(endpoint)
            
            # Update database
            if data:
                self.db.upsert_players([data])
            
            return data
        except Exception as e:
            print(f"Error fetching player info for {player_id}: {e}")
            return {}
    
    def get_match_events(self, match_id: str) -> Dict:
        """Fetch all events for a specific match."""
        try:
            endpoint = f"matches/{match_id}/events"
            data = self._make_request(endpoint)
            
            # Update database
            if data:
                self.db.upsert_events(data)
            
            return data
        except Exception as e:
            print(f"Error fetching match events for {match_id}: {e}")
            return {}
    
    def scrape_and_save_all_data(self):
        """Main method to scrape all required data and save it locally and to database."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get all matches
        matches = self.get_league_matches()
        
        # Extract unique team IDs from matches
        team_ids = set()  # This would need to be populated based on the actual match data structure
        
        # Get team information
        teams_data = {}
        for team_id in team_ids:
            teams_data[team_id] = self.get_team_info(team_id)
        
        # Save team data
        with open(f"{self.data_dir}/teams_{timestamp}.json", "w") as f:
            json.dump(teams_data, f, indent=2)
        
        # Get match events for each match
        match_events = {}
        for match in matches:
            match_id = match.get("id")  # Adjust based on actual data structure
            if match_id:
                match_events[match_id] = self.get_match_events(match_id)
        
        # Save match events
        with open(f"{self.data_dir}/match_events_{timestamp}.json", "w") as f:
            json.dump(match_events, f, indent=2)
        
        # Convert to DataFrames for easier processing
        matches_df = pd.DataFrame(matches)
        teams_df = pd.DataFrame(teams_data).T
        
        # Save as CSV
        matches_df.to_csv(f"{self.data_dir}/matches_{timestamp}.csv", index=False)
        teams_df.to_csv(f"{self.data_dir}/teams_{timestamp}.csv", index=True)

if __name__ == "__main__":
    scraper = FotMobScraper()
    scraper.scrape_and_save_all_data() 