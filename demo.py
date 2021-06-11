import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.PostTrade import QAP_2780, QAP_3304, QAP_2615, QAP_3000, QAP_3315, QAP_3332, QAP_3334, QAP_3337, \
    QAP_2850, QAP_3338
from stubs import Stubs
from quod_qa.eq.Care import QAP_2611, QAP_3306, QAP_1075, QAP_1074, QAP_1365


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
        QAP_3338.execute(report_id)
    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()