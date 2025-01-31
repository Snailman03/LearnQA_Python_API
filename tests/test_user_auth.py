import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from allure_commons.types import Severity


@allure.epic("API methods")
@allure.feature("Test user authentication methods")
class TestUserAuth(BaseCase):
    url_user_auth = "https://playground.learnqa.ru/api/user/auth"
    url_send_lp = "https://playground.learnqa.ru/api/user/login"

    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    @allure.title("Set up method send email ,password/ get auth_sid, token, user_id")
    @allure.story("Set up method send email ,password/ get auth_sid, token, user_id")
    @allure.description("Set up method send email ,password/ get auth_sid, token, user_id")
    @allure.severity(Severity.CRITICAL)
    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")

    @allure.title("Test user auth with correct auth cookie and token")
    @allure.story("This test checks authorization status with sending correct auth cookie and token")
    @allure.description("This test checks authorization status with sending correct auth cookie and token")
    @allure.severity(Severity.CRITICAL)
    def test_auth_user(self):

        response_2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method "
            "is not equal to user id from check method"
        )

    @allure.story("This test checks authorization status w/o sending auth cookie or token")
    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    @allure.title("This test checks authorization status w/o sending {'condition'}")
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response_2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            response_2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response_2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"

        )
