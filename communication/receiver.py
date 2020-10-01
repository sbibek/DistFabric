import pika
import threading

class DfReceiver:
    def __init__(self, config, callback):
        self.config = config["rabbitmq"]
        self. connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config["host"], 
            port=self.config["port"], 
            virtual_host="/",
            credentials=pika.PlainCredentials(self.config['user'], self.config['pass'])
            ))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.config["exchange"], exchange_type=self.config["type"]) 
        self.q = self.channel.queue_declare(queue='', exclusive=True)
        self.channel.queue_bind(exchange=self.config["exchange"], queue=self.q.method.queue)
        self.channel.basic_consume(queue=self.q.method.queue, on_message_callback=self.__received, auto_ack=True)
        self.callback = callback
    

    def __received(self, ch, method, properties, body):
        # the callback should be made as a thread so that we dont 
        # break anything in connection
        respThread = threading.Thread(target=self.callback, args=(body,))
        respThread.start()
    
    def start(self):
        self.channel.start_consuming() 