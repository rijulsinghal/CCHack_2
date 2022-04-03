# import required libraries
from tinydb import TinyDB
import pika
import json
import time
import os

time.sleep(30)

# Read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# Connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

chan.queue_declare(queue='ride_database', durable=True)

# Create a local database
db = TinyDB('./db.json')

def receive_msg(ch, method, properties, body):
    db.insert(json.loads(body))
    print("Data added successfully")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# To make sure the consumer receives only one message at a time
# Next message is received only after acking the previous one
chan.basic_qos(prefetch_count=1)

# Define the queue consumption
chan.basic_consume(queue='ride_database', on_message_callback=receive_msg)

chan.start_consuming()

