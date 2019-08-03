import pika
import uuid
import os


class RmqClient(object):

    def __init__(self):
        parameter = pika.URLParameters(os.getenv('RMQ_URL'))
        self.connection = pika.BlockingConnection(parameter)

        self.channel = self.connection.channel()
        self.queue_name = os.getenv('RMQ_QUEUE')

        result = self.channel.queue_declare(
            queue=self.queue_name, durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
