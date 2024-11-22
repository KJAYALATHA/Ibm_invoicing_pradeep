# importing module
import inspect
import logging
import os

import coloredlogs


def custom_logger(log_level=logging.DEBUG):
    """
    wrapper function to create new instance of logger
    :param log_level:
    :return: logger object
    """
    # Gets the name of the class / method from where this method is called
    msg_format: str = '%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s'
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        # By default, log all messages
        logger.setLevel(logging.DEBUG)
        # check if the dir exists
        file_path = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        #  add file handler
        file_name = os.path.join(file_path, "IBMInvoiceRPA.log")
        # mode we are setting it to append
        file_handler = logging.FileHandler(file_name, mode='a')
        file_handler.setLevel(log_level)

        formatter = logging.Formatter(msg_format, datefmt='%d/%m/%Y %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # add console handler
        coloredlogs.install(fmt=msg_format, level='DEBUG', logger=logger)

    return logger
