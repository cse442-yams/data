/* Orders table from team with the most blocks to least amount of blocks */
CREATE FUNCTION BestBlocksTeam()
RETURNS TABLE
AS
RETURN
    SELECT *
    FROM basketball.nba_team_games
    ORDER BY blk DESC;