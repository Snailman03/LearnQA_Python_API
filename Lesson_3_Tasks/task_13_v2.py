import requests
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestThirteenTask(BaseCase):
    user_agents = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
    ]
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

    ua_1 = ("Mozilla/5.0 (Linux; U;"
            " Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 "
            "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")

    def test_ua_1(self):
        # Get object with type Response.
        # We could work with it in our abstract classes

        response_1 = requests.get(self.url, headers={"User-Agent": self.ua_1})

        Assertions.assert_parse_ua(
            response_1,
            self.ua_1
        )

    @pytest.mark.parametrize('user_agent', user_agents)
    def test_user_agent_parse(self, user_agent):

        response = requests.get(self.url, headers={"User-Agent": user_agent})

        Assertions.assert_parse_ua(
            response,
            user_agent
        )









