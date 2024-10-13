import dotenv
from flask import Flask, Response, request, jsonify
from os import environ

from models.product import Product
from services.product_service import ProductService
from services.user_service import UserService
from data.data_access_object import DataAccessObject
from data.product_repository import ProductRepository
from data.user_repository import UserRepository

dotenv.load_dotenv("environment/.env")

# Database Initial Setup
DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("POSTGRES_DB")
DB_USER = environ.get("POSTGRES_USER")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD")

# Setup Dependencies
data_access_object = DataAccessObject(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

user_repository = UserRepository(data_access_object)
user_service = UserService(user_repository)

product_repository = ProductRepository(data_access_object)
product_service = ProductService(product_repository)

app = Flask(__name__)

# Routes
## Health Check
@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"message": "Hello World!"}), 200

## User Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    result = user_service.insert_new_user(username, password)
    return jsonify(result), result["status_code"]

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    result = user_service.login_user_by(username, password)
    return jsonify(result), result["status_code"]

## Product Routes
@app.route('/api/products', methods=['GET'])
def selectAll():
    result = product_service.selectAll()
    return jsonify(result), result["status_code"]

@app.route('/api/products/<id>', methods=['GET'])
def selectOne(id:int):
    result = product_service.selectOneBy(id)
    return jsonify(result), result["status_code"]

@app.route('/api/products', methods=['POST'])
def insert():
    token = request.headers.get("token")

    if not user_service.validate_user_by_token(token):
        return jsonify({"message": "Not Authorized!"}), 401

    product : Product = request.get_json()

    result = product_service.insert(product)
    return jsonify(result), result["status_code"]

@app.route('/api/products/<id>', methods=['PUT'])
def update(id:int):
    # Autentication check
    token = request.headers.get("token")
    if not user_service.validate_user_by_token(token):
        return jsonify({"message": "Not Authorized!"}), 401

    product = request.get_json()

    result = product_service.update(id, product)
    return jsonify(result), result["status_code"]

@app.route('/api/products/<id>', methods=['DELETE'])
def delete(id:int):
    # Autentication check
    token = request.headers.get("token")
    if not user_service.validate_user_by_token(token):
        return jsonify({"message": "Not Authorized!"}), 401

    result = product_service.delete(id)
    return jsonify(result), result["status_code"]


if __name__ == '__main__':
    app.run(debug=True)