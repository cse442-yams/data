import psycopg2 as pg
import json
import csv
from collections import defaultdict


def get_conn():
    return pg.connect(database="cse442", user="alex", host="localhost")

def insert_teams():
    statement = """
    INSERT INTO basketball.nba_teams (abbr, active, full_name, first_name, last_name, city, conference, division, state)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_conn() as conn:
        with conn.cursor() as cur, open("teams.json") as f:
            teams = json.load(f)
            teams_db = [(t["abbreviation"], t["active"], t['full_name'], t['first_name'], t['last_name'], t['city'], t['conference'], t['division'], t['state']) for t in teams]
            cur.executemany(statement, teams_db)

def insert_games():
    csv_id_to_db_id = {}
    db_ids = {}
    with open("nba-historical/nba_teams_all.csv") as f, get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, abbr FROM basketball.nba_teams")
            for id, abbr in cur.fetchall():
                db_ids[abbr] = id

        reader = csv.DictReader(f)
        for row in reader:
            if row["abbreviation"]:
                csv_id_to_db_id[row["team_id"]] = db_ids[row["abbreviation"]]

    team_games = defaultdict(dict)
    with open("nba-historical/nba_games_all.csv") as f, get_conn() as conn:
        reader = csv.DictReader(f)
        for row in reader:
            is_home = row["is_home"] == "t"
            team_games[row['game_id']]['home' if is_home else 'away'] = row





def main():
    insert_teams()

if __name__ == '__main__':
    main()



