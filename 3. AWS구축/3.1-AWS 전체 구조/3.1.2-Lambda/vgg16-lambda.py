import boto3
import json
    
def lambda_handler(event, context):
    print('Received event:', event)
    # value = event['nameValuePairs']
    bucket = event['bucket']
    image_uri = event['image_uri']
    test_data = {
        'bucket' : bucket,
        'image_uri' : image_uri,
        'content_type': "application/json",
    }
    payload = json.dumps(test_data)
    
    sagemaker = boto3.client('runtime.sagemaker')
    endpoint_name = 'vgg16'
    
    response = sagemaker.invoke_endpoint(EndpointName=endpoint_name, 
                                       ContentType='application/json', 
                                       Body=payload)
    
    result = json.loads(response["Body"].read(), encoding='utf-8')
    
    result.update({"success" : True})
    print(result)
    
    # return json.dumps(result, ensure_ascii=False)
    return result
    # return  str(result)
    # return result