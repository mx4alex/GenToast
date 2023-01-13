from transformers import GPT2Tokenizer, GPT2LMHeadModel
import pika
import os
import torch

import gen_producer
import gen_consumer

amqp_url = os.getenv("RABBITMQ_URL")
connection_parameters = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(connection_parameters)
input_channel = connection.channel()
input_channel.queue_declare(queue='predict')

output_channel = connection.channel()
output_channel.queue_declare(queue='result')

DEVICE = torch.device('cpu')

def callback(ch,method,properties,body):
    input_data, id = gen_consumer.consume(body)

    path_to_model = 'best_model'
    tokenizer = GPT2Tokenizer.from_pretrained(path_to_model)
    model = GPT2LMHeadModel.from_pretrained(path_to_model).to(DEVICE)
    model.eval()
    input_ids = tokenizer.encode(input_data, return_tensors='pt').to(DEVICE)
    with torch.no_grad():
        out = model.generate(input_ids, 
                            do_sample=True,
                            temperature=1.8,
                            top_p=0.8,
                            top_k=50,
                            max_length=80,
                            min_length=30,
                            no_repeat_ngram_size=2
                            )

    gen_text = list(map(tokenizer.decode, out))[0]
    out_text = gen_text.replace('[SJ]', '').split('[ET]')[0]

    gen_producer.publish(id, out_text, output_channel)

input_channel.basic_consume(on_message_callback=callback, queue='predict')

try:
    input_channel.start_consuming()
except Exception:
    input_channel.stop_consuming()
    
