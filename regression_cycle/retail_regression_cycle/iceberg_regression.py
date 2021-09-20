from quod_qa.RET.Algo.Algo_Iceberg import QAP_5120, QAP_5122, QAP_5123, QAP_5138, QAP_5175, QAP_5185, QAP_5302
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(session_id, parent_id=None):
    report_id = bca.create_event('DMA', parent_id)
    try:
        QAP_5120.execute(session_id, report_id)
        QAP_5122.execute(session_id, report_id)
        QAP_5123.execute(session_id, report_id)
        QAP_5138.execute(session_id, report_id)
        QAP_5175.execute(session_id, report_id)
        QAP_5185.execute(session_id, report_id)
        QAP_5302.execute(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
