from data.data_access_object import DataAccessObject

class BaseRepository:
    def __init__(self, data_access_object : DataAccessObject):
        self.data_access_object = data_access_object
        self.table_scheme = data_access_object.DB_NAME 

    def get_db_connection(self):
        return self.data_access_object.get_db_connection()