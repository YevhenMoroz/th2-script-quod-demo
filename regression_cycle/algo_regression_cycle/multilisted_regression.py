import os

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None):
    report_id = bca.create_event(os.path.basename(__file__) + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    try:
        pass
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
