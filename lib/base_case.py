import json

from requests import Response
from datetime import  datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert  cookie_name in response.cookies, (f"Cannot find cookie with name {cookie_name} "
                                                  f"in the last response")
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, (f"Cannot find header with the name {headers_name} "
                                                  f"in the last response")
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format.Response text is '{response.text}' "

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        return response_as_dict[name]

    def prepare_registration_data(self, email = None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

    def prepare_reg_data_incorrect_email(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"
        return {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

    def prepare_reg_data_short_username(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            "password": "123",
            "username": "l",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

    def prepare_reg_data_long_username(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        long_user_name = ''
        for x in range(251):
            long_user_name = long_user_name + 'a'
        print(long_user_name)
        print(len(long_user_name))
        return {
            "password": "123",
            "username": long_user_name,
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

    def prepare_reg_uncompleted_data(self, without_param:str):
        if without_param == 'no_password':
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
            return {
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email,
                "missed_param": "password"
            }

        elif without_param == 'no_username':
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"
            return {
                "password": "123",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email,
                "missed_param": "username"
            }
        elif without_param == 'no_firstName':
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"
            return {
                "password": "123",
                "username": "learnqa",
                "lastName": "learnqa",
                "email": email,
                "missed_param": "firstName"
            }
        elif without_param == 'no_lastName':
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"
            return {
                "password": "123",
                "username": "learnqa",
                "firstName": "learnqa",
                "email": email,
                "missed_param": "lastName"
            }

        elif without_param == 'no_email':
            return {
                "password": "123",
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "missed_param": "email"
            }