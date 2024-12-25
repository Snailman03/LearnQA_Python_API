import json
from json.decoder import JSONDecodeError


str_as_json_format_2 = '{"messages":[{"message":"This is the first message",' \
                       '"timestamp":"2021-06-04 16:40:53"},' \
                       '{"message":"And this is a second message",' \
                       '"timestamp":"2021-06-04 16:41:01"}]}'

try:
    obj_2 = json.loads(str_as_json_format_2)
    print(obj_2['messages'][1]['message'])
except JSONDecodeError:
    print("Сообщение распарсить не удалось")

# str_as_json_format = '{"answer":"Hello User"}'
#
# obj = json.loads(str_as_json_format)
# key = "answer2"
#
# if key in obj:
#     print(obj[key])
# else:
#     print(f"Ключа {key} в json нет")


