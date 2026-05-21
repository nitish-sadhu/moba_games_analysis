import pandas as pd 
import psycopg2
from psycopg2.extras import execute_values
import requests
import argparse

from headers import HEADERS

import logging 



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




#---------------------------------------------#
def get_db_conn():

	conn = psycopg2.connect(
			host="localhost",
			port=5432,
			database="postgres_db",
			user="admin",
			password="admin_password"
		)

	return conn 



#---------------------------------------------#
def get_top_players_puuids(league: str, region: str) -> list:

	list_puuids = []

	if league not in {"challengerleagues", "grandmasterleagues", "masterleagues"}:
		raise 


	URL = f"https://{region}.api.riotgames.com/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5"


	try:
		with requests.get(URL, headers=HEADERS) as response:
			response.raise_for_status()

			response_json = response.json()

			response_json_entries = response_json["entries"]
			
			for each_dict in response_json_entries:
				list_puuids.append((each_dict["puuid"], str(league), get_top_players_match_details(each_dict["puuid"])))

	except Exception as e:
		logger.error(f"___EXCEPTION___: {e}")
		raise


	return list_puuids



#---------------------------------------------#
def get_top_players_match_details(puuid: str) -> list:

	URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20"

	try:
		with requests.get(URL, headers=HEADERS) as response:
			response.raise_for_status()

			list_match_ids = response.json()

	except Exception as e:
		logger.error(f"___EXCEPTION___: {e}")


	return list_match_ids



#---------------------------------------------#
def insert_top_players_puuids(league: str, region: str) -> None:

	conn = get_db_conn()
	curr = conn.cursor()


	query = """
		INSERT INTO top_players (
				puuid,
				league,
				match_ids
			)
		VALUES %s
	"""

	list_puuids = get_top_players_puuids(league, region)

	try:
		curr.execute("TRUNCATE TABLE top_players;")
		execute_values(curr, query, list_puuids)

	except Exception as e:
		logger.error(f"Exception: {e}")
		raise


	conn.commit()
	curr.close()
	conn.close()


	return None



#---------------------------------------------#
def main() -> None:

	parser = argparse.ArgumentParser()

	parser.add_argument("--league", type=str, required=True)
	parser.add_argument("--region", type=str, default="jp1")

	args = parser.parse_args()


	insert_top_players_puuids(args.league, args.region)


	return None



#---------------------------------------------#
#---------------------------------------------#
if __name__ == "__main__":

	main()





