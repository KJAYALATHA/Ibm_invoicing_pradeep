import requests
from urllib3 import HTTPSConnectionPool

from log_handler import custom_logger

log = custom_logger()


def monitor(url):
    """
    method to check if a web portal is up and accessible
    :param url: url of the web portal
    :return: True else False
    """
    try:
        res = requests.head(url)
    except HTTPSConnectionPool:
        return True
    else:
        if res.status_code == 200:
            log.info("Application was reachable")
            return True
        else:
            log.info("Application was not reachable, hence terminating the execution of bot")
            return False
