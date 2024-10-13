import psycopg2


class DataAccessObject:
    def __init__(self, db_host: str, db_name : str, db_user : str, db_password : str):
        self.DB_HOST = db_host
        self.DB_NAME = db_name
        self.DB_USER = db_user
        self.DB_PASSWORD = db_password
    
    def get_db_connection(self):
        return psycopg2.connect(
            host=self.DB_HOST,
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD
        )