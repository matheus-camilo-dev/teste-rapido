from util.base_repository import BaseRepository
from psycopg2 import sql

class UserRepository(BaseRepository):
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def updateTokenExpiration(self, token, token_activate_at):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        UPDATE test_db.user 
                        SET token_activate_at = %s 
                        WHERE token = %s;
                        """), (token_activate_at, token))
            self.connection.commit()
            return {"message": "User Token Expiration was been updated sucessfully!", "data": {
                "token": token
            }}
        
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            self.connection.close()

    def insert(self, username, password, token, token_activate_at):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        INSERT INTO test_db.user 
                            (username, password, token, token_activate_at) 
                        VALUES 
                            (%s, %s, %s, %s) RETURNING id;
                        """), (username, password, token, token_activate_at))
            self.connection.commit()
            return {"message": "User was been insert sucessfully!", "data": {
                "token": token
            }}
        
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            self.connection.close()

    def selectOneBy(self, username, password):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        SELECT 
                            token, token_activate_at
                        FROM test_db.user
                        WHERE username = %s AND password = %s;
                        """), (username, password))

            user_record = cursor.fetchone()

            return {"data": user_record}

        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            self.connection.close()
    
    def getByToken(self, token : str):
        cursor = self.connection.cursor()
        try:
            a  = sql.SQL("""
                        SELECT 
                            token, token_activate_at
                        FROM test_db.user
                        WHERE token = %s;
                        """)
            
            cursor.execute("""
                        SELECT 
                            token, token_activate_at
                        FROM test_db.user
                        WHERE token = %s;
                        """, [str(token)])

            user_record = cursor.fetchone()

            return {"data": user_record}

        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            self.connection.close()