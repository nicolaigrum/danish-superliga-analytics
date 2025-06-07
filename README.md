# Danish Superliga Football Analytics Pipeline

This project creates an automated pipeline for collecting, storing, and analyzing Danish Superliga football data using FotMob, Supabase, and Streamlit.

## Setup Instructions

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SECRET_KEY=your_supabase_secret_key
```

4. Create a `.streamlit/secrets.toml` file with:
```toml
[supabase]
url = "your_supabase_url"
key = "your_supabase_anon_key"
```

## Project Structure

```
├── data/                  # Raw scraped data storage
├── scraper/              # FotMob scraping scripts
├── database/             # Supabase database schemas and scripts
├── dashboard/            # Streamlit dashboard files
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Components

1. **Data Scraping**: Python scripts to collect match, team, player, and event data from FotMob
2. **Data Storage**: Supabase PostgreSQL database with tables for matches, teams, players, and events
3. **Dashboard**: Streamlit web application for data visualization and analysis

## Usage

1. Run the scraper:
```bash
python scraper/fotmob_scraper.py
```

2. Run the Streamlit dashboard locally:
```bash
streamlit run dashboard/app.py
```

## Database Schema

The Supabase database includes the following tables:
- matches
- teams
- players
- events

Each table includes appropriate foreign key relationships and indexes for efficient querying.

## Automation

The data collection is automated using GitHub Actions, which runs the scraper daily and updates the Supabase database with new data.

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

MIT License 