
from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/hello",
                        params={"name": "UUUUser"})

parse_resp_text = response.json()
print(parse_resp_text["answer"])

response2 = requests.get("https://playground.learnqa.ru/api/get_text")

try:
    print(response2.text)
    parse_resp_text_2 = response2.json()
except JSONDecodeError:
    print(f"{response2} is not json format")