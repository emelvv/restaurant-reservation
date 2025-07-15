import os
import json
import pika
from .schemas import BookingCreated
from .notifier import send_notification


def consume():
    url = os.getenv("RABBITMQ_URL")
    params = pika.URLParameters(url)
    params.heartbeat = 300
    params.blocked_connection_timeout = 300
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.exchange_declare(exchange="booking_events",
                             exchange_type="topic", durable=True)
    q = channel.queue_declare(queue="notify_queue", durable=True).method.queue
    channel.queue_bind(exchange="booking_events", queue=q,
                       routing_key="booking.created")

    def callback(ch, method, props, body):
        data = json.loads(body)
        event = BookingCreated(**data)
        send_notification(event)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=q, on_message_callback=callback)
    channel.start_consuming()
