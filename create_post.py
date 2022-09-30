from email import header
import requests
import os 
from dotenv import load_dotenv
import json
import  logging
from data_sender.provide_data import SendData

load_dotenv()
URL = os.getenv('URL')
FETCHURL = os.getenv('FETCHURL')
module_loggger = logging.getLogger("collectors_and_sender.CreatePost")

class CreatePost:
    '''
        geting random data from target source and post data into different apis
        receving mulitipale data and saving into file 
    '''
    def __init__(self):
        self.logger = logging.getLogger("collectors_and_sender.CreatePost")
        self.logger.info("post creation objects created")

    def post_creation(self):
        headers = {'Content-type':'application/json; charset=UTF-8'}
        self.logger.info("Data reciving...")
        py_obj = SendData().send_data()
        requests.post(f'{URL}/posts',headers=headers,data=json.dumps(py_obj))

    def display(self):
        self.logger.info('loading data into file')
        res = requests.get(FETCHURL)
        try:
            with open(file='{}.json'.format(res.status_code),mode='w') as f:
                f.write(res.text)
        except Exception as e:
            self.logger.error(e)
        return res.text