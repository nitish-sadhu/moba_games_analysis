#!/bin/zsh

export PROJECT_NAME="moba_games_analysis"

cd ..
pwd

docker compose up -d

sleep 10

docker exec -i "${PROJECT_NAME}-postgres-1" psql -U admin -d postgres_db <<EOF
CREATE TABLE IF NOT EXISTS top_players (
	puuid VARCHAR(80) PRIMARY KEY,
	league VARCHAR(25),
	match_ids TEXT[]
);
EOF

cd -

pwd

(crontab -l 2>/dev/null; echo "0 0 * * * /Users/krishnasadhu/${PROJECT_NAME}/scripts/call_py_top_players_puuids.sh") | crontab -
