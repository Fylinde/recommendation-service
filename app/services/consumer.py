import pika
import os
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")
    # Process message here (e.g., updating a product in the recommendation system)

def consume_messages(queue_name):
    url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
    )

    print(f"Waiting for messages in {queue_name}...")
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages(queue_name='product_queue')
