

class SkillsRepository:
    def __init__(self, db):
        self._db = db

    def get_all_skills(self):
        with self._db.cursor() as cursor:
            cursor.execute("""
            SELECT id, name FROM skills;
            """)
            return [{'skill_id': row['id'], 'name': row['name']} for row in cursor]

    def get_skill_by_name(self,name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            SELECT id, name FROM skills WHERE name=%s;
            """, [name])
            row = cursor.fetchone()
            return {'skill_id': row['id'], 'name': row['name']}

    def add_skill(self, name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO skills(name) VALUES (%s);
            """, [name])

    def modify_name(self,skill_id, new_name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            UPDATE skills SET name=%s WHERE id=%s; 
            """, [new_name, skill_id])


class PlayersRepository:
    def __init__(self, db):
        self._db = db

    def get_player_by_name(self, name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            SELECT id, name FROM players WHERE name=%s;
            """, [name])
            row = cursor.fetchone()
            return {'player_id': row['id'], 'name': row['name'], 'skills': self.get_skills_from_player(row['id'])}

    def get_player_by_id(self, player_id):
        with self._db.cursor() as cursor:
            cursor.execute("""
            SELECT id, name FROM players WHERE id=%s;
            """, [player_id])
            row = cursor.fetchone()
            return {'player_id': row['id'], 'name': row['name'], 'skills': self.get_skills_from_player(row['id'])}

    def add_player(self, name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO players(name) VALUES (%s);
            """, [name])

    def modify_name(self,player_id, new_name):
        with self._db.cursor() as cursor:
            cursor.execute("""
            UPDATE players SET name=%s WHERE id=%s; 
            """, [new_name, player_id])

    def add_skill(self, player_id, skill_id, strength):
        with self._db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO players_skills(player_id,skill_id,strength) VALUES (%(player_id)s,%(skill_id)s,%(strength)s)
            ON CONFLICT (player_id,skill_id)
            DO UPDATE
            SET strength=%(strength)s
            """, {"player_id": player_id, "skill_id": skill_id, "strength": strength})

    def get_skills_from_player(self,player_id):
        with self._db.cursor() as cursor:
            cursor.execute("""
            SELECT skills.name as skill_name, players_skills.strength as strength
            FROM players_skills
            INNER JOIN skills
            ON (players_skills.skill_id=skills.id)
            WHERE players_skills.player_id=%s
            """,[player_id])
            return [{"name": row["skill_name"], "strength": row["strength"]} for row in cursor]

    def get_players(self):
        with self._db.cursor() as cursor:
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