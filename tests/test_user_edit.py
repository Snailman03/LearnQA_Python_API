import pytest
import requests
import time
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from allure_commons.types import Severity


@allure.epic("API methods")
@allure.feature("Test user edit methods")
@allure.label("owner", "Ivan Mitin")
class TestUserEdit(BaseCase):
    incorrect_params = [
        ('incorrect_email'),
        ('incorrect_firstName')
    ]

    @allure.title("Test edit just created user")
    @allure.story("Test edit just created user")
    @allure.description("Test edit just created user")
    @allure.severity(Severity.NORMAL)
    def test_edit_just_created_user(self):
        # REGISTER
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

        # EDIT
        new_name = 'changed_Name'

        response_3 = MyRequests.put(f"/user/{user_id}",
                                    headers={'x-csrf-token': token},
                                    cookies={'auth_sid': auth_sid},
                                    data={'firstName': new_name}
                                    )
        Assertions.assert_code_status(response_3, 200)

        # GET
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_4,
            "firstName",
            new_name,
            f"Wrong user name after edit"
        )

    @allure.title("Test edit same not authorized user")
    @allure.story("Test edit same not authorized user")
    @allure.description("Test edit same not authorized user")
    @allure.severity(Severity.NORMAL)
    def test_edit_not_authorized_user(self):

        # REGISTER
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

        # EDIT
        new_name = 'changed_Name'

        response_3 = MyRequests.put(f"/user/{user_id}",
                                    # headers = {'x-csrf-token': token}
                                    # cookies = {'auth_sid': auth_sid},
                                    data={'firstName': new_name}
                                    )
        print(response_3.content)
        error_message = self.get_json_value(response_3, 'error')
        Assertions.assert_code_status(response_3, 400)
        assert error_message == f"Auth token not supplied", \
            f"You try edit data without authorized"

    @allure.title("Test try edit another user data by authorized user")
    @allure.story("Test try edit another user data by authorized user")
    @allure.description("Test try edit another user data by authorized user")
    @allure.severity(Severity.NORMAL)
    def test_try_edit_by_another_user(self):
        # CREATE RANDOM USER AND GET HIS USER_ID
        data_0 = self.prepare_registration_data()

        response_0 = MyRequests.post("/user/",
                                     data=data_0)
        random_user_id = self.get_json_value(response_0, 'id')
        print(random_user_id)
        print(response_0.json())
        Assertions.assert_code_status(response_0, 200)

        # LOGIN BY EXISTING USER
        data_1 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post("/user/login",
                                     data=data_1)
        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response_1, 'user_id')
        print(f"athorized user id {user_id_from_auth_method}")

        # TRY TO EDIT INFO BY RANDOM USER USE ANOTHER USER CREDENTIALS
        new_name = 'changed_Name'

        response_3 = MyRequests.put(f"/user/{random_user_id}",
                                    headers={'x-csrf-token': token},
                                    cookies={'auth_sid': auth_sid},
                                    data={'firstName': new_name}
                                    )
        print(response_3.content)
        Assertions.assert_code_status(response_3, 400)

    @allure.title("Test try edit another user data by authorized user with id not in [1..5]")
    @allure.story("Test try edit another user data by authorized user with id not in [1..5]")
    @allure.description("Test try edit another user data by authorized user with id not in [1..5]")
    @allure.severity(Severity.NORMAL)
    def test_try_edit_data_by_another_user_2(self):
        # CREATE FIRST RANDOM USER AND GET HIS USER_ID
        data_0 = self.prepare_registration_data()

        response_0 = MyRequests.post("/user/",
                                     data=data_0)
        random_first_user_id = self.get_json_value(response_0, 'id')
        print(random_first_user_id)
        print(response_0.json())
        Assertions.assert_code_status(response_0, 200)

        time.sleep(5)
        # REGISTER SECOND RANDOM USER
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

        # LOGIN SECOND RANDOM USER
        login_data = {
            'email': email,
            'password': password
        }

        response_2 = MyRequests.post("/user/login",
                                     data=login_data)
        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        # TRY TO EDIT INFO BY FIRST RANDOM USER USE SECOND USER CREDENTIALS
        new_name = 'changed_Name_222'

        response_3 = MyRequests.put(f"/user/{random_first_user_id}",
                                    headers={'x-csrf-token': token},
                                    cookies={'auth_sid': auth_sid},
                                    data={'firstName': new_name}
                                    )
        print(response_3.content)
        error_message = self.get_json_value(response_3, 'error')
        Assertions.assert_code_status(response_3, 400)
        assert error_message == f"This user can only edit their own data.", \
            f"You try edit data by another user"

    @allure.story("Test try edit incorrect user data by same user with auth")
    @allure.description("Test try edit incorrect user data by same user with auth")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize('incorrect_param', incorrect_params)
    @allure.title("Test try edit incorrect user data {incorrect_param} by same user with auth")
    def test_edit_incorrect_data_same_user(self, incorrect_param):
        # REGISTER
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

        # EDIT
        incorrect_firstname = 'c'
        incorrect_email = self.prepare_incorrect_email()

        if incorrect_param == 'incorrect_email':
            response_3 = MyRequests.put(f"/user/{user_id}",
                                        headers={'x-csrf-token': token},
                                        cookies={'auth_sid': auth_sid},
                                        data={'email': incorrect_email}
                                        )
            error_message = self.get_json_value(response_3, 'error')
            print(response_3.content)
            Assertions.assert_code_status(response_3, 400)
            error_message = self.get_json_value(response_3, 'error')
            assert error_message == f"Invalid email format", \
                f"Try set incorrect email for same user"

        elif incorrect_param == 'incorrect_firstName':
            response_3 = MyRequests.put(f"/user/{user_id}",
                                        headers={'x-csrf-token': token},
                                        cookies={'auth_sid': auth_sid},
                                        data={'firstName': incorrect_firstname}
                                        )

            print(response_3.content)
            error_message = self.get_json_value(response_3, 'error')
            assert error_message == f"The value for field `firstName` is too short", \
                f"Try set too short first name for same user"
            Assertions.assert_code_status(response_3, 400)
