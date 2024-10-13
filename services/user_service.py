import datetime
import hashlib
from random import randint
from models.user import User
from data.user_repository import UserRepository


class UserService:
    def __init__(self, userRepository : UserRepository):
        self.userRepository = userRepository
        self.token_expiration_time_in_minutes = 5
    
    # Actions
    def insert_new_user(self, username: str, password: str) -> dict:
        # Input Validations
        validation_errors = self.__get_user_input_validation_errors(username, password);
        if validation_errors is not None:
            return { "status_code": 400, **validation_errors}

        # Token
        token = self.__get_generated_token(username, password)
        token_activate_at = self.__get_expiration_token_time()

        password = self.__encrypt_content(password)

        user_result = self.userRepository.selectOneBy(username, password)
        if user_result.success and user_result.data is not None:
            return {
                "status_code": 400,
                "message": "User Already Exists!"
            }

        user = User(username, password, token, token_activate_at)

        result = self.userRepository.insert(user)

        if result.success:
            return {
                "status_code": 201, 
                "message": "User was been insert sucessfully!"
            }
        else:
            return {
                "status_code": 400,
                "message": "User was been not insert sucessfully!", 
                "error": result.error
            }
    
    def login_user_by(self, username: str, password: str) -> dict:
        # Input Validations
        validation_errors = self.__get_user_input_validation_errors(username, password);
        if validation_errors is not None:
            return { "status_code": 400 , **validation_errors }
        
        password = self.__encrypt_content(password)

        user_result = self.userRepository.selectOneBy(username, password)

        if not user_result.success or user_result.data is None:
            return {
                "status_code": 400,
                "message": "User not Found!", 
                "error": user_result.error
            }
    
        user_result.data["token_activate_at"] = self.__get_expiration_token_time() 

        result = self.userRepository.updateTokenExpiration(user_result.data["token"], user_result.data["token_activate_at"])

        if result.success:
            return {
                "status_code": 200, 
                "message": "User is Logged!",
                "data": user_result.data
            }
        else:
            return {
                "status_code": 400, 
                "message": "User is not Logged!",
                "error": result.error
            }

    def validate_user_by_token(self, token:str):
        result = self.userRepository.getByToken(token)

        if result.success and result.data is not None:
            return self.__is_token_valid(result.data["token_activate_at"])
        return False 
    

    # Private Methods
    def __encrypt_content(self, content:str) -> str:
        return hashlib.sha256(content.encode()).hexdigest() 

    def __get_expiration_token_time(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(minutes=self.token_expiration_time_in_minutes)

    def __get_generated_token(self, username : str, password : str) -> str:
        return self.__encrypt_content(str(randint(0, 100)) + str(username) + str(password))
    
    def __is_token_valid(self, token_activate_at: datetime.datetime) -> bool:
        return token_activate_at > datetime.datetime.now()
    
    def __get_user_input_validation_errors(self, username: str, password:str):
        if None in [username, password]:
            return {
                "message": "username and password are required!"
            }
        
        if [type(username), type(password)] != [str, str]:
            return { 
                "message": "username and password must be text"
            } 
        
        if len(username) > 20:
            return { 
                "message": "username must be a maximum of 20 characters in length!"
            }

        if len(password) > 8 or len(password) < 6:
            return { 
                "message": "password must have between 6 and 8 characters!"
            }
        return None