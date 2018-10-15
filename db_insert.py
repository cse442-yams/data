import psycopg2 as pg
import json
import csv
from collections import defaultdict
from datetime import datetime

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
            if row['w'] != "" and row["l"] != "" and row["game_date"] != "" and row["wl"] != "":
                is_home = row["is_home"] == "t"
                team_games[row['game_id']]['home' if is_home else 'away'] = row

    team_game_stmt = """
    INSERT INTO basketball.nba_team_games (team_id, is_home, result, current_wins, current_losses, fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, reb, ast, stl, blk, tov, pf, pts)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """

    game_stmt = """
    INSERT INTO basketball.nba_games (original_id, game_date, season_type, home_team_game_id, away_team_game_id, minutes)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for id, g in team_games.items():
        if g['home']['team_id'] not in csv_id_to_db_id or g['away']['team_id'] not in csv_id_to_db_id:
            continue
        with conn.cursor() as cur:
            cur.execute(team_game_stmt, _team_game_tuple(g['home'], csv_id_to_db_id))
            home_id = cur.fetchone()[0]

        with conn.cursor() as cur:
            cur.execute(team_game_stmt, _team_game_tuple(g['away'], csv_id_to_db_id))
            away_id = cur.fetchone()[0]

        h = g['home']
        game_tuple = (h['game_id'], datetime.strptime(h['game_date'], "%Y-%d-%M"), h['season_type'], home_id, away_id, h['min'])
        with conn.cursor() as cur:
            cur.execute(game_stmt, game_tuple)



def _team_game_tuple(r, team_ids):
    t = (team_ids[r['team_id']], r['is_home'], game_result(r['wl']), r['w'], r['l'], r['fgm'], r['fga'], r['fg3m'], r['fg3a'], r['ftm'], r['fta'], r['oreb'], r['dreb'], r['reb'], r['ast'], r['stl'], r['blk'], r['tov'], r['pf'], r['pts'])
    return t

def game_result(s):
    if s == "W":
        return "Win"
    if s == "L":
        return "Loss"
    else:
        raise ValueError




def main():
    # insert_teams()
    insert_games()

if __name__ == '__main__':
    main()



