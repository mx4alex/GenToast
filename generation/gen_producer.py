import json

def publish(id, out_text, output_channel):
    json_parameters = {
        "chat_id" : id,
        "text" : out_text
    }

    json_message = json.dumps(json_parameters)
    output_channel.basic_publish(exchange='', routing_key="result", body=json_message)