import requests
import pytest

class TestElevenTask:


    def test_cookie_parse(self):

        url = ("https://playground.learnqa.ru/api/homework_cookie")


        response = requests.get(url)
        parse_cookie = response.cookies
        dict_cookie = dict(parse_cookie)
        current_cookie = response.cookies.get("HomeWork")
        print(dict_cookie)
        print(dict_cookie['HomeWork'])
        expected_result = "hm_value"
        actual_result = current_cookie
        assert response.status_code == 200, "Wrong response code"
        assert actual_result == expected_result ,"The actual cookie value is not equal hm_value"



