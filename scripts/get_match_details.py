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

	set_match_ids = get_match_ids()


	for match_id in tqdm(set_match_ids):

		sleep(0.5)

		URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"

		try:
			with requests.get(URL, headers=HEADERS) as response:
				response.raise_for_status()

				response_json = response.json()

				curr.execute(query, (match_id, Json(response_json)))


		except Exception as e:
			logger.error(f"_____ERROR_____: {e}")
			raise


if __name__ == "__main__":
	get_match_details()