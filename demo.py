import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.PostTrade import QAP_3338, QAP_3337
from stubs import Stubs


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('ymoroz ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        QAP_3337.execute(report_id)
    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()