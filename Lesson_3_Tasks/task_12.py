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
            if current_key == 'x-secret-homework-header':
                assert current_val == 'Some secret value'
                break




