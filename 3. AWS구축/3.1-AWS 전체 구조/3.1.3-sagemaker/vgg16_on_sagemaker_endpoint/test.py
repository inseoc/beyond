import requests
import json

url='http://127.0.0.1:5000/invocations'

bucket = 'sagemaker-studio-8r6zfwskopd'
image_uri = 'train/01_ginpal/100217797_1.jpg'
test_data = {
    'bucket' : bucket,
    'image_uri' : image_uri,
    'content_type': "application/json",
}
payload = json.dumps(test_data)


r = requests.post(url,data=payload)

#show result
print (r.text)