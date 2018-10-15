/* Orders table from team with the most 3 pointers to least amount of 3 pointers */
CREATE FUNCTION Best3team()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY fg3a DESC;