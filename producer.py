from kafka import KafkaProducer
from create_post import CreatePost
import json
import logging
import time
module_logger = logging.getLogger(__name__)
class ProducerClass:
    '''
    getting data continuly so that data distrbuting with source
    '''
    def __init__(self):
        self.logger = logging.getLogger('Creatpost_to_producer')
        self.logger.info('producer producing data into kafka')

    def json_serilizers(data):
        return json.dumps(data).encode('utf-8')

    producer = KafkaProducer(
                                bootstrap_servers=['127.0.1.1:9092'],
                                value_serializer=json_serilizers
                            )
    module_logger.info('Data sending to Kafka')
    data=CreatePost().display()
    producer.send('random_data',data)
