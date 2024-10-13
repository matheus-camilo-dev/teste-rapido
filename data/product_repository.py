from psycopg2 import sql

from data.base_repository import BaseRepository
from data.data_access_object import DataAccessObject
from services.service_message import ServiceMessage


class ProductRepository(BaseRepository):
    def __init__(self, data_access_object : DataAccessObject):
        super().__init__(data_access_object)
    
    def selectAll(self):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL(f"""
                        SELECT 
                            id, name, unit_price, quantity
                        FROM {self.table_scheme}.product;
                        """))

            user_record = cursor.fetchall()

            if user_record is None or user_record  == []:
                return ServiceMessage(success=False, error="Products not Found!")

            result = []

            for item in user_record:
                result.append({
                    "id": item[0],
                    "name": item[1],
                    "unit_price": item[2],
                    "quantity": item[3]
                })

            return ServiceMessage(success=True, data=result)

        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))
        
        finally:
            cursor.close()
            connection.close()
    
    def selectOneBy(self, id:int):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL(f"""
                        SELECT 
                            id, name, unit_price, quantity
                        FROM {self.table_scheme}.product
                        WHERE id = {id};
                        """))

            user_record = cursor.fetchone()

            if user_record is None:
                return ServiceMessage(success=False, error="Product not Found!")

            return ServiceMessage(success=True, data={
                    "id": user_record[0],
                    "name": user_record[1],
                    "unit_price": user_record[2],
                    "quantity": user_record[3]
                })

        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))
        
        finally:
            cursor.close()
            connection.close()
    
    def insert(self, name:str, unit_price, quantity:int) -> ServiceMessage:
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL(f"""
                        INSERT INTO {self.table_scheme}.product 
                            (name, unit_price, quantity) 
                        VALUES 
                            ('{name}', {unit_price}, {quantity});
                        """))
            connection.commit()
            return ServiceMessage(success=True)
        
        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))

        finally:
            cursor.close()
            connection.close()
    
    def update(self, id:int, name:str, unit_price, quantity:int):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL(f"""
                        UPDATE {self.table_scheme}.product 
                        SET name = '{name}', unit_price = '{unit_price}', quantity = '{quantity}' 
                        WHERE id = '{id}';
                        """))
            connection.commit()
            return ServiceMessage(success=True)
        
        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))

        finally:
            cursor.close()
            connection.close()

    def delete(self, id:int):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL(f"""
                        DELETE FROM {self.table_scheme}.product 
                        WHERE id = {id};
                        """))
            connection.commit()
            return ServiceMessage(success=True)
        
        except Exception as e:
            connection.rollback()
            return ServiceMessage(success=False, error=str(e))

        finally:
            cursor.close()
            connection.close()