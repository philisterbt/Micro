import os
import pika
import json
import time

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Notification received: {message}")
    # In a real app, this might send an email or push notification

def main():
    print("Notification Service starting...")
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue='notifications')
            channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    main()
