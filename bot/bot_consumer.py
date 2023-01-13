import aio_pika
import json
import codecs
from aiogram import Bot
from aiogram.dispatcher import FSMContext

async def consume(bot, storage, amqp_url):
    amqp_connection = await aio_pika.connect_robust(
        amqp_url, 
    )
    
    queue_name = 'result'

    async with amqp_connection:
        channel = await amqp_connection.channel()

        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    input_message = codecs.decode(message.body, 'UTF-8')

                    input_json = json.loads(input_message)
                    text = input_json['text']
                    id = input_json['chat_id']

                    await bot.send_message(id, text)
                    end_state = FSMContext(storage, id, id)
                    await end_state.finish()