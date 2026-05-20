#!/bin/zsh


for league in "challengerleagues" "grandmasterleagues" "masterleagues"
do
	uv run python3 -m get_top_players_puuids --league $league
done