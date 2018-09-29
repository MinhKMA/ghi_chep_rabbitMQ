import os
import pika

url = os.environ.get('CLOUDAMQP_URL', 'amqp://admin:minhkma@192.168.100.65:5672/%2f')
params = pika.URLParameters(url) 
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')