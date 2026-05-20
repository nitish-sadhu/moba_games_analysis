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
def list_top_players_puuids(league: str, region: str) -> list:

	puuids_list = []

	if league not in {"challengerleagues", "grandmasterleagues", "masterleagues"}:
		raise 


	URL = f"https://{region}.api.riotgames.com/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5"


	try:
		with requests.get(URL, headers=HEADERS) as response:
			response.raise_for_status()

			response_json = response.json()

			response_json_entries = response_json["entries"]
			
			for each_dict in response_json_entries:
				puuids_list.append((each_dict["puuid"], str(league)))

	except Exception as e:
		logger.error(f"Exception: {e}")
		raise


	return puuids_list



#---------------------------------------------#
def insert_top_players_puuids(league: str, region: str) -> None:

	conn = get_db_conn()
	curr = conn.cursor()

	puuids_list = list_top_players_puuids(league, region)

	query = """
		INSERT INTO top_players (
				puuid,
				league
			)
		VALUES %s
	"""
	try:
		curr.execute("TRUNCATE TABLE top_players;")
		execute_values(curr, query, puuids_list)

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





