import json
import random
import string
import base64
import urllib.parse
import time

print("Loading function")

url_maps = {
    "shortURL": {"long_url": "longURL",
                 'created_at': "time"}
}

def set_with_ttl(key, value):
    url_maps[key] = {'long_url': value, 'created_at': time.time()}

def get_with_ttl(key):
    data = url_maps.get(key)
    
    if data and (time.time() - data['created_at']) < 30:
        return data['long_url']
    else:
        return None
    
def generate_random_string():
    letters_and_digits = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(letters_and_digits, k=5))
    return random_string


def url_shortener(event, context):
    # POST /urlshortener endpoint
    if event['resource'].startswith('/urlshortener'):
        long_url = str(base64.b64decode(
            event["body"]).decode('utf-8').split('=')[1])
        short_url = generate_random_string()

        while short_url in url_maps:
            short_url = generate_random_string()

        # url_maps[short_url]['long_url'] = long_url
        set_with_ttl(short_url, long_url, )

        print(url_maps)

        return {
            'statusCode': 200,
            'body': "https://" + event['headers']['Host'] + "/dev/short/" + short_url
        }
    # GET /short/{short_url} endpoint
    else:
        req_url = event['pathParameters']['short_url']
        dest_url = get_with_ttl(req_url)
        if req_url in url_maps and dest_url is not None:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': urllib.parse.unquote(dest_url)
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps("Not found.")
            }
