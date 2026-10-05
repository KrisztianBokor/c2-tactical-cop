-- Enable PostGIS spatial capabilities
CREATE EXTENSION IF NOT EXISTS postgis;

-- Clean slate if re-running
DROP TABLE IF EXISTS asset_tracks;

-- Core telemetry and spatial table
CREATE TABLE asset_tracks (
    id BIGSERIAL PRIMARY KEY,
    track_id VARCHAR(32) NOT NULL,
    classification VARCHAR(16) NOT NULL CHECK (classification IN ('FRIENDLY', 'HOSTILE', 'UNKNOWN')),
    speed_knots NUMERIC(6, 2) DEFAULT 0.0,
    altitude_m NUMERIC(8, 2) DEFAULT 0.0,
    heading_deg NUMERIC(5, 2) DEFAULT 0.0,
    location GEOMETRY(Point, 4326) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spatial index (GiST) for fast bounding box and proximity searches
CREATE INDEX idx_asset_tracks_location ON asset_tracks USING GIST (location);

-- Index for fast per-track lookups and chronological ordering
CREATE INDEX idx_asset_tracks_track_time ON asset_tracks (track_id, recorded_at DESC);

-- Optional sample point (The Hague coordinates: Lon 4.3007, Lat 52.0705)
INSERT INTO asset_tracks (track_id, classification, speed_knots, altitude_m, heading_deg, location)
VALUES (
    'NATO-TRK-001',
    'FRIENDLY',
    420.50,
    8500.00,
    045.00,
    ST_SetSRID(ST_MakePoint(4.3007, 52.0705), 4326)
);