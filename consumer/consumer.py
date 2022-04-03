import pika
import time
import os
import json
import requests

time.sleep(45)

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
server_url = os.environ['SERVER_URL']
ride_url = os.environ['RIDE_URL']
consumer_id = os.environ['CONSUMER_ID']
url_params = pika.URLParameters(amqp_url)

# Send URL to consumer
print(server_url,type(server_url))
dt={"consumerId":consumer_id}
ride_data = {"consumerId":consumer_id,"taskId":1,"time":20,"pickup":"start","destination":"end","cost":50,"seats":3}
requests.post(server_url, json = dt)

print("Consumer")
print("sleeping for 10 seconds")
time.sleep(10)
requests.post(ride_url, json = ride_data)
# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# declare a new queue
# in the rabbitmq volume even between restarts
chan.queue_declare(queue='ride_queue', durable=True)


def receive_msg(ch, method, properties, body):
    data = json.loads(body)
    t = data["time"]
    print("sleeping for ",t," seconds")
    time.sleep(t)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("id",consumer_id, "time:",t )


# to make sure the consumer receives only one message at a time
chan.basic_qos(prefetch_count=1)

chan.basic_consume(queue='ride_queue',
                   on_message_callback=receive_msg)

chan.start_consuming()
