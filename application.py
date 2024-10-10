import datetime
import hashlib
import dotenv
from flask import Flask, request, jsonify
from random import randint

from util.base_repository import BaseRepository
from util.product_repository import ProductRepository
from util.user_repository import UserRepository
from os import environ

app = Flask(__name__)

# Configurações do banco de dados
dotenv.load_dotenv("environment/.env")

DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")

def insert_user_in_db(username:str, password:str):
    previous_token = str(randint(0, 100)) + str(username) + str(password)
    token = hashlib.sha256(previous_token.encode()).hexdigest()[:20]
    token_activate_at = get_expiration_token_time()

    connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    userRepository = UserRepository(connection)
    
    result = userRepository.insert(username, password, token, token_activate_at)

    if result.get('error') is None:
        return jsonify(result), 500

    return jsonify(result), 201


def get_user_in_db(username:str, password:str):
    connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    userRepository = UserRepository(connection)

    result = userRepository.selectOneBy(username, password)
    return result


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if None in [username, password]:
        return jsonify({"error": "Name and email are required!"}), 400

    return insert_user_in_db(username, password)

def validateUserByToken(token):
    connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    userRepository = UserRepository(connection)

    result = userRepository.getByToken(token)

    if result.get("data") is not None:
        if isTokenValid(result.get("data")[1]):
            return True 
    
    return False 

def isTokenValid(token_activate_at: datetime.datetime) -> bool:
    return token_activate_at > datetime.datetime.now()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    if None in [username, password]:
        return jsonify({"error": "Name and email are required!"}), 400

    result = get_user_in_db(username, password)

    if result is None:
        return jsonify({"message": "User Not Found!"}), 404
    
    if result.get("data") is None:
        return jsonify(result), 500

    connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
    userRepository = UserRepository(connection)
    userRepository.updateTokenExpiration(result.get("data")[0], get_expiration_token_time())

    return jsonify({"message": "User was Found!", "data": {
            "token": result.get("data")[0]
        }}), 200

def get_expiration_token_time():
    return datetime.datetime.now() + datetime.timedelta(minutes=5)


@app.route('/teste', methods=['GET'])
def teste():
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     return jsonify({"message": "Hello World!"}), 200


# Products
@app.route('/api/products', methods=['GET'])
def selectAll():
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     result = productRepository.selectAll()

     if result is None:
         return jsonify({"message": "Products not Found!"}), 404

     return jsonify(result), 200

@app.route('/api/products/<id>', methods=['GET'])
def selectOne(id: int):
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     result = productRepository.selectOneBy(id)

     if result is None:
         return jsonify({"message": "Not Found!"}), 404

     return jsonify(result), 200

@app.route('/api/products', methods=['POST'])
def insert():
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     product = request.get_json()

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     result = productRepository.insert(product["name"], product["unit_price"], product["quantity"])

     if result is None:
         return jsonify({"message"}), 404

     return jsonify(result), 204

@app.route('/api/products/<id>', methods=['PUT'])
def update(id):
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     product = request.get_json()

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     saved_product = productRepository.selectOneBy(id)

     if saved_product is None:
         return jsonify({"message": "Product has not Found!"}), 400

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     result = productRepository.update(id, product["name"], product["unit_price"], product["quantity"])

     if result is None:
         return jsonify({"message": "Product has been not updated sucessfuly!"}), 404

     return jsonify(result), 200

@app.route('/api/products/<id>', methods=['DELETE'])
def delete(id):
     token = request.headers.get("token")

     if not validateUserByToken(token):
         return jsonify({"message": "Not Authorized!"}), 401

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     saved_product = productRepository.selectOneBy(id)

     if saved_product is None:
         return jsonify({"message": "Product has not Found!"}), 400

     connection = BaseRepository.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
     productRepository = ProductRepository(connection)
     result = productRepository.delete(id)

     if result is None:
         return jsonify({"message": "Product has been not deleted sucessfuly!"}), 404

     return jsonify(result), 204
     
if __name__ == '__main__':
    app.run(debug=True)
