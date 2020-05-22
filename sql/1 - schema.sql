CREATE TABLE IF NOT EXISTS players(
    id SERIAL PRIMARY KEY,
    name VARCHAR);

CREATE TABLE IF NOT EXISTS skills(
    id SERIAL PRIMARY KEY,
    name VARCHAR);

CREATE TABLE IF NOT EXISTS players_skills(
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    skill_id INTEGER REFERENCES skills(id),
    strength INTEGER);

CREATE UNIQUE INDEX IF NOT EXISTS unique_skill_assignment on players_skills(player_id,skill_id);
CREATE UNIQUE INDEX IF NOT EXISTS unique_player_name on players(name);