import pika
import json

class DfSender:
    def __init__(self, config):
        self.config = config["rabbitmq"]
        self. connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config["host"], 
            port=self.config["port"], 
            virtual_host="/",
            credentials=pika.PlainCredentials(self.config['user'], self.config['pass'])
            ))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.config["exchange"], exchange_type=self.config["type"]) 
    
    def sendToNodes(self, message):
        message['from'] = self.config['whoAmI']
        self.channel.basic_publish(exchange=self.config['exchange'], routing_key='', body=json.dumps(message))