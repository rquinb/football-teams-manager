import os
from contextlib import closing


class BaseRepository:
    def __init__(self,db):
        self._db = db

    def initialize_db(self):
        files = os.listdir('sql')
        for file in files:
            with open(os.path.join(os.getcwd(), "sql", file), 'r') as sql_file:
                sql_script = sql_file.read()
                self._db.executescript(sql_script)


class SkillsRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    def get_all_skills(self):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            SELECT id, name FROM skills;
            """)
            return [{'skill_id': row['id'], 'name': row['name']} for row in cursor]

    def get_skill_by_name(self,name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            SELECT id, name FROM skills WHERE name=?;
            """, [name])
            row = cursor.fetchone()
            return {'skill_id': row['id'], 'name': row['name']}

    def add_skill(self, name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            INSERT INTO skills(name) VALUES (?);
            """, [name])

    def modify_name(self,skill_id, new_name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            UPDATE skills SET name=? WHERE id=?; 
            """, [new_name, skill_id])


class PlayersRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    def get_player_by_name(self, name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            SELECT id, name FROM players WHERE name=?;
            """, [name])
            row = cursor.fetchone()
            return {'player_id': row['id'], 'name': row['name'], 'skills': self.get_skills_from_player(row['id'])}

    def get_player_by_id(self, player_id):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            SELECT id, name FROM players WHERE id=?;
            """, [player_id])
            row = cursor.fetchone()
            return {'player_id': row['id'], 'name': row['name'], 'skills': self.get_skills_from_player(row['id'])}

    def add_player(self, name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            INSERT INTO players(name) VALUES (?);
            """, [name])

    def delete_player(self, id):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            DELETE FROM players WHERE id=?;
            """, [id])

    def modify_name(self, player_id, new_name):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            UPDATE players SET name=? WHERE id=?; 
            """, [new_name, player_id])

    def add_skill(self, player_id, skill_id, strength):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            INSERT INTO players_skills(player_id,skill_id,strength) VALUES (:player_id,:skill_id,:strength)
            ON CONFLICT (player_id,skill_id)
            DO UPDATE
            SET strength=:strength
            """, {"player_id": player_id, "skill_id": skill_id, "strength": strength})

    def get_skills_from_player(self,player_id):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("""
            SELECT skills.name as skill_name, players_skills.strength as strength
            FROM players_skills
            INNER JOIN skills
            ON (players_skills.skill_id=skills.id)
            WHERE players_skills.player_id=?
            """,[player_id])
            return [{"name": row["skill_name"], "strength": row["strength"]} for row in cursor]

    def get_players(self):
        with closing(self._db.cursor()) as cursor:
            cursor.execute("SELECT id, name FROM players;")
            players = [{"player_id": row["id"], "name": row["name"]} for row in cursor]
            for i, player in enumerate(players):
                skills = self.get_skills_from_player(player['player_id'])
                players[i]['skills'] = skills
            return players


class Player:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
