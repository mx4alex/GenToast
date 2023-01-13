import json
import pika

def publish(id, text, connection_parameters):
    json_parameters = {
        "chat_id" : id,
        "text" : text[:-1]
    }

    json_message = json.dumps(json_parameters)

    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='predict')
    channel.basic_publish(exchange='', routing_key='predict', body=json_message)
    connection.close()