import psycopg2




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