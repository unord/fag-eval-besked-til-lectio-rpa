import logging
import class_msg
import datetime


def log(this_log_msg:str):

    # now we will Create and configure logger
    logging.basicConfig(filename=f"logs/fag-eval-{class_msg.log_date.year}{class_msg.log_date.month}{class_msg.log_date.day}{class_msg.log_date.hour}{class_msg.log_date.minute}.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    now = datetime.datetime.now()
    print(f"{now}: {this_log_msg}")

    # Let us Create an object
    logger = logging.getLogger()

    # Now we are going to Set the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    # some messages to test
    logger.debug(this_log_msg)
