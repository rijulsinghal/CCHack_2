
# imports
import pika 
import uuid
import json
import os
from flask import Flask, request
#from flask_cors import CORS
import time

time.sleep(10)
# Initialisations
app = Flask(__name__)
#CORS(app)
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(url_params)
channel = connection.channel()

channel.queue_declare(queue='ride_queue', durable=True)
channel.queue_declare(queue='ride_database', durable=True)
consumerData = []


print("[x] Ready to send messages")
@app.route('/')
def home():
    return "Hello, this is HomePage"

@app.route('/new_ride', methods=['POST'])
def new_ride():
    data = request.get_json(force=True)
    print(data["pickup"])
    print(consumerData)
    #checking if consumer exists or not
    f = 0
    #print("consumerdATA ", type(consumerData[0]))
    for map in consumerData:
        if data["consumerId"]==map["name"]:
            f = 1
            break
    if(f==0):
        return "Consumer doesn't exist"
    taskId = str(uuid.uuid4())
    data['taskId'] = taskId
    print(data['taskId'])
    channel.basic_publish(exchange='',routing_key = 'ride_queue',body = json.dumps(data),properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                      ))
    print (" [x] Sent data")
    # send data to database
    channel.basic_publish(exchange='',routing_key = 'ride_database',
                        body = json.dumps(data),properties=pika.BasicProperties(delivery_mode = 2, # make message persistent
                      ))
    print (" [x] Sent data to database")
    return json.dumps({'taskId': taskId}), 200, {'ContentType':'application/json'}

@app.route('/new_ride_matching_consumer', methods=['POST'])
def new_ride_matching_consumer():
    data = request.get_json(force=True)
    ip = request.remote_addr
    map = {"name":data['consumerId'],"IP":ip}
    consumerData.append(map)
    print(consumerData)
    return "Consumer added successfully"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)

"""
"consumerId":1,
    "serverIp":"127.0.0.1",
    "consumerIp":"127.0.0.1",
    "name":"test"

"consumerId":1,
    "taskId":1,
    "time":20,
    "pickup":"start",
    "destination":"end",
    "cost":50,
    "seats":3
"""