import json
import random
import string


print("Loading function")

url_maps = {
    "longURL": "shortURL"
}


def generate_random_string():
    letters_and_digits = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(letters_and_digits, k=5))
    return random_string


def url_shortener(event, context):
    if event['httpMethod'] == "POST":
        print('eventtttt:', event)
        print('contexttt:', context)
        long_url = event['queryStringParameters']
        short_url = generate_random_string()

        if short_url in url_maps.values():
            short_url = generate_random_string()

        url_maps[long_url] = short_url

        print(url_maps)
        
        return {
            'statusCode': 200,
            'body': json.dumps("https://" + event['headers']['host'] + "/" +short_url)
        }
    return {
            'statusCode': 200,
            'body': json.dumps("hi")
        }
