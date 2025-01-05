import requests
import pytest


class TestTwelveTask:

    def test_headers_parse(self):

        url = "https://playground.learnqa.ru/api/homework_header"


        response = requests.get(url)
        assert response.status_code == 200

        headers_dict = dict(response.headers)
        print (headers_dict)
        for key, value in headers_dict.items():
            print(f"{key}: {value}")
            current_key = key
            current_val = value
            assert 'x-secret-homework-header' in headers_dict, ("The response headers dict has not key "
                                                                "'x-secret-homework-header' ")

            if current_key == 'x-secret-homework-header':
                assert current_val == 'Some secret value', ("headers with key 'x-secret-homework-header' is"
                                                            "not equal 'x-secret-homework-header' ")
                break




