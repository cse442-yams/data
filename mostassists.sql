/* Orders table from team with the most assists to least amount of assists */
CREATE FUNCTION BestAssistsTeam()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY ast DESC;