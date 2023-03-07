import json
import uuid

import pika
from aio_pika import connect_robust
from sqlalchemy.orm import Session

from app.transaction_api.crud import CRUDWallet
from app.transaction_api.schemas import AddCoin
from config import settings
from db.session import get_session


class PikaClient:
    def __init__(self, queue_name):
        self.publish_queue_name = queue_name
        self.credentials = pika.PlainCredentials(
            settings.LOGIN_RABBITMQ, settings.PASS_RABBITMQ
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq", port=5672, credentials=self.credentials
            )
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(
            queue=self.publish_queue_name, durable=True
        )
        self.callback_queue = self.publish_queue.method.queue
        self.response = None

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(
            host="rabbitmq",
            port=5672,
            loop=loop,
            login=settings.LOGIN_RABBITMQ,
            password=settings.PASS_RABBITMQ,
        )
        channel = await connection.channel()
        queue = await channel.declare_queue(self.publish_queue_name, durable=True)
        await queue.consume(self.process_incoming_message, no_ack=False)
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        await message.ack()
        body = json.loads(json.loads(message.body))
        body = AddCoin.parse_obj(body)
        if body.rem:
            CRUDWallet().remove_coin(db=get_session(), msg=body)
        else:
            CRUDWallet().add_coin(db=get_session(), msg=body)

    def send_message(self, message):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange="",
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message.json()),
        )
