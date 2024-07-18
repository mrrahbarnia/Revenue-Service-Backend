# import pika
# import json


# connection = pika.BlockingConnection(
#     pika.URLParameters("amqp://guest:guest@rabbitmq/")
# )
# channel = connection.channel()


# channel.queue_declare(
#     queue="main_queue", durable=True, arguments={"x-dead-letter-exchange": "dlx", "x-message-ttl": 2000}
# )