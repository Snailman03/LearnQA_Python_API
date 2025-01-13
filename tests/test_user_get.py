import requests

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from tests.test_user_register import TestUserRegister

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')
        # print(response.content)

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')
        Assertions.assert_json_has_no_key(response, 'email')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email':'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post("/user/login",
                                   data = data)
        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response_1,'user_id')

        response_2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
            )

        expected_fields = ["username","email","firstName","lastName"]

        Assertions.assert_json_has_keys(response_2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):

        #CREATE RANDOM USER AND GET HIS USER_ID
        data_0 =  self.prepare_registration_data()

        response_0 = MyRequests.post("/user/",
                                 data=data_0)
        random_user_id = self.get_json_value(response_0,'id')
        print(random_user_id)
        print(response_0.json())
        Assertions.assert_code_status(response_0,200)

        #LOGIN BY EXISTING USER
        data_1 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post("/user/login",
                                     data=data_1)
        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')
        # user_id_from_auth_method = self.get_json_value(response_1, 'user_id')

        # TRY TO GET INFO BY RANDOM USER USE ANOTHER USER CREDENTIALS
        response_2 = MyRequests.get(
            f"/user/{random_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username"]
        print(response_2.json())

        Assertions.assert_json_has_keys(response_2, expected_fields)