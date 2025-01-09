
import pytest
import requests
import time

URL = "https://playground.learnqa.ru/ajax/api/longtime_job"


def test_check_not_ready_status(generate_incorrect_token):
    resp_new_task_create = requests.get(URL)
    parse_1 = resp_new_task_create.json()
    token = parse_1['token']
    resp_check_status = requests.get(URL, params={"token": token})
    parse_2 = resp_check_status.json()

    assert parse_2["status"]== 'Job is NOT ready'

    resp_check_status_incorrect = (
        requests.get(URL, params={"token": generate_incorrect_token}))
    parse_3 = resp_check_status_incorrect.json()
    print(parse_3["error"])

    assert parse_3["error"] == "No job linked to this token"

def test_check_ready_status(generate_incorrect_token):
    resp_new_task_create = requests.get(URL)
    parse_1 = resp_new_task_create.json()
    token = parse_1['token']
    time.sleep(60)
    resp_check_status = requests.get(URL, params={"token": token})
    parse_3 = resp_check_status.json()
    status_2 = parse_3['status']

    assert status_2 == 'Job is ready'
    assert 'result' in parse_3

    resp_check_status_2 = requests.get(URL, params={"token": generate_incorrect_token})
    parse_4 = resp_check_status_2.json()

    assert parse_4["error"] == "No job linked to this token"