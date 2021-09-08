from quod_qa.RET.Care import QAP_1719, QAP_4286, QAP_4313, QAP_5087, QAP_5088, QAP_493, QAP_5139, QAP_5142, QAP_5143, \
    QAP_495, QAP_494, QAP_496, QAP_497, QAP_5144, QAP_5145, QAP_5146, QAP_5147
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('Care regression', parent_id)

    try:
        QAP_4286.execute(session_id, report_id)
        QAP_4313.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()

