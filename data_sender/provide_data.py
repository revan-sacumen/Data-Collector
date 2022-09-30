import names
import random
import  logging

module_logger = logging.getLogger("collectors_and_sender.data")
class SendData:
    '''
    creating calss for sending different datas  
    '''
    def __init__(self):
        self.logger = logging.getLogger("collectors_and_sender.data.SendData")
        self.logger.info('creating instance of SendData...')
    def send_data(self):
        self.logger.info("Preparing to data send")
        body = ["JamesBond","stroy","TopGun","Mission","Imposible"]
        return {
            'title':names.get_full_name(),
            'body':random.choice(body),
            'userId':random.randint(1,100)
        }
    module_logger.info("Data successfully sent")


