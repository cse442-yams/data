/* Orders table from team with the most rebounds to least amount of rebounds */
CREATE FUNCTION BestReboundingTeam()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY reb DESC;