from psycopg2.extras import Json
from pprint import pprint
from time import sleep
from tqdm import tqdm
import requests

from get_match_ids import get_match_ids
from utilities import get_db_conn
from headers import HEADERS

import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



#---------------------------------------------#
def get_existing_match_details(curr) -> set:

	list_exist_match_ids = []

	fetch_query = """
		SELECT match_id FROM raw_match_details
	"""

	curr.execute(fetch_query)

	temp_list = curr.fetchall()

	for item in temp_list:
		list_exist_match_ids.append(item[0])

	pprint(list_exist_match_ids)

	set_existing_match_ids = set(list_exist_match_ids)


	return set_existing_match_ids



#---------------------------------------------#
def get_match_details():

	conn = get_db_conn()
	curr = conn.cursor()

	query = """
		INSERT INTO raw_match_details (
				match_id,
				match_details
			)
		VALUES (%s, %s)
		ON CONFLICT (match_id) DO NOTHING;
	"""

	set_existing_match_ids = get_existing_match_details(curr)
	set_match_ids = get_match_ids()

	set_missing_match_ids = set_match_ids - set_existing_match_ids

	#pprint(set_missing_match_ids)
	print("#---------------------------------------------#")
	print("length: set_missing_match_ids: ",len(set_missing_match_ids))
	print("length: set_match_ids: ", len(set_match_ids))
	print("length: set_existing_match_ids: ", len(set_existing_match_ids))
	print("#---------------------------------------------#")


	for match_id in tqdm(set_missing_match_ids):

		sleep(1.2)

		URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"

		try:
			with requests.get(URL, headers=HEADERS) as response:
				response.raise_for_status()

				response_json = response.json()

				#pprint(response_json)

				curr.execute(query, (match_id, Json(response_json)))
				conn.commit()


		except Exception as e:
			logger.error(f"_____ERROR_____: {e}")
			raise


	return None



if __name__ == "__main__":
	get_match_details()