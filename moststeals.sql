/* Orders table from team with the most steals to least amount of steals */
CREATE FUNCTION BestStealsTeam()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY stl DESC;