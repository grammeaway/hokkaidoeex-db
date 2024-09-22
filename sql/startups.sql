CREATE TABLE startups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pitcher_name VARCHAR(255) NOT NULL,
    description_brief TEXT NOT NULL,
    description_long TEXT NOT NULL,
    logo_url VARCHAR(255) NOT NULL,
    twitter VARCHAR(255),
    linkedin VARCHAR(255),
    website VARCHAR(255),
    instagram VARCHAR(255),
    pitch_order INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    currently_pitching BOOLEAN DEFAULT FALSE,
    -- Foreign key references
    event_id INTEGER REFERENCES events(id)
);