-- Enable Row Level Security
ALTER DATABASE postgres SET "app.settings.jwt_secret" = 'your-jwt-secret';

-- Create tables with appropriate relationships
CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT,
    country TEXT,
    founded_year INTEGER,
    home_stadium TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE players (
    id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    nationality TEXT,
    birth_date DATE,
    height INTEGER,
    team_id TEXT REFERENCES teams(id),
    position TEXT,
    jersey_number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE matches (
    id TEXT PRIMARY KEY,
    competition_id TEXT NOT NULL,
    season TEXT NOT NULL,
    home_team_id TEXT REFERENCES teams(id),
    away_team_id TEXT REFERENCES teams(id),
    match_date TIMESTAMP WITH TIME ZONE,
    status TEXT,
    home_score INTEGER,
    away_score INTEGER,
    stadium TEXT,
    referee TEXT,
    attendance INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE events (
    id TEXT PRIMARY KEY,
    match_id TEXT REFERENCES matches(id),
    team_id TEXT REFERENCES teams(id),
    player_id TEXT REFERENCES players(id),
    event_type TEXT NOT NULL,
    minute INTEGER,
    second INTEGER,
    additional_time INTEGER,
    event_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX idx_matches_competition_season ON matches(competition_id, season);
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_events_match ON events(match_id);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_players_team ON players(team_id);

-- Enable Row Level Security on all tables
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Create policies for read access
CREATE POLICY "Enable read access for all users" ON teams
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON players
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON matches
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON events
    FOR SELECT USING (true);

-- Create policies for write access (only authenticated users)
CREATE POLICY "Enable insert for authenticated users only" ON teams
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable insert for authenticated users only" ON players
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable insert for authenticated users only" ON matches
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable insert for authenticated users only" ON events
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_teams_updated_at
    BEFORE UPDATE ON teams
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_players_updated_at
    BEFORE UPDATE ON players
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_matches_updated_at
    BEFORE UPDATE ON matches
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 