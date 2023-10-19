import json
import random
import string
import base64
import urllib.parse
import time

print("Loading function")

# dict to store the mapping between short and long URLs and their created time
url_maps = {
    "<short URL>": {"long_url": "<long URL>",
                    "created_at": "<creation time>"}
}

# functions to set and get url_maps with expiry
def set_with_ttl(key, value):
    url_maps[key] = {'long_url': value, 'created_at': time.time()}
    print("url_maps updated:", url_maps)


def get_with_ttl(key):
    value = url_maps.get(key)
    ttl = 30

    if value and (time.time() - value['created_at']) < ttl:
        return value['long_url']
    else:
        print("Failed accessing", key)
        return None

# function to generate random string with 5 letters/digits
def generate_random_string():
    letters_and_digits = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(letters_and_digits, k=5))
    return random_string

# function to handle events from AWS API gateway
def url_shortener(event, context):
    # POST /urlshortener endpoint
    if event['resource'].startswith('/urlshortener'):
        long_url = str(base64.b64decode(
            event["body"]).decode('utf-8').split('=')[1])
        short_url = generate_random_string()
        
        # generate short_url again if it already exists
        while short_url in url_maps:
            short_url = generate_random_string()

        # store short-long URL pair to url_maps
        set_with_ttl(short_url, long_url)

        return {
            'statusCode': 200,
            'body': "https://" + event['headers']['Host'] + "/dev/short/" + short_url
        }
    # GET /short/{short_url} endpoint
    else:
        req_url = event['pathParameters']['short_url']
        dest_url = get_with_ttl(req_url)

        # redirect user if short URL exists and not expired
        if req_url in url_maps and dest_url is not None:
            print("Redirected user to", req_url)
            return {
                'statusCode': 302,
                'headers': {
                    'Location': urllib.parse.unquote(dest_url)
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': "Not found."
            }
