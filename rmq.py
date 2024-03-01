import pika
import functools
from pika import DeliveryMode
from pika.exchange_type import ExchangeType
from env import mq_host, mq_user, mq_pw, mq_vhost
    
class MQ:
    def __init__(self):
        credentials = pika.PlainCredentials(mq_user, mq_pw)
        parameters = pika.ConnectionParameters(mq_host, 5672, mq_vhost, credentials=credentials)
        self.connection = pika.SelectConnection(parameters)
        self.channel = self.connection.channel()
        #channel.exchange_declare(exchange='consume', exchange_type=ExchangeType.direct, passive=False, durable=True, auto_delete=False)
        #channel.queue_declare(queue='standard', auto_delete=True)
        self.channel.queue_bind(queue='standard', exchange='consume', routing_key='standard_key')
        self.channel.basic_qos(prefetch_count=1)
    
    def on_message(self, chan, method_frame, header_frame, body, userdata=None):
        self.value = body
        
    def send(self, data):
        self.channel.basic_publish('exchange', 'standard_key', data, pika.BasicProperties(content_type='text/plain', delivery_mode=DeliveryMode.Transient))
        
    def run(self):
        on_message_callback = functools.partial(self.on_message, userdata='on_message_userdata')
        self.channel.basic_consume('standard', on_message_callback)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()
        
    def get(self):
        while True:
            if self.value:
                yield self.value.decode()
                self.value = None