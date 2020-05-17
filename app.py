import os
import http
import logging
import flask
import psycopg2.extensions
import psycopg2.extras
import entities

# DB credentials
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'admin')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', str(5432))
DB_SCHEMA = os.getenv('DB_SCHEMA', 'football-teams')
db = psycopg2.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT,database=DB_SCHEMA,
                      cursor_factory=psycopg2.extras.DictCursor)
psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
db.autocommit = True

app = flask.Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

players_repository = entities.PlayersRepository(db)
skills_repository = entities.SkillsRepository(db)

@app.route("/")
def main_page():
    return flask.render_template("index.html")


@app.route("/creador-de-equipos/")
def teams_creator_page():
    return flask.render_template("teams_creator.html")


@app.route("/player/", methods=['POST'])
def add_player():
    body = flask.request.get_json()
    player_name = body['name']
    try:
        players_repository.add_player(player_name)
    except Exception:
        logging.info(f'Player {player_name} already added to database')
    player = players_repository.get_player_by_name(player_name)
    for skill in body["skills"]:
        players_repository.add_skill(player['player_id'],skill['id'], skill['strength'])
    return {}, http.HTTPStatus.CREATED


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
