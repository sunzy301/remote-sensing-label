# coding=utf-8

import json

data = [{'a':"A",'b':(2,4),'c':3.0}]  #list对象
print("DATA:", repr(data))

data_string = json.dumps(data)
print("JSON:", data_string)
print(type(data_string))

decode_data = json.loads(data_string)
print("DECODE DATE:", repr(decode_data), type(decode_data))