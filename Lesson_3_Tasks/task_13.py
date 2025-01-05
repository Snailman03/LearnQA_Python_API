import requests
import pytest

class TestThirteenTask:
    user_agents = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
    ]

    @pytest.mark.parametrize('user_agent', user_agents)
    def test_user_agent_parse(self, user_agent):

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        response = requests.get(url, headers={"User-Agent": user_agent})
        response_dict = response.json()
        assert response.status_code == 200
        list_incorrect_parse_ua = []

        if user_agent == ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) '
                          'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'):
            try:
                assert response_dict['platform'] == 'Mobile', \
                    "Wrong parse value for 'platform' key"
                assert response_dict['browser'] == 'No', \
                    "Wrong parse value for 'browser' key"
                assert response_dict['device'] == 'Android', \
                    "Wrong parse value for 'device' key"
            except AssertionError:
                list_incorrect_parse_ua.append(user_agent)

        elif user_agent == ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) '
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'):
            try:
                assert response_dict['platform'] == 'Mobile', \
                    "Wrong parse value for 'platform' key"
                assert response_dict['browser'] == 'Chrome', \
                    "Wrong parse value for 'browser' key"
                assert response_dict['device'] == 'iOS', \
                    "Wrong parse value for 'device' key"
            except AssertionError:
                list_incorrect_parse_ua.append(user_agent)

        elif user_agent == 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)':
            try:
                assert response_dict['platform'] == 'Googlebot', \
                    "Wrong parse value for 'platform' key"
                assert response_dict['browser'] == 'Unknown', \
                    "Wrong parse value for 'browser' key"
                assert response_dict['device'] == 'Unknown', \
                    "Wrong parse value for 'device' key"
            except AssertionError:
                list_incorrect_parse_ua.append(user_agent)

        elif user_agent == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0':
            try:
                assert response_dict['platform'] == 'Web', \
                    "Wrong parse value for 'platform' key"
                assert response_dict['browser'] == 'Chrome', \
                    "Wrong parse value for 'browser' key"
                assert response_dict['device'] == 'No', \
                    "Wrong parse value for 'device' key"
            except AssertionError:
                list_incorrect_parse_ua.append(user_agent)

        elif user_agent == 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1':
            try:
                assert response_dict['platform'] == 'Mobile', \
                    "Wrong parse value for 'platform' key"
                assert response_dict['browser'] == 'No', \
                    "Wrong parse value for 'browser' key"
                assert response_dict['device'] == 'iPhone', \
                    "Wrong parse value for 'device' key"
            except AssertionError:
                list_incorrect_parse_ua.append(user_agent)

        print(list_incorrect_parse_ua)





