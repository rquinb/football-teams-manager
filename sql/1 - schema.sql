CREATE TABLE IF NOT EXISTS players(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    UNIQUE(name));

CREATE TABLE IF NOT EXISTS skills(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    UNIQUE(name));

CREATE TABLE IF NOT EXISTS players_skills(
    player_id INTEGER REFERENCES players(id),
    skill_id INTEGER REFERENCES skills(id),
    strength INTEGER,
    PRIMARY KEY (player_id, skill_id)
    );

CREATE UNIQUE INDEX IF NOT EXISTS unique_skill_assignment on players_skills(player_id,skill_id);
CREATE UNIQUE INDEX IF NOT EXISTS unique_player_name on players(name);
CREATE UNIQUE INDEX IF NOT EXISTS unique_skills_name on skills(name);