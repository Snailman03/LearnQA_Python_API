import json

from requests import Response


class Assertions:

    @staticmethod
    def assert_response_error(response: Response, expected_message=None,
                              expected_error=None, info_message=None):

        response_content_type = type(response.content)
        print(response_content_type)

        if isinstance(response_content_type, bytes):
            response_message = response.content.decode("utf-8")
            assert response_message == expected_message, f"we expected error - '{expected_message}'" \
                                                         f"but received {response_message}"
        if isinstance(response_content_type, dict):
            response_dict = response.json()
            print(response_dict)
            if 'error' in response_dict:
                actual_error = response_dict['error']
            elif 'success' in response_dict:
                actual_result = response_dict['success']

        assert actual_error == expected_error, f"we expected error - '{expected_error}'" \
                                               f"but received {actual_result}"
        assert actual_result == expected_message, f"we expected error - '{expected_error}'" \
                                                  f"but received {actual_result}"

    @staticmethod
    def assert_response_value_by_message_text(response: Response, expected_message=None,
                                              error_message=None):

        response_content_type = type(response.content)
        print(response_content_type)

        if isinstance(response_content_type, bytes):
            response_message = response.content.decode("utf-8")
            assert response_message == expected_message, error_message

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value,
                                  error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, (f"Response is not in JSON format. "
                           f"Response text is {response.text}")

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, (f"Response is not in JSON format. "
                           f"Response text is {response.text}")

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, (f"Response is not in JSON format. "
                           f"Response text is {response.text}")

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, (f"Response is not in JSON format. "
                           f"Response text is {response.text}")

        assert name not in response_as_dict, (f"Response JSON shouldn't have key {name},"
                                              f"but it is present")

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            (f"Unexpected status code {response.status_code}, "
             f"expected {expected_status_code}")

    @staticmethod
    def assert_parse_ua(response: Response, ua):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, (f"Response is not in JSON format. "
                           f"Response text is {response.text}")

        if ua == ("Mozilla/5.0 (Linux; U;"
                  " Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 "
                  "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"):

            expected_ua_1_dict = {
                'platform': 'Mobile',
                'browser': 'No',
                'device': 'Android'
            }
            for key in expected_ua_1_dict:
                # print(key)
                try:
                    assert response_as_dict[key] == expected_ua_1_dict[key]
                except AssertionError:
                    print(f"Incorrect parse '{key}' value for "
                          f"{ua} "
                          f"user agent")

        elif ua == ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) '
                    'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 '
                    'Mobile/15E148 Safari/604.1'):
            expected_ua_2_dict = {
                'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'
            }
            for key in expected_ua_2_dict:
                try:
                    assert response_as_dict[key] == expected_ua_2_dict[key]
                except AssertionError:
                    print(f"Incorrect parse '{key}' value for "
                          f"{ua} "
                          f"user agent")

        elif ua == ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'):
            expected_ua_3_dict = {
                'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'
            }
            for key in expected_ua_3_dict:
                try:
                    assert response_as_dict[key] == expected_ua_3_dict[key]
                except AssertionError:
                    print(f"Incorrect parse '{key}' value for "
                          f"{ua} "
                          f"user agent")

        elif ua == ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 '
                    'Safari/537.36 Edg/91.0.100.0'):
            expected_ua_4_dict = {
                'platform': 'Web', 'browser': 'Chrome', 'device': 'No'
            }
            for key in expected_ua_4_dict:
                try:
                    assert response_as_dict[key] == expected_ua_4_dict[key]
                except AssertionError:
                    print(f"Incorrect parse '{key}' value for "
                          f"{ua} "
                          f"user agent")

        elif ua == ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                    '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'):
            expected_ua_5_dict = {
                'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'
            }
            for key in expected_ua_5_dict:
                try:
                    assert response_as_dict[key] == expected_ua_5_dict[key]
                except AssertionError:
                    print(f"Incorrect parse '{key}' value for "
                          f"{ua} "
                          f"user agent")
