from models.user import User
from services.service_message import ServiceMessage
from data.base_repository import BaseRepository
from psycopg2 import sql

from data.data_access_object import DataAccessObject

class UserRepository(BaseRepository):

    def __init__(self, data_access_object : DataAccessObject):
        super().__init__(data_access_object)

    def updateTokenExpiration(self, token, token_activate_at) -> ServiceMessage:
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        UPDATE test_db.user 
                        SET token_activate_at = %s 
                        WHERE token = %s;
                        """), (token_activate_at, token))
            connection.commit()
            return ServiceMessage(success=True)
        
        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))

        finally:
            cursor.close()
            connection.close()


    def insert(self, user : User) -> ServiceMessage:
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        INSERT INTO test_db.user 
                            (username, password, token, token_activate_at) 
                        VALUES 
                            (%s, %s, %s, %s);
                        """), (user.username, user.password, user.token, user.token_activate_at))
            
            connection.commit()
            return ServiceMessage(success=True)
        
        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))

        finally:
            cursor.close()
            connection.close()


    def selectOneBy(self, username, password) -> ServiceMessage:
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        SELECT 
                            token, token_activate_at
                        FROM test_db.user
                        WHERE username = %s AND password = %s;
                        """), (username, password))

            user_record = cursor.fetchone()

            result_dict = None 
            if user_record is not None:           
                result_dict = {
                    "token" : user_record[0],
                    "token_activate_at" : user_record[1]
                }
            return ServiceMessage(success=True, data=result_dict)

        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))
        
        finally:
            cursor.close()
            connection.close()
    
    def getByToken(self, token : str):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            script =  sql.SQL(f"""
                        SELECT 
                            token, token_activate_at
                        FROM test_db.user
                        WHERE token = '{token}';
                        """)
            cursor.execute(script)

            user_record = cursor.fetchone()
            
            result_dict = {
                "token" : user_record[0],
                "token_activate_at" : user_record[1]
            }
            return ServiceMessage(success=True, data=result_dict)

        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))
        
        finally:
            cursor.close()
            connection.close()