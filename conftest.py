import pytest
import random, string


@pytest.fixture
def generate_incorrect_token():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(7))