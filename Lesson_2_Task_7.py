import requests
import pytest

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"


'''
1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
'''

response_get_NOparams = requests.get(URL)
response_post_NOdata = requests.post(URL)
print(f"get request without params = {response_get_NOparams.text} \n"
      f"post request without data = {response_post_NOdata.text}")

'''
2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
'''

response_get_incorrect_params = requests.get(URL, params={"method": "HEAD"})
print(f"Делает http-запрос не из списка method = HEAD. \n"
      f" = {response_get_incorrect_params.text}")

'''
3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
'''
response_get_ok = requests.get(URL, params={"method": "GET"})
print(response_get_ok.text)

response_post_ok = requests.post(URL, data={"method": "POST"})
print(response_post_ok.text)

response_put_ok = requests.put(URL, data={"method": "PUT"})
print(response_put_ok.text)

response_delete_ok = requests.delete(URL, data={"method": "DELETE"})
print(response_delete_ok.text)

"""
 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и 
 значений параметра method. Например с GET-запросом передает значения параметра method равное ‘GET’, 
 затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для всех типов запроса. 
 Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок. 
 Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
"""


def test_get_request():
    data_list = ["GET", "POST", "PUT", "DELETE"]

    print("Check status code and response text for GET ")
    for data in data_list:
        print(f" get request current param method value = {data}")
        payload = {"method": data}
        resp_current_get_param = requests.get(URL, params=payload)
        print(resp_current_get_param.text)
        print(resp_current_get_param.status_code)
        try:
            if data == "GET":
                print(resp_current_get_param.json())
                assert resp_current_get_param.json()["success"] == "!"
                assert resp_current_get_param.status_code == 200
            else:
                assert resp_current_get_param.text == "Wrong method provided"
                assert resp_current_get_param.status_code != 200
        except AssertionError:
            print("Ответ 200 некорректен при отправке в params метода не GET")


def test_post_request():
    data_list = ["GET", "POST", "PUT", "DELETE"]

    print("Check status code and response text for POST ")
    for data in data_list:
        print(f" get request current param method value = {data}")
        payload = {"method": data}
        resp_current_post_param = requests.post(URL, data=payload)
        print(resp_current_post_param.text)
        print(type(resp_current_post_param.status_code))
        try:
            if data == "POST":
                print(resp_current_post_param.json())
                assert resp_current_post_param.json()["success"] == "!"
                assert resp_current_post_param.status_code == 200
            elif data != "POST":
                assert resp_current_post_param.text == "Wrong method provided"
                assert resp_current_post_param.status_code != 200
        except AssertionError:
            print("Ответ 200 некорректен при отправке в data метода не POST")
      
            
def test_put_request():
    data_list = ["GET", "POST", "PUT", "DELETE"]

    print("Check status code and response text for PUT ")
    for data in data_list:
        print(f" get request current param method value = {data}")
        payload = {"method": data}
        resp_current_put_param = requests.put(URL, data=payload)
        print(resp_current_put_param.text)
        print(type(resp_current_put_param.status_code))
        try:
            if data == "PUT":
                print(resp_current_put_param.json())
                assert resp_current_put_param.json()["success"] == "!"
                assert resp_current_put_param.status_code == 200
            elif data != "PUT":
                assert resp_current_put_param.text == "Wrong method provided"
                assert resp_current_put_param.status_code != 200
        except AssertionError:
            print("Ответ 200 некорректен при отправке в data метода не PUT")


def test_delete_request():
    data_list = ["GET", "POST", "PUT", "DELETE"]

    print("Check status code and response text for DELETE ")
    for data in data_list:
        print(f" get request current param method value = {data}")
        payload = {"method": data}
        resp_current_delete_param = requests.delete(URL, data=payload)
        print(resp_current_delete_param.text)
        print(type(resp_current_delete_param.status_code))
        try:
            if data == "DELETE":
                print(resp_current_delete_param.json())
                assert resp_current_delete_param.json()["success"] == "!"
                assert resp_current_delete_param.status_code == 200
            elif data != "DELETE":
                assert resp_current_delete_param.text == "Wrong method provided"
                assert resp_current_delete_param.status_code != 200
        except AssertionError:
            print("Ответ 200 некорректен при отправке в data метода не delete")