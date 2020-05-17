CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name VARCHAR);

CREATE TABLE skills(
  id SERIAL PRIMARY KEY,
  name VARCHAR);

CREATE TABLE players_skills(
  id SERIAL PRIMARY KEY,
  player_id INTEGER REFERENCES players(id),
  skill_id INTEGER REFERENCES skills(id),
  strength INTEGER);

CREATE UNIQUE INDEX unique_skill_assignment on players_skills(player_id,skill_id);
CREATE UNIQUE INDEX unique_player_name on players(name);