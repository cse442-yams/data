/* Orders table from team with the most points scored to least amount of points scored */
CREATE FUNCTION BestOffensiveTeam()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY pts DESC;