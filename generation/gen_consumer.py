import json
import codecs

def consume(body):
    input_message = codecs.decode(body, 'UTF-8')

    input_json = json.loads(input_message)
    print(input_json)

    input_data = input_json['text']
    id = input_json['chat_id']
    return input_data, id