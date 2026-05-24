import psycopg2
from pprint import pprint

from utilities import get_db_conn

import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




#---------------------------------------------#
def get_match_ids():

	list_flat_match_ids = []


	conn = get_db_conn()
	curr = conn.cursor()

	query = "SELECT match_ids FROM top_players;"

	curr.execute(query)

	result = curr.fetchall()

	list_match_ids = []

	for tup in result:
		for item in tup[0]:
			list_match_ids.append(item)

	set_match_ids = set(list_match_ids)


	curr.close()
	conn.close()


	return set_match_ids



if __name__ == "__main__":
	get_match_ids()




