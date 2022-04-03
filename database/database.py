# import required libraries
from tinydb import TinyDB
import pika
import json
import time
import os

time.sleep(30)
# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

chan.queue_declare(queue='ride_database', durable=True)

# create a local database
db = TinyDB('./db.json')

def receive_msg(ch, method, properties, body):
    db.insert(json.loads(body))
    print("Data added successfully")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# to make sure the consumer receives only one message at a time
# next message is received only after acking the previous one
chan.basic_qos(prefetch_count=1)

# define the queue consumption
chan.basic_consume(queue='ride_database',
                   on_message_callback=receive_msg)

chan.start_consuming()

#To connect with the pymongo library:

# import json
# import pika
# import time
# import os
# import pymongo

# time.sleep(30)

# #channel for database
# amqp_url = os.environ['AMQP_URL']
# url_params = pika.URLParameters(amqp_url)

# # connect to rabbitmq
# connection = pika.BlockingConnection(url_params)
# chan = connection.channel()

# chan.queue_declare(queue='ride_database', durable=True)

# #mongoDB connection
# mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')
# myDB = mongoClient["rideDB"]
# myCollection = myDB["consumer"]
# cursor = myCollection.find()


# print ("[*] Waiting for payload. To exit press CTRL+C")

# def dbCallback(ch, method, properties, body):
#     payload = json.loads(body)
#     print("[x] Processing Request")
#     # time.sleep(payload.get('time'))
#     myCollection.insert_one(payload)
#     #print name of the consumer from the database
#     for document in cursor:
#         print(document)
#     ch.basic_ack(delivery_tag = method.delivery_tag)



# channel.basic_consume(on_message_callback=dbCallback, queue='rideSharingQueue')
# channel.start_consuming()
