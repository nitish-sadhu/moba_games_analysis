from psycopg2.extras import execute_values
import psycopg2
from tqdm import tqdm
import pandas as pd 
import requests
import argparse
import time

from headers import HEADERS
from utilities import get_db_conn

import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





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
			
			for each_dict in tqdm(response_json_entries):
				list_puuids.append(each_dict["puuid"])

			#print(list_puuids[:3])

	except Exception as e:
		logger.error(f"___EXCEPTION___: {e}")
		raise


	return list_puuids



#---------------------------------------------#
def get_top_players_match_ids(puuid: list) -> list:

	list_match_ids = []

	URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20"

	try:
		print("_______getting match_ids_______")

		with requests.get(URL, headers=HEADERS) as response:
			response.raise_for_status()

			list_match_ids = list(response.json())

	except Exception as e:
		logger.error(f"___EXCEPTION___: {e}")
		raise

	print(list_match_ids)

	return list_match_ids



#---------------------------------------------#
def assemble_details(league: str, region: str) -> list:

	list_details = []
	list_match_ids = []

	list_puuids = get_top_players_puuids(league, region)

	print(f"_______total puuids_______: {len(list_puuids)}")

	for puuid in tqdm(list_puuids):
		print(f"_________PUUID_________: {puuid}")
		list_match_ids.append(get_top_players_match_ids(puuid))
		time.sleep(0.5)

	for i in range(len(list_puuids)):
		list_details.append((list_puuids[i], league, list_match_ids[i]))

	return list_details



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

	list_details = assemble_details(league, region)

	try:
		execute_values(curr, query, list_details)

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



