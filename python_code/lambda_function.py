import json

print("Loading function")

def url_shortener(event, context):
    print('event:', event)
    x = event['queryStringParameters']
    print(x)

    return {
        'statusCode': 200,
        'body': json.dumps('Helloooo from Lambda!')
    }

