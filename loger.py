import logging
from data_sender import provide_data
import create_post
import producer
#creating logger with data sender name
logger = logging.getLogger("collectors_and_sender")
logger.setLevel(logging.DEBUG)

#creating formmatters
formatters = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#creating Filehandler and seting level 
fh = logging.FileHandler('post_creation.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# seting formatters to Handlers
fh.setFormatter(formatters)
ch.setFormatter(formatters)

#adding handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

#creating instance for sendind data 
logger.info('creating an instance of data_prvoviders')
a = provide_data.SendData()
logger.info('created an instance of data_prvoviders')

#calling function to send data using cls_instance_obj
logger.info("data sending")
a.send_data()
logger.info("data sent successfully")

#Receving data and creating posts
logger.info('creating reciver data instance')
b = create_post.CreatePost()
logger.info("created reciver data object instance")

#here calling create function create posts
logger.info("module ready to receiveing data coming from different modules")
b.post_creation()
logger.info('Data received successfully')

#displaying posts what we posts
logger.info("geting recently posted data")
b.display()
logger.info("geted data")

#producing some into queue sources
logger.info('Sending prodcer source')
b = producer.ProducerClass()
logger.info('Producer sending ')

logger.info("Data producing")
# #Testing posts are created proper
# logger.info('testing is data is posted')
# b.test_posted_data()
# logger.info('response test case your getting')

