/* Orders table from team with the most wins to least wins */
CREATE FUNCTION BestForm()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY current_wins DESC;
