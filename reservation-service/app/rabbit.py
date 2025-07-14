import os
import json
import pika

# один глобальный канал на всё приложение
_connection = None
_channel = None


def get_channel():
    global _connection, _channel
    if _channel and _channel.is_open:
        return _channel

    params = pika.URLParameters(os.getenv("RABBITMQ_URL"))
    params.heartbeat = 300
    params.blocked_connection_timeout = 300

    _connection = pika.BlockingConnection(params)
    _channel = _connection.channel()
    _channel.exchange_declare(
        exchange='booking_events',
        exchange_type='topic',
        durable=True
    )
    return _channel


def publish_booking_created(booking_data: dict):
    ch = get_channel()
    ch.basic_publish(
        exchange='booking_events',
        routing_key='booking.created',
        body=json.dumps(booking_data),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2
        )
    )
