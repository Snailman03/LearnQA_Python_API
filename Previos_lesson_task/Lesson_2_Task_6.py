import requests

response_3 = requests.get("https://playground.learnqa.ru/api/long_redirect")

resp_3_history = response_3.history
len_resp_3_history = len(resp_3_history)


print(f"От изначального URL происходит {len_resp_3_history-1} редиректа \n"
      f"итоговый адрес = {resp_3_history[len_resp_3_history-1].url} ")


# response_2 = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects = True)
# first_response = response_2.history[0]
# second_response = response_2
#
# print(first_response.url)
# print(second_response.url)
#
# print(response_2.status_code)