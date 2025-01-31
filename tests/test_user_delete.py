import requests
import pytest
import time
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from allure_commons.types import Severity


@allure.epic("API methods")
@allure.feature("Test user delete methods")
@allure.label("owner", "Ivan Mitin")
class TestUserDelete(BaseCase):
    special_id_list = [1, 2, 3, 4, 5]

    @allure.title("Try to delete user with special id")
    @allure.story("Try to delete user with special id [1 .. 5] requirements negative")
    @allure.description("Try to delete user with special id [1 .. 5] requirements negative")
    @allure.severity(Severity.NORMAL)
    def test_n_try_delete_user_with_special_id(self):
        # LOGIN AS USER WITH SPECIAL ID
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post("/user/login",
                                     data=data)
        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response_1, 'user_id')

        print(f"\n Data user with email = {data['email']} \n"
              f"auth_sid = {auth_sid},\ntoken = {token} \n"
              f"user id from auth method = {user_id_from_auth_method}")

        # TRY TO DELETE USER WITH SPECIAL ID
        if user_id_from_auth_method in self.special_id_list:
            response_2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                           headers={'x-csrf-token': token},
                                           cookies={'auth_sid': auth_sid}
                                           )

            Assertions.assert_code_status(response_2, 400)
            Assertions.assert_json_has_key(response_2, 'error')
            print(response_2.content)
            error_message = self.get_json_value(response_2, 'error')
            Assertions.assert_json_value_by_name(response_2, 'error',
                                                 error_message,
                                                 "incorrect mistake for try to delete special user action")

    @allure.title("Try to delete same user w/o authorization")
    @allure.story("Try to delete same user w/o authorization requirements negative")
    @allure.description("Try to delete same user w/o authorization requirements negative")
    @allure.severity(Severity.NORMAL)
    def test_n_try_delete_user_without_authorization(self):
        # REGISTER NEW USER AND GET HIS USER ID
        register_data = self.prepare_registration_data()

        response_1 = MyRequests.post("/user/",
                                     data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_1, "id")

        # TRY DELETE USER WITHOUT AUTHORIZATION

        response_2 = MyRequests.delete(f"/user/{user_id}"
                                       # headers = {'x-csrf-token': token}
                                       # cookies = {'auth_sid': auth_sid},
                                       )
        print(response_2.content)
        error_message = self.get_json_value(response_2, 'error')
        Assertions.assert_code_status(response_2, 400)
        Assertions.assert_json_value_by_name(response_2, 'error', error_message,
                                             f"Incorrect error message for delete without authorized action")

    @allure.title("Try to delete same user with authorization")
    @allure.story("Try to delete same user with authorization p")
    @allure.description("Try to delete same user with authorization positive")
    @allure.severity(Severity.CRITICAL)
    def test_p_delete_same_user_with_auth(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()

        response_1 = MyRequests.post("/user/",
                                     data=register_data)

        print(response_1.text)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response_2 = MyRequests.post("/user/login",
                                     data=login_data)
        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        # TRY DELETE SAME AUTHORIZED USER

        response_3 = MyRequests.delete(f"/user/{user_id}",
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid}
                                       )
        Assertions.assert_code_status(response_3, 200)

        # GET INFO ABOUT USER AFTER DELETE
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        print(response_4.content)
        expected_message = "User not found"
        Assertions.assert_code_status(response_4, 404)
        Assertions.assert_response_value_by_message_text(response_4, expected_message,
                                                         f"We get incorrect message after get "
                                                         f"deleted userr information")

    @allure.title("Try to delete another user with authorization")
    @allure.story("Try to delete another user with authorization req negative")
    @allure.description("Try to delete another user with authorization")
    @allure.severity(Severity.CRITICAL)
    def test_try_delete_data_by_another_auth_user(self):
        # CREATE FIRST RANDOM USER AND GET HIS USER_ID
        with allure.step("# CREATE FIRST RANDOM USER AND GET HIS USER_ID"):
            data_0 = self.prepare_registration_data()

            response_0 = MyRequests.post("/user/",
                                         data=data_0)
            random_first_user_id = self.get_json_value(response_0, 'id')
            print(random_first_user_id)
            print(response_0.json())
            Assertions.assert_code_status(response_0, 200)

        time.sleep(5)

        # REGISTER SECOND RANDOM USER
        register_data_2_user = self.prepare_registration_data()

        response_1 = MyRequests.post("/user/",
                                     data=register_data_2_user)

        print(response_1.text)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data_2_user['email']
        first_name = register_data_2_user['firstName']
        password = register_data_2_user['password']
        user_id_2 = self.get_json_value(response_1, "id")

        # LOGIN SECOND RANDOM USER
        login_data = {
            'email': email,
            'password': password
        }

        response_2 = MyRequests.post("/user/login",
                                     data=login_data)
        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        # TRY TO DELETE INFO BY FIRST RANDOM USER USE SECOND USER CREDENTIALS
        response_3 = MyRequests.delete(f"/user/{random_first_user_id}",
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid}
                                       )
        print(response_3.content)
        print(type(response_3.json()))

        Assertions.assert_json_has_key(response_3, "error")
        # assert error_message == f"This user can only delete their own account.", \
        #     f"incorrect message for attempt to delete another account action "
        Assertions.assert_code_status(response_3, 400)

        # CHECK THEN USER 1 IS EXIST

        response_4 = MyRequests.get(
            f"/user/{random_first_user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        print(response_4.content)
        Assertions.assert_json_value_by_name(
            response_4,
            "username",
            "learnqa",
            f"Wrong info about first user"
        )
