import os
import pika
import logging
import app.core.log
from dotenv import load_dotenv

load_dotenv()



class RabbitMQ:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQ, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        try:
            self.host = os.getenv('AMQP_HOST')
            self.port = int(os.getenv('AMQP_PORT'))
            self.user = os.getenv('AMQP_USER')
            self.password = os.getenv('AMQP_PASS')

            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logging.info("[AMQP] Connected to RabbitMQ")
        except Exception as e:
            logging.error(f"[AMQP] Connection failed: {e}")
            self.connection = None
            self.channel = None

    def get_channel(self):
        return self.channel

    def publish(self, exchange, routing_key, body):
        if not self.channel:
            logging.error("[AMQP] Channel not available.")
            return

        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body
            )
            logging.info(f"[AMQP] Published message to {routing_key}")
        except Exception as e:
            logging.error(f"[AMQP] Publish failed: {e}")

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info("[AMQP] Connection closed")