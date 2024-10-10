from util.base_repository import BaseRepository
from psycopg2 import sql

class ProductRepository(BaseRepository):
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
    
    def delete(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        DELETE FROM test_db.product 
                        WHERE id = %s;
                        """), (id))
            self.connection.commit()
            return {"message": "Product was been updeleteddated sucessfully!"}
        
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            self.connection.close()

    def update(self, id, name, unit_price, quantity):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        UPDATE test_db.product 
                        SET name = %s, unit_price = %s, quantity = %s 
                        WHERE id = %s;
                        """), (name, unit_price, quantity, id))
            self.connection.commit()
            return {"message": "Product was been updated sucessfully!"}
        
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            self.connection.close()

    def selectAll(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        SELECT 
                            id, name, unit_price, quantity
                        FROM test_db.product;
                        """))

            user_record = cursor.fetchall()

            if user_record is None or user_record  == []:
                return None

            result = []

            for item in user_record:
                result.append({
                    "id": item[0],
                    "name": item[1],
                    "unit_price": item[2],
                    "quantity": item[3]
                })

            return {"data": result}

        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            self.connection.close()
    
    def selectOneBy(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        SELECT 
                            id, name, unit_price, quantity
                        FROM test_db.product
                        WHERE id = %s;
                        """), (str(id)))

            user_record = cursor.fetchone()

            if user_record is None:
                return user_record

            return {"data": {
                    "id": user_record[0],
                    "name": user_record[1],
                    "unit_price": user_record[2],
                    "quantity": user_record[3]
                }}

        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            self.connection.close()
    
    def insert(self, name, unit_price, quantity):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                sql.SQL("""
                        INSERT INTO test_db.product 
                            (name, unit_price, quantity) 
                        VALUES 
                            (%s, %s, %s) RETURNING id;
                        """), (name, unit_price, quantity))
            self.connection.commit()
            return {"message": "Product was been insert sucessfully!"}
        
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            self.connection.close()