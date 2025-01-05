import requests
import pytest

class TestTenTask:

    def test_phrase_len(self):

        phrase = input("Set a phrase: ")
        len_phrase = len(phrase)

        assert len_phrase < 15 ,"The phrase len greater then 15 symbols"





