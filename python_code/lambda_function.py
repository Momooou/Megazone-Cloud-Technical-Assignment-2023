import json
import random
import string
import base64
import webbrowser

print("Loading function")

url_maps = {
    "shortURL": "longURL"
}


def generate_random_string():
    letters_and_digits = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(letters_and_digits, k=5))
    return random_string


def url_shortener(event, context):
    if event['httpMethod'] == "POST":
        print('eventtttt:', event)
        print('contexttt:', context)

        long_url = str(base64.b64decode(event["body"]).decode('utf-8').split('=')[1])
        short_url = generate_random_string()

        if short_url in url_maps:
            short_url = generate_random_string()

        url_maps[short_url] = long_url

        print(url_maps)
        
        return {
            'statusCode': 200,
            'body': json.dumps("https://" + event['headers']['Host'] + "/" +short_url)
        }
    if 'haha' in event['pathParameters']:
        webbrowser.open(event['pathParameters']['haha'])
        return {
            'statusCode': 200
        }
    return {
            'statusCode': 200,
            'body': json.dumps("hi")
        }
