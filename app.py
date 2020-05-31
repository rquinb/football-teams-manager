import os
import http
import logging
import flask
import entities
import sqlite3

db = sqlite3.connect(os.path.join(os.getcwd(), "db.sqlite3"),check_same_thread=False,isolation_level=None)
db.row_factory = sqlite3.Row
app = flask.Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
base_repository = entities.BaseRepository(db)
base_repository.initialize_db()
players_repository = entities.PlayersRepository(db)
skills_repository = entities.SkillsRepository(db)

@app.route("/")
def main_page():
    return flask.render_template("homepage.html")

@app.route("/registro-de-jugadores")
def register_page():
    return flask.render_template("newfulluser.html")

@app.route("/administrador-de-jugadores")
def players_page():
    return flask.render_template("players.html")


@app.route("/creador-de-equipos/")
def teams_creator_page():
    return flask.render_template("teams_creator.html")


@app.route("/skills/", methods=['GET'])
def get_all_skills():
    skills = skills_repository.get_all_skills()
    return flask.jsonify({"data": skills})


@app.route("/players/", methods=['POST'])
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


@app.route("/players/", methods=["GET"])
def get_all_players():
    players = players_repository.get_players()
    return flask.jsonify({"data":players})


@app.route("/players/<int:player_id>/")
def get_player(player_id):
    player = players_repository.get_player_by_id(player_id)
    if player is not None:
        return flask.jsonify({"data": player})
    else:
        raise http.HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
