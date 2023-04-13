import boto3
import json
    
def lambda_handler(event, context):
    print('Received event:', event)
    word = event['word']
    test_data = {
        'word' : word,
        'content_type': "application/json",
    }
    payload = json.dumps(test_data)
    
    sagemaker = boto3.client('runtime.sagemaker')
    endpoint_name = 'rnn'
    
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
