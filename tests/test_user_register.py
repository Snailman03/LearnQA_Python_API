import requests
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
# from datetime import datetime

class TestUserRegister(BaseCase):
    uncompleted_data_variants = [
        ('no_password'),
        ('no_username'),
        ('no_firstName'),
        ('no_lastName'),
        ('no_email')
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/",
                                 data=data)

        print(response.content)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(
            response,
            "id"
        )

    def test_create_user_with_exciting_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/",
                                 data = data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"user exists with email {email}"

    def test_create_user_with_incorrect_email(self):

        data = self.prepare_reg_data_incorrect_email()
        print(data['email'])

        response = MyRequests.post("/user/",
                                 data = data)
        print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format",\
            f"You try create user with incorrect email - '{data['email']}'"

    def test_create_user_with_short_username(self):

        data = self.prepare_reg_data_short_username()
        print(data['username'])

        response = MyRequests.post("/user/",
                                 data = data)
        print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short",\
             f"You try create user with very short username - '{data['username']}'"

    def test_create_user_with_long_name(self):

        data = self.prepare_reg_data_long_username()
        print(data['username'])

        response = MyRequests.post("/user/",
                                 data = data)
        print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long",\
              f"You try create user with very long username - '{data['username']}'"

    @pytest.mark.parametrize('uncompleted_data_variant',uncompleted_data_variants)
    def test_create_user_with_uncompleted_data(self,uncompleted_data_variant):

        data = self.prepare_reg_uncompleted_data(uncompleted_data_variant)
        print(data)

        response = MyRequests.post("/user/",
                                 data = data)
        print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {data['missed_param']}"