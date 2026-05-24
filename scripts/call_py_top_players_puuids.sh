#!/bin/zsh

docker exec -i moba_games_analysis-postgres-1 psql -U admin -d postgres_db -c "TRUNCATE TABLE top_players;"

for league in "challengerleagues" "grandmasterleagues" "masterleagues"
do
	uv run python3 -m get_top_players_puuids --league $league
done