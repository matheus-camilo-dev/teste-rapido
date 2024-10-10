import psycopg2

class BaseRepository:
    def get_db_connection(db_host, db_name, db_user, db_password):
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        return conn