import requests
import json

url='http://127.0.0.1:5000/invocations'

test_data = {
    "category" : "원피스",
    "color" : "파란색",
    "size" : "M",
    "washing" : "손세탁",
    'content_type': "application/json"
}
payload = json.dumps(test_data)


r = requests.post(url,data=payload)

#show result
print (r.text)