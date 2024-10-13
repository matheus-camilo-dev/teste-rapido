from models.product import Product
from data.product_repository import ProductRepository

class ProductService:
    def __init__(self, product_repository : ProductRepository):
        self.product_repository = product_repository
    
    # Actions
    def selectAll(self):
        result = self.product_repository.selectAll()

        if not result.success:
            return { "error": result.error, "status_code": 404}
        return {"data": result.data, "status_code": 200 }
    
    def selectOneBy(self, id:str):
        # Input Validations
        if not str(id).isnumeric():
            return { "status_code": 400, "message": "id must be numeric!"}

        result = self.product_repository.selectOneBy(id)

        if not result.success:
            return { "error": result.error, "status_code": 404}
        return {"data": result.data, "status_code": 200 }

    def insert(self, product: Product):
        # Input Validations
        validation_errors = self.__get_product_input_validation_errors(product)
        if validation_errors is not None:
            return { "status_code": 400 , **validation_errors}

        result = self.product_repository.insert(product["name"], product["unit_price"], product["quantity"])

        if not result.success:
            return { "message": "Product has not been inserted!", "error": result.error, "status_code": 400 }
        return { "message": "Product has been inserted!", "status_code": 200 }

    def update(self, id:int, product: Product) -> dict:
        # Input Validations
        validation_errors = self.__get_product_input_validation_errors(product)
        if validation_errors is not None:
            return { "status_code": 400 , **validation_errors}

        saved_product = self.product_repository.selectOneBy(id)

        if not saved_product.success:
            return { "message": saved_product.error, "status_code": 404 }

        result = self.product_repository.update(id, product["name"], product["unit_price"], product["quantity"])
        
        if not result.success:
            return {"message": "Product has been not updated sucessfuly!", "status_code" : 400, "error": result.error}
        return {"message": "Product has been updated sucessfuly!", "status_code" : 200}

    def delete(self, id:int) -> dict:
        # Input Validations
        if not str(id).isnumeric():
            return { "status_code": 400, "message": "id must be numeric!"}

        saved_product = self.product_repository.selectOneBy(id)

        if not saved_product.success:
            return { "message": saved_product.error, "status_code": 404 }

        result = self.product_repository.delete(id)

        if not result.success:
            return {"message": "Product has been not deleted sucessfuly!", "status_code": 400, "error": result.error }

        return {
            "message": "Product has been deleted successfuly!",
            "status_code": 204
        }
    

    # Private Methods
    def __get_product_input_validation_errors(self, product: dict):
        name = product.get('name')
        unit_price = product.get('unit_price')
        quantity = product.get('quantity')

        if None in [name, unit_price, quantity]:
            return {
                "message": "name, unit_price and quantity are required!"
            }
        
        if [type(name), type(unit_price), type(quantity)] != [str, float, int]:
            return { 
                "message": "name, unit_price and quantity must be respectively text, decimal and numeric!"
            } 
        
        if len(name) > 20:
            return { 
                "message": "name must be a maximum of 20 characters in length!"
            }
        return None