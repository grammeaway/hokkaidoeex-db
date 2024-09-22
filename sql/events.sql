CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    event_image_url VARCHAR(255) NOT NULL,
    venue_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL
);